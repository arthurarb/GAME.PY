import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas - FINAL ADM", page_icon="🐲", layout="wide")

# --- SISTEMA DE SAVE/LOAD ---
def export_save():
    dados = {k: v for k, v in st.session_state.items() if k not in ['log']}
    return json.dumps(dados, indent=4)

def carregar_save(arquivo):
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.update(dados)
        st.rerun()

# --- INICIALIZAÇÃO ---
if 'nome_heroi' not in st.session_state:
    st.title("🐲 Dragões e Espadas")
    st.subheader("Retornar à Jornada")
    arquivo_save = st.file_uploader("Arraste seu arquivo .json aqui:", type=["json"])
    if arquivo_save and st.button("Confirmar Carregamento 📂"):
        carregar_save(arquivo_save)
    st.write("---")
    
    st.subheader("Nova Jornada")
    nome = st.text_input("Nome do novo herói:", placeholder="Ex: Arthur")
    
    if st.button("Iniciar Nova Jornada ⚔️"):
        if nome:
            st.session_state.update({
                'nome_heroi': nome, 'classe': "Nenhuma 👤", 'vida_max': 100, 'vida': 100, 
                'moedas': 20, 'pocoes': 2, 'pocoes_furia': 0, 'furia_rodadas': 0,
                'espada': {"nome": "Madeira 🪵", "dano": 7},
                'armadura': {"nome": "Madeira 🪵", "bonus": 0},
                'em_combate': False, 'monstro': None, 'na_vila': False,
                'achou_vila': False, 'log': [f"{nome} iniciou a jornada!"],
                'missoes_ativas': {}, 'em_dungeon': False, 'dungeon_tipo': None
            })
            st.rerun()
    st.stop()

# --- FUNÇÕES ---
def spawn(tipo_nome=None):
    m_data = {
        "Gosma 🟢": {"n": "Gosma 🟢", "v": 30, "d": 4, "o": 5},
        "Goblin 👺": {"n": "Goblin 👺", "v": 50, "d": 9, "o": 10},
        "Dragão 🐲": {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 30},
        "🔥 REI DRAGÃO 🔥": {"n": "🔥 REI DRAGÃO 🔥", "v": 500, "d": 25, "o": 500},
        "🌌 DRAGÃO DEUS 🌌": {"n": "🌌 DRAGÃO DEUS 🌌", "v": 9999, "d": 999, "o": 9999}
    }
    if tipo_nome and tipo_nome in m_data:
        st.session_state.monstro = m_data[tipo_nome].copy()
    else:
        st.session_state.monstro = m_data[random.choice(["Gosma 🟢", "Goblin 👺", "Dragão 🐲"])].copy()
    st.session_state.em_combate = True

# --- SIDEBAR ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.caption(f"Classe Atual: {st.session_state.classe}")
    st.write(f"❤️ HP: {st.session_state.vida} / {st.session_state.vida_max}")
    st.progress(max(0.0, min(1.0, st.session_state.vida / st.session_state.vida_max)) if st.session_state.vida_max > 0 else 0.0)
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    st.write(f"🗡️ Arma: {st.session_state.espada['nome']} | 🛡️ Armadura: {st.session_state.armadura['nome']}")
    st.markdown(f"### 💰 {st.session_state.moedas} Moedas")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 FÚRIA ATIVA: {st.session_state.furia_rodadas} rodadas!")
    else:
        st.write("❄️ Fúria Inativa")

    if st.session_state.missoes_ativas:
        st.markdown("---")
        st.subheader("📜 Missões Ativas")
        for npc, dados in list(st.session_state.missoes_ativas.items()):
            prog = ", ".join([f"{k}: {dados['p'][k]}/{dados['a'][k]}" for k in dados['a']])
            st.write(f"**{npc}**: {prog}")
            if st.button(f"❌ Cancelar {npc}", key=f"can_{npc}"):
                del st.session_state.missoes_ativas[npc]; st.rerun()
    st.markdown("---")
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name="save_dragao.json")
    
    with st.expander("🔐 Painel Admin"):
        senha = st.text_input("Senha", type="password")
        if senha == "05062012":
            if st.button("💰 +99k Moedas"): st.session_state.moedas += 99000; st.rerun()
            if st.button("❤️ VIDA INFINITA"): st.session_state.vida_max = 999999; st.session_state.vida = 999999; st.rerun()
            if st.button("🏘️ Spawn Vila"): st.session_state.achou_vila = True; st.rerun()
            esc_m = st.selectbox("Monstro:", ["Gosma 🟢", "Goblin 👺", "Dragão 🐲", "🔥 REI DRAGÃO 🔥"])
            if st.button("Spawn Monstro"): spawn(esc_m); st.rerun()

# --- LÓGICA DE BATALHA ---
if st.session_state.vida <= 0:
    st.error("💀 VOCÊ MORREU!")
    if st.button("Pagar Resgate (50 💰) e Renascer"):
        if st.session_state.moedas >= 50: st.session_state.moedas -= 50; st.session_state.vida = 25; st.session_state.em_combate = False; st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    
    # Buffs de Classe no Dano
    d_base = st.session_state.espada['dano']
    if st.session_state.classe == "Bárbaro 🪓": d_base += 5
    
    mult = 2.5 if (st.session_state.furia_rodadas > 0 and st.session_state.classe == "Mago 🧙") else (1.7 if st.session_state.furia_rodadas > 0 else 1.0)
    d_at = int(d_base * mult)
    
    if st.session_state.classe == "Arqueiro 🏹" and random.random() < 0.2:
        d_at *= 2
        st.warning("🎯 CRÍTICO!")

    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    if st.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if st.session_state.classe == "Clérigo ⛪": st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + 5)
        
        if m['v'] <= 0:
            rec = int(m['o'] * 1.5) if st.session_state.classe == "Mercador 💰" else m['o']
            st.session_state.moedas += rec
            for n, d in st.session_state.missoes_ativas.items():
                if m['n'] in d['p']: d['p'][m['n']] = min(d['a'][m['n']], d['p'][m['n']] + 1)
            st.session_state.em_combate = False; st.rerun()
        else:
            st.session_state.vida -= m['d']; st.rerun()
    
    if st.button("Cura 🧪") and st.session_state.pocoes > 0:
        v_c = 60 if st.session_state.classe == "Paladino 🛡️" else 40
        st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + v_c); st.session_state.pocoes -= 1; st.rerun()
    
    if st.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas += 5; st.session_state.pocoes_furia -= 1; st.rerun()

# --- VILA (COM O MAGO) ---
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3, t4, t5 = st.tabs(["📜 Missões", "⚔️ Armas", "🛡️ Armaduras", "🧪 Alquimia", "🧙 Mago das Classes"])
    
    with t5:
        st.write("### O Mago Ancião")
        st.write("Escolha uma especialização para mudar seus atributos!")
        classes_info = {
            "Guerreiro ⚔️": "Buff: +15 HP Máximo inicial.",
            "Mago 🧙": "Buff: Fúria muito mais poderosa (2.5x dano).",
            "Ladino 🗡️": "Buff: Maior sorte para achar Vilas e Dungeons.",
            "Paladino 🛡️": "Buff: Poções de Cura recuperam mais vida.",
            "Bárbaro 🪓": "Buff: +5 de Dano fixo em todas as armas.",
            "Arqueiro 🏹": "Buff: Chance de acerto crítico (Dano 2x).",
            "Clérigo ⛪": "Buff: Recupera 5 de HP toda rodada de combate.",
            "Mercador 💰": "Buff: Ganha 50% a mais de ouro dos monstros."
        }
        for nome_cl, desc_cl in classes_info.items():
            col_cl1, col_cl2 = st.columns([1, 3])
            if col_cl1.button(f"Tornar-se {nome_cl}"):
                st.session_state.classe = nome_cl
                # Ajuste de HP se virar Guerreiro
                if nome_cl == "Guerreiro ⚔️": 
                    st.session_state.vida_max = 115 + st.session_state.armadura['bonus']
                else:
                    st.session_state.vida_max = 100 + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max
                st.success(f"Agora você é um {nome_cl}!")
                st.rerun()
            col_cl2.write(desc_cl)

    with t1:
        if st.button("🏹 Caçar Monstros ao Redor"): spawn(); st.rerun()
        miss = [{"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 25}, {"i": "REI", "de": "Mate o REI DRAGÃO", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500}]
        for x in miss:
            if x['i'] not in st.session_state.missoes_ativas:
                if st.button(f"Missão de {x['i']}: {x['de']}"):
                    st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}; st.rerun()
            else:
                at = st.session_state.missoes_ativas[x['i']]
                if all(at['p'][k] >= at['a'][k] for k in at['a']) and st.button(f"Entregar para {x['i']} ✅"):
                    st.session_state.moedas += at['pago']; del st.session_state.missoes_ativas[x['i']]; st.rerun()

    with t2:
        loja_w = {"Ferro ⚔️": (250, 14), "Rei Caído 💀": (3500, 50)}
        for n, (c, d) in loja_w.items():
            if st.button(f"{n} ({d} D) - {c}💰") and st.session_state.moedas >= c:
                st.session_state.moedas -= c; st.session_state.espada = {"nome": n, "dano": d}; st.rerun()

    with t3:
        loja_a = {"Ferro ⚙️": (200, 25), "Rei Caído 💀": (1500, 100)}
        for n, (c, b) in loja_a.items():
            if st.button(f"Armadura {n} (+{b} HP) - {c}💰") and st.session_state.moedas >= c:
                st.session_state.moedas -= c; st.session_state.armadura = {"nome": n, "bonus": b}
                st.session_state.vida_max = (115 if st.session_state.classe == "Guerreiro ⚔️" else 100) + b
                st.session_state.vida = st.session_state.vida_max; st.rerun()

    with t4:
        if st.button("Poção Cura (35💰)") and st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes += 1; st.rerun()
        if st.button("Poção Fúria (45💰)") and st.session_state.moedas >= 45: st.session_state.moedas -= 45; st.session_state.pocoes_furia += 1; st.rerun()
    
    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

# --- MAPA ---
else:
    st.subheader("🗺️ Exploração")
    c1, c2 = st.columns(2)
    chance_mod = 2 if st.session_state.classe == "Ladino 🗡️" else 1
    if c1.button("Andar 🥾"):
        if random.randint(1, 100) <= (1 * chance_mod): st.session_state.dungeon_tipo = "COVIL DO REI DRAGÃO 👑"; st.session_state.em_dungeon = True
        elif random.randint(1, 4 // chance_mod) == 1: st.session_state.achou_vila = True
        elif random.randint(1, 15 // chance_mod) == 1: st.session_state.dungeon_tipo = "Monstros"; st.session_state.em_dungeon = True
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()

    if st.session_state.em_dungeon:
        st.warning(f"📍 Dungeon Avistada!")
        if st.button("ENTRAR!"): spawn(); st.rerun()
        if st.button("Ignorar"): st.session_state.em_dungeon = False; st.rerun()
    if st.session_state.achou_vila:
        st.success("🏘️ Vila avistada!")
        if st.button("Entrar na Vila"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
