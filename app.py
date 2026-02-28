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

# --- INICIALIZAÇÃO E TELA DE NOME ---
if 'nome_heroi' not in st.session_state:
    st.title("🐲 Dragões e Espadas")
    st.subheader("Bem-vindo ao Reino")
    
    nome = st.text_input("Qual o nome do herói?", placeholder="Digite seu nome...")
    
    col_ini1, col_ini2 = st.columns(2)
    with col_ini1:
        if st.button("Iniciar Nova Jornada ⚔️"):
            if nome:
                st.session_state.update({
                    'nome_heroi': nome, 'vida': 100, 'moedas': 20, 'pocoes': 2,
                    'pocoes_furia': 0, 'furia_rodadas': 0,
                    'espada': {"nome": "Madeira 🪵", "dano": 7},
                    'em_combate': False, 'monstro': None, 'na_vila': False,
                    'achou_vila': False, 'log': [f"{nome} iniciou a jornada!"],
                    'missoes_ativas': {}, 'concluidas': [],
                    'em_dungeon': False, 'dungeon_tipo': None, 'dungeon_progresso': 0
                })
                st.rerun()
            else:
                st.error("O herói precisa de um nome!")
    with col_ini2:
        uploaded_file = st.file_uploader("Carregar Save (.json)", type="json")
        if uploaded_file:
            carregar_save(uploaded_file)
    st.stop()

# --- FUNÇÕES DE APOIO ---
def add_log(txt):
    st.session_state.log.append(txt)

def spawn(tipo_nome=None, boss=False):
    if boss:
        st.session_state.monstro = {"n": "🔥 REI DRAGÃO 🔥", "v": 500, "d": 17, "o": 500}
    elif tipo_nome:
        m_list = {
            "Gosma 🟢": {"n": "Gosma 🟢", "v": 30, "d": 4, "o": 15},
            "Goblin 👺": {"n": "Goblin 👺", "v": 50, "d": 9, "o": 30},
            "Dragão 🐲": {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 60}
        }
        st.session_state.monstro = m_list[tipo_nome].copy()
    else:
        m = [{"n": "Gosma 🟢", "v": 30, "d": 4, "o": 15}, 
             {"n": "Goblin 👺", "v": 50, "d": 9, "o": 30},
             {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 60}]
        st.session_state.monstro = random.choice(m).copy()
    st.session_state.em_combate = True

# --- SIDEBAR ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.write(f"❤️ HP: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    
    st.markdown(f"""
        <div style="background-color: #FFD700; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #B8860B;">
            <span style="color: #000000; font-weight: bold; font-size: 20px;">💰 {st.session_state.moedas} Moedas</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 Fúria: {st.session_state.furia_rodadas} rds restantes")

    if st.session_state.em_dungeon:
        st.info(f"🏰 Dungeon: {st.session_state.dungeon_tipo}\nProgresso: {st.session_state.dungeon_progresso}/7")

    st.write("---")
    st.header("📜 Missões")
    if not st.session_state.missoes_ativas:
        st.write("Sem missões.")
    else:
        for npc, dados in st.session_state.missoes_ativas.items():
            for m_nome, alvo in dados['a'].items():
                st.write(f"{npc}: {m_nome} ({dados['p'][m_nome]}/{alvo})")

    st.write("---")
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name=f"save_{st.session_state.nome_heroi}.json", mime="application/json")
    if st.button("🔄 Reiniciar Tudo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA DE TELAS ---
st.title("🐲 Dragões e Espadas")

# 1. MORTE
if st.session_state.vida <= 0:
    st.error(f"💀 {st.session_state.nome_heroi} foi derrotado!")
    if st.button("Pagar Resgate (50 💰)"):
        st.session_state.moedas -= 50; st.session_state.vida = 100; st.session_state.em_combate = False; st.rerun()
    if st.button("Novo Jogo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# 2. COMBATE
elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    d_at = int(st.session_state.espada['dano'] * (1.7 if st.session_state.furia_rodadas > 0 else 1))
    
    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    b1, b2, b3 = st.columns(3)
    if b1.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            # Progresso de Missões
            for npc, dados in st.session_state.missoes_ativas.items():
                if m['n'] in dados['p']:
                    dados['p'][m['n']] = min(dados['a'][m['n']], dados['p'][m['n']] + 1)
            
            if st.session_state.em_dungeon:
                st.session_state.dungeon_progresso += 1
                if st.session_state.dungeon_progresso >= 7:
                    premios = {"Gosmas (Fácil)": 200, "Goblins (Médio)": 450, "Dragões (Difícil)": 800}
                    st.session_state.moedas += premios.get(st.session_state.dungeon_tipo, 0)
                    st.session_state.em_dungeon = False; st.session_state.em_combate = False
                    add_log("🏰 DUNGEON CONCLUÍDA!")
                else: spawn(m['n'])
            else: st.session_state.em_combate = False
            st.rerun()
        else:
            st.session_state.vida -= m['d']
            st.rerun()
    if b2.button("Cura 🧪"):
        if st.session_state.pocoes > 0:
            st.session_state.vida = min(100, st.session_state.vida + 40); st.session_state.pocoes -= 1; st.rerun()
    if b3.button("Fúria ⚡"):
        if st.session_state.pocoes_furia > 0:
            st.session_state.furia_rodadas = 3; st.session_state.pocoes_furia -= 1; st.rerun()

# 3. VILA
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila de Ravenwood")
    t1, t2, t3 = st.tabs(["📜 Missões", "⚒️ Ferreiro", "🧪 Alquimista"])
    
    with t1:
        miss = [
            {"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 15},
            {"i": "Maria", "de": "3 Goblins", "a": {"Goblin 👺": 3}, "p": 45},
            {"i": "REI", "de": "Derrotar o REI DRAGÃO", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500}
        ]
        for x in miss:
            if x['i'] not in st.session_state.concluidas:
                if x['i'] not in st.session_state.missoes_ativas:
                    if st.button(f"Aceitar missão de {x['i']}"):
                        st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}
                        if x['i'] == "REI": spawn(boss=True)
                        st.rerun()
                else:
                    at = st.session_state.missoes_ativas[x['i']]
                    if all(at['p'][k] >= at['a'][k] for k in at['a']):
                        if st.button(f"Entregar missão para {x['i']} ✅"):
                            st.session_state.moedas += at['pago']
                            st.session_state.concluidas.append(x['i'])
                            del st.session_state.missoes_ativas[x['i']]; st.rerun()
    
    with t2:
        espadas = {"Pedra 🪨": (150, 10), "Ferro ⚔️": (250, 14), "Ouro 👑": (400, 18), "Rei Caído 💀": (3500, 50)}
        for nome_e, (preco, dano_e) in espadas.items():
            if st.button(f"{nome_e} ({dano_e} Dano) - {preco}💰"):
                if st.session_state.moedas >= preco:
                    st.session_state.moedas -= preco; st.session_state.espada = {"nome": nome_e, "dano": dano_e}; st.rerun()
    
    with t3:
        if st.button("Poção Cura (35💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes += 1; st.rerun()
        if st.button("Poção Fúria (35💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes_furia += 1; st.rerun()
            
    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

# 4. EXPLORAÇÃO
else:
    st.subheader("🗺️ Onde o herói irá agora?")
    c1, c2 = st.columns(2)
    if c1.button("Andar 🥾"):
        sorte = random.randint(1, 100)
        if random.randint(1, 5) == 1: st.session_state.achou_vila = True
        elif sorte <= 2: st.session_state.dungeon_tipo = "Dragões (Difícil)"; st.session_state.em_dungeon = True
        elif sorte <= 16: st.session_state.dungeon_tipo = "Gosmas (Fácil)"; st.session_state.em_dungeon = True
        else: add_log("Nada além de grama no horizonte.")
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.em_dungeon:
        st.warning(f"🏰 Dungeon: {st.session_state.dungeon_tipo}")
        if st.button("ENTRAR (7 Monstros)"):
            st.session_state.dungeon_progresso = 0
            spawn("Gosma 🟢" if "Gosma" in st.session_state.dungeon_tipo else "Dragão 🐲"); st.rerun()
        if st.button("Ignorar"): st.session_state.em_dungeon = False; st.rerun()

    if st.session_state.achou_vila:
        st.success("🏘️ Vila avistada!")
        if st.button("Entrar na Vila"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()

st.write("---")
for log in reversed(st.session_state.log[-5:]): st.write(log)
