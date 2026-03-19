import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

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
                'nome_heroi': nome, 'classe': "Nenhuma 👤", 'vezes_mudou_classe': 0, 'vida_max': 100, 'vida': 100, 'moedas': 20, 
                'pocoes': 2, 'pocoes_furia': 0, 'furia_rodadas': 0,
                'espada': {"nome": "Madeira 🪵", "dano": 7},
                'armadura': {"nome": "Madeira 🪵", "bonus": 0},
                'em_combate': False, 'monstro': None, 'na_vila': False,
                'achou_vila': False, 'log': [f"{nome} iniciou a jornada!"],
                'missoes_ativas': {}, 'em_dungeon': False, 'dungeon_tipo': None
            })
            st.rerun()
    st.stop()

if 'vezes_mudou_classe' not in st.session_state: st.session_state.vezes_mudou_classe = 0

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

# --- SIDEBAR E PAINEL ADMIN ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.success(f"Classe: {st.session_state.classe}")
    st.write(f"❤️ HP: {st.session_state.vida} / {st.session_state.vida_max}")
    st.progress(max(0.0, min(1.0, st.session_state.vida / st.session_state.vida_max)) if st.session_state.vida_max > 0 else 0.0)
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    st.write(f"🗡️ Arma: {st.session_state.espada['nome']} | 🛡️ Armadura: {st.session_state.armadura['nome']}")
    st.markdown(f"### 💰 {st.session_state.moedas} Moedas")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 FÚRIA ATIVA: {st.session_state.furia_rodadas} rodadas!")

    if st.session_state.missoes_ativas:
        st.subheader("📜 Missões")
        for npc, dados in list(st.session_state.missoes_ativas.items()):
            prog = ", ".join([f"{k}: {dados['p'][k]}/{dados['a'][k]}" for k in dados['a']])
            st.write(f"**{npc}**: {prog}")

    with st.expander("🔐 Painel do Dono"):
        senha = st.text_input("Senha Admin", type="password")
        if senha == "arthur.arb2012adm":
            if st.button("💰 Dinheiro Infinito"): st.session_state.moedas += 999999; st.rerun()
            if st.button("🧪 Kit Poções (99)"): st.session_state.pocoes = 99; st.session_state.pocoes_furia = 99; st.rerun()
            if st.button("❤️ VIDA INFINITA"): st.session_state.vida_max = 999999; st.session_state.vida = 999999; st.rerun()
            
            st.write("✨ Classes:")
            lista_cl = ["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰", "ADM ⚡"]
            sel_cl = st.selectbox("Escolher Classe:", lista_cl)
            if st.button("Equipar Classe"):
                st.session_state.classe = sel_cl
                st.session_state.vida_max = 100000 if sel_cl == "ADM ⚡" else (115 if sel_cl == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max; st.rerun()

            st.write("👾 Monstros:")
            m_list = ["Gosma 🟢", "Goblin 👺", "Dragão 🐲", "🔥 REI DRAGÃO 🔥", "🌌 DRAGÃO DEUS 🌌"]
            esc_m = st.selectbox("Spawnar:", m_list)
            if st.button("Spawnar Monstro"): spawn(esc_m); st.rerun()

            st.write("🏰 Dungeons:")
            d_list = ["Gosmas (Fácil)", "Goblins (Médio)", "Dragões (Difícil)", "COVIL DO REI DRAGÃO 👑"]
            esc_d = st.selectbox("Escolher Dungeon:", d_list)
            if st.button("Spawnar Dungeon"):
                st.session_state.dungeon_tipo = esc_d
                st.session_state.em_dungeon = True
                st.rerun()

            st.write("⚔️ Equipamento:")
            w_list = {"Madeira 🪵": 7, "Pedra 🪨": 10, "Ferro ⚔️": 14, "Ouro 👑": 18, "Cavaleiro 🛡️": 22, "Rei Caído 💀": 50, "CRIADOR ⚡": 99999}
            sel_w = st.selectbox("Armas:", list(w_list.keys()))
            if st.button("Equipar Arma"): st.session_state.espada = {"nome": sel_w, "dano": w_list[sel_w]}; st.rerun()

            a_list = {"Madeira 🪵": 0, "Couro 🪵": 10, "Ferro ⚙️": 25, "Ouro 👑": 50, "Cavaleiro 🛡️": 75, "Rei Caído 💀": 100, "DEUS DA GUERRA 🛡️": 99999}
            sel_a = st.selectbox("Armaduras:", list(a_list.keys()))
            if st.button("Equipar Armadura"):
                st.session_state.armadura = {"nome": sel_a, "bonus": a_list[sel_a]}
                st.session_state.vida_max = (115 if st.session_state.classe == "Guerreiro ⚔️" else 100) + a_list[sel_a]
                st.session_state.vida = st.session_state.vida_max; st.rerun()

    if st.button("🔄 Reset Total"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name="save_dragao.json")

# --- LÓGICA DE JOGO ---
if st.session_state.vida <= 0:
    st.error("💀 VOCÊ MORREU!")
    if st.button("Pagar Resgate (50 💰)"):
        if st.session_state.moedas >= 50: st.session_state.moedas -= 50; st.session_state.vida = 25; st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    
    if st.session_state.furia_rodadas > 0:
        st.info(f"⚡ Fúria ativa por mais {st.session_state.furia_rodadas} rodadas!")

    d_base = st.session_state.espada['dano']
    if st.session_state.classe == "Bárbaro 🪓": d_base += 5
    mult = 2.5 if (st.session_state.furia_rodadas > 0 and st.session_state.classe == "Mago 🧙") else (1.7 if st.session_state.furia_rodadas > 0 else 1.0)
    d_at = int(d_base * mult)
    if st.session_state.classe == "ADM ⚡": d_at *= 11
    if st.session_state.classe == "Arqueiro 🏹" and random.random() < 0.2: d_at *= 2; st.warning("🎯 CRÍTICO!")
    
    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    b1, b2, b3, b4, b5 = st.columns(5)
    if b1.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if st.session_state.classe == "Clérigo ⛪": st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + 5)
        if m['v'] <= 0:
            rec = m['o']
            if st.session_state.classe == "Mercador 💰": rec = int(rec * 1.5)
            if st.session_state.classe == "ADM ⚡": rec *= 11
            st.session_state.moedas += int(rec)
            for n, d in st.session_state.missoes_ativas.items():
                if m['n'] in d['p']: d['p'][m['n']] = min(d['a'][m['n']], d['p'][m['n']] + 1)
            st.session_state.em_combate = False; st.session_state.em_dungeon = False; st.rerun()
        else:
            st.session_state.vida -= m['d']; st.rerun()
    
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        v_c = 60 if st.session_state.classe == "Paladino 🛡️" else 40
        st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + v_c); st.session_state.pocoes -= 1; st.rerun()

    if b3.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas += 3
        st.session_state.pocoes_furia -= 1
        st.rerun()

    if b4.button("FUGIR 🏃"):
        st.session_state.em_combate = False
        st.session_state.em_dungeon = False
        st.warning("Você fugiu da batalha!")
        st.rerun()

elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3, t4, t5 = st.tabs(["📜 Missões", "⚔️ Armas", "🛡️ Armaduras", "🧪 Alquimia", "🧙 Mago"])
    
    with t5:
        st.write("### Mago das Classes")
        st.info("Primeira vez: 50💰 | Próximas: 450💰 (Aleatório)")
        st.write("- **Guerreiro**: +15 HP | **Mago**: Fúria 2.5x | **Ladino**: Sorte | **Paladino**: Cura + | **Bárbaro**: +5 Dano | **Arqueiro**: Crítico | **Clérigo**: Regen | **Mercador**: +Ouro")
        custo = 50 if st.session_state.vezes_mudou_classe == 0 else 450
        if st.button(f"🔮 Ritual ({custo} 💰)"):
            if st.session_state.moedas >= custo:
                st.session_state.moedas -= custo; st.session_state.vezes_mudou_classe += 1
                nova = random.choice(["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰"])
                st.session_state.classe = nova
                st.session_state.vida_max = (115 if nova == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max; st.rerun()

    with t1:
        if st.button("🏹 Caçar Monstros ao Redor"): spawn(); st.rerun()
        st.write("---")
        miss = [{"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 25}, {"i": "Silas", "de": "5 Gosmas", "a": {"Gosma 🟢": 5}, "p": 40}, {"i": "Maria", "de": "3 Goblins", "a": {"Goblin 👺": 3}, "p": 70}, {"i": "Bram", "de": "5 Gobs e 3 Gosmas", "a": {"Goblin 👺": 5, "Gosma 🟢": 3}, "p": 120}, {"i": "Elara", "de": "1 Dragão", "a": {"Dragão 🐲": 1}, "p": 150}, {"i": "REI", "de": "Mate o REI DRAGÃO", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500}]
        for x in miss:
            if x['i'] not in st.session_state.missoes_ativas:
                if st.button(f"Aceitar {x['i']}: {x['de']}"):
                    st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}; st.rerun()
            else:
                at = st.session_state.missoes_ativas[x['i']]
                if all(at['p'][k] >= at['a'][k] for k in at['a']) and st.button(f"Entregar Missão {x['i']} ✅"):
                    st.session_state.moedas += at['pago']; del st.session_state.missoes_ativas[x['i']]; st.rerun()

    with t2:
        l_w = {"Pedra 🪨": (150, 10), "Ferro ⚔️": (250, 14), "Ouro 👑": (400, 18), "Cavaleiro 🛡️": (1000, 22), "Rei Caído 💀": (3500, 50)}
        for n, (c, d) in l_w.items():
            if st.button(f"{n} ({d} D) - {c}💰"):
                if st.session_state.moedas >= c: st.session_state.moedas -= c; st.session_state.espada = {"nome": n, "dano": d}; st.rerun()

    with t3:
        l_a = {"Couro 🪵": (100, 10), "Ferro ⚙️": (200, 25), "Ouro 👑": (400, 50), "Cavaleiro 🛡️": (800, 75), "Rei Caído 💀": (3000, 100)}
        for n, (c, b) in l_a.items():
            if st.button(f"{n} (+{b} HP) - {c}💰"):
                if st.session_state.moedas >= c:
                    st.session_state.moedas -= c; st.session_state.armadura = {"nome": n, "bonus": b}
                    st.session_state.vida_max = (115 if st.session_state.classe == "Guerreiro ⚔️" else 100) + b
                    st.session_state.vida = st.session_state.vida_max; st.rerun()

    with t4:
        if st.button("Cura (35💰)"): 
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes += 1; st.rerun()
        if st.button("Fúria (45💰)"):
            if st.session_state.moedas >= 45: st.session_state.moedas -= 45; st.session_state.pocoes_furia += 1; st.rerun()

    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

else:
    st.subheader("🗺️ Exploração")
    prob = 75 if st.session_state.classe == "ADM ⚡" else (2 if st.session_state.classe == "Ladino 🗡️" else 1)
    c1, c2 = st.columns(2)
    if c1.button("Andar 🥾"):
        roll = random.randint(1, 100)
        if roll <= prob: 
            st.session_state.dungeon_tipo = random.choice(["Gosmas (Fácil)", "Goblins (Médio)", "Dragões (Difícil)", "COVIL DO REI DRAGÃO 👑"])
            st.session_state.em_dungeon = True
        elif random.randint(1, 5) == 1: st.session_state.achou_vila = True
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.em_dungeon:
        st.warning(f"📍 Dungeon Avistada: {st.session_state.dungeon_tipo}")
        if st.button("ENTRAR!"): 
            if "REI" in st.session_state.dungeon_tipo: spawn("🔥 REI DRAGÃO 🔥")
            elif "Dragão" in st.session_state.dungeon_tipo: spawn("Dragão 🐲")
            elif "Goblin" in st.session_state.dungeon_tipo: spawn("Goblin 👺")
            else: spawn("Gosma 🟢")
            st.rerun()
        if st.button("Ignorar Dungeon"): st.session_state.em_dungeon = False; st.rerun()
    
    if st.session_state.achou_vila:
        st.success("🏘️ Vila avistada!")
        if st.button("Entrar"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if st.button("Ignorar Vila"): st.session_state.achou_vila = False; st.rerun()
