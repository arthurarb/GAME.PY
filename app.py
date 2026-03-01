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
                'nome_heroi': nome, 'classe': "Nenhuma 👤", 'vida_max': 100, 'vida': 100, 'moedas': 20, 
                'pocoes': 2, 'pocoes_furia': 0, 'furia_rodadas': 0,
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

# --- SIDEBAR E PAINEL ADMIN COMPLETO ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.caption(f"Classe: {st.session_state.classe}")
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
    
    with st.expander("🔐 Painel do Dono"):
        senha = st.text_input("Senha Admin", type="password")
        if senha == "05062012":
            if st.button("💰 Dinheiro Infinito"): st.session_state.moedas += 99999; st.rerun()
            if st.button("🧪 Kit Poções (99)"): st.session_state.pocoes = 99; st.session_state.pocoes_furia = 99; st.rerun()
            if st.button("❤️ VIDA INFINITA"): st.session_state.vida_max = 9999999; st.session_state.vida = 9999999; st.rerun()
            if st.button("🏘️ Spawnar Vila Agora"): st.session_state.achou_vila = True; st.rerun()
            
            st.write("🏰 Spawnar Dungeon:")
            dungs_adm = ["Gosmas (Fácil)", "Goblins (Médio)", "Dragões (Difícil)", "COVIL DO REI DRAGÃO 👑"]
            sel_dung = st.selectbox("Escolher Dungeon:", dungs_adm, key="adm_d")
            if st.button("Spawnar Dungeon"):
                st.session_state.dungeon_tipo = sel_dung; st.session_state.em_dungeon = True; st.rerun()

            st.write("👾 Spawnar Monstro:")
            esc_m = st.selectbox("Escolher Monstro:", ["Gosma 🟢", "Goblin 👺", "Dragão 🐲", "🔥 REI DRAGÃO 🔥", "🌌 DRAGÃO DEUS 🌌"])
            if st.button("Spawnar Monstro"): spawn(esc_m); st.rerun()

            st.write("⚔️ Trocar Equipamento:")
            armas_adm = {"Madeira 🪵": 7, "Pedra 🪨": 10, "Ferro ⚔️": 14, "Ouro 👑": 18, "Cavaleiro 🛡️": 22, "Rei Caído 💀": 50, "CRIADOR ⚡": 9999}
            sel_arma = st.selectbox("Armas:", list(armas_adm.keys()), key="adm_w")
            if st.button("Equipar Arma"): st.session_state.espada = {"nome": sel_arma, "dano": armas_adm[sel_arma]}; st.rerun()

            arms_adm = {"Madeira 🪵": 0, "Couro 🪵": 10, "Ferro ⚙️": 25, "Ouro 👑": 50, "Cavaleiro 🛡️": 75, "Rei Caído 💀": 100, "DEUS DA GUERRA 🛡️": 99999}
            sel_arm = st.selectbox("Armaduras:", list(arms_adm.keys()), key="adm_a")
            if st.button("Equipar Armadura"):
                st.session_state.armadura = {"nome": sel_arm, "bonus": arms_adm[sel_arm]}
                st.session_state.vida_max = (115 if st.session_state.classe == "Guerreiro ⚔️" else 100) + arms_adm[sel_arm]
                st.session_state.vida = st.session_state.vida_max; st.rerun()

    if st.button("🔄 Reset Total"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA DE BATALHA ---
if st.session_state.vida <= 0:
    st.error("💀 VOCÊ MORREU!")
    if st.button("Pagar Resgate (50 💰) e Renascer (25 HP)"):
        if st.session_state.moedas >= 50: st.session_state.moedas -= 50; st.session_state.vida = 25; st.session_state.em_combate = False; st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    
    # Buffs de Classe
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
    
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if st.session_state.classe == "Clérigo ⛪": st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + 5)
        if m['v'] <= 0:
            rec = int(m['o'] * 1.5) if st.session_state.classe == "Mercador 💰" else m['o']
            st.session_state.moedas += rec
            for npc, d in st.session_state.missoes_ativas.items():
                if m['n'] in d['p']: d['p'][m['n']] = min(d['a'][m['n']], d['p'][m['n']] + 1)
            st.session_state.em_dungeon = False; st.session_state.em_combate = False; st.rerun()
        else:
            st.session_state.vida -= m['d']; st.rerun()
    
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        v_c = 60 if st.session_state.classe == "Paladino 🛡️" else 40
        st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + v_c); st.session_state.pocoes -= 1; st.rerun()
    
    if b3.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas += 5; st.session_state.pocoes_furia -= 1; st.rerun()
    
    if b4.button("FUGIR 🏃"): st.session_state.em_combate = False; st.rerun()

# --- VILA (COM MAGO E TODAS MISSÕES) ---
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    tabs = st.tabs(["📜 Missões", "⚔️ Armas", "🛡️ Armaduras", "🧪 Alquimia", "🧙 Mago"])
    
    with tabs[4]:
        st.write("### Mago das Classes")
        classes_info = {
            "Guerreiro ⚔️": "Buff: +15 HP Máximo inicial.",
            "Mago 🧙": "Buff: Fúria poderosa (2.5x).",
            "Ladino 🗡️": "Buff: Sorte em achar vilas/dungeons.",
            "Paladino 🛡️": "Buff: Cura melhorada.",
            "Bárbaro 🪓": "Buff: +5 Dano fixo.",
            "Arqueiro 🏹": "Buff: 20% Chance de Crítico (2x).",
            "Clérigo ⛪": "Buff: Regenera 5 HP por turno.",
            "Mercador 💰": "Buff: +50% Ouro de monstros."
        }
        for n_cl, d_cl in classes_info.items():
            col_m1, col_m2 = st.columns([1, 2])
            if col_m1.button(f"Ser {n_cl}"):
                st.session_state.classe = n_cl
                st.session_state.vida_max = (115 if n_cl == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max; st.rerun()
            col_m2.write(d_cl)

    with tabs[0]:
        if st.button("🏹 Caçar Monstros ao Redor"): spawn(); st.rerun()
        st.write("---")
        miss = [
            {"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 25},
            {"i": "Silas", "de": "5 Gosmas", "a": {"Gosma 🟢": 5}, "p": 40},
            {"i": "Maria", "de": "3 Goblins", "a": {"Goblin 👺": 3}, "p": 70},
            {"i": "Bram", "de": "5 Gobs e 3 Gosmas", "a": {"Goblin 👺": 5, "Gosma 🟢": 3}, "p": 120},
            {"i": "Elara", "de": "1 Dragão", "a": {"Dragão 🐲": 1}, "p": 150},
            {"i": "REI", "de": "Mate o REI DRAGÃO", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500}
        ]
        for x in miss:
            if x['i'] not in st.session_state.missoes_ativas:
                if st.button(f"Missão de {x['i']}: {x['de']}"):
                    st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}; st.rerun()
            else:
                at = st.session_state.missoes_ativas[x['i']]
                if all(at['p'][k] >= at['a'][k] for k in at['a']) and st.button(f"Entregar para {x['i']} ✅"):
                    st.session_state.moedas += at['pago']; del st.session_state.missoes_ativas[x['i']]; st.rerun()

    with tabs[1]:
        loja_w = {"Pedra 🪨": (150, 10), "Ferro ⚔️": (250, 14), "Ouro 👑": (400, 18), "Cavaleiro 🛡️": (1000, 22), "Rei Caído 💀": (3500, 50)}
        for n, (c, d) in loja_w.items():
            if st.button(f"{n} ({d} D) - {c}💰") and st.session_state.moedas >= c:
                st.session_state.moedas -= c; st.session_state.espada = {"nome": n, "dano": d}; st.rerun()

    with tabs[2]:
        loja_a = {"Couro 🪵": (100, 10), "Ferro ⚙️": (200, 25), "Ouro 👑": (400, 50), "Cavaleiro 🛡️": (800, 75), "Rei Caído 💀": (1500, 100)}
        for n, (c, b) in loja_a.items():
            if st.button(f"Armadura {n} (+{b} HP) - {c}💰") and st.session_state.moedas >= c:
                st.session_state.moedas -= c; st.session_state.armadura = {"nome": n, "bonus": b}
                st.session_state.vida_max = (115 if st.session_state.classe == "Guerreiro ⚔️" else 100) + b
                st.session_state.vida = st.session_state.vida_max; st.rerun()

    with tabs[3]:
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
        elif random.randint(1, 25 // chance_mod) == 1: st.session_state.dungeon_tipo = "Dragões (Difícil)"; st.session_state.em_dungeon = True
        elif random.randint(1, 15 // chance_mod) == 1: st.session_state.dungeon_tipo = "Goblins (Médio)"; st.session_state.em_dungeon = True
        elif random.randint(1, 10 // chance_mod) == 1: st.session_state.dungeon_tipo = "Gosmas (Fácil)"; st.session_state.em_dungeon = True
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()

    if st.session_state.em_dungeon:
        st.warning(f"📍 Dungeon Avistada: {st.session_state.dungeon_tipo}")
        if st.button("ENTRAR! ⚔️"):
            if "REI" in st.session_state.dungeon_tipo: spawn("🔥 REI DRAGÃO 🔥")
            elif "Dragão" in st.session_state.dungeon_tipo: spawn("Dragão 🐲")
            elif "Goblin" in st.session_state.dungeon_tipo: spawn("Goblin 👺")
            else: spawn("Gosma 🟢")
            st.rerun()
        if st.button("Ignorar Dungeon"): st.session_state.em_dungeon = False; st.rerun()
    if st.session_state.achou_vila:
        st.success("🏘️ Vila avistada!")
        if st.button("Entrar na Vila 🚪"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if st.button("Ignorar Vila 🚶"): st.session_state.achou_vila = False; st.rerun()state.achou_vila = False; st.rerun()
