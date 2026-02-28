import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

# --- SISTEMA DE SAVE/LOAD ---
def export_save():
    save_data = {k: v for k, v in st.session_state.items() if k not in ['log']}
    return json.dumps(save_data)

def import_save(uploaded_file):
    if uploaded_file:
        data = json.load(uploaded_file)
        st.session_state.update(data)
        st.rerun()

# --- INICIALIZAÇÃO ---
if 'nome' not in st.session_state:
    st.title("🐲 Bem-vindo a Ravenwood")
    nome_temp = st.text_input("Como os bardos devem chamar o herói?", placeholder="Digite seu nome...")
    if st.button("Iniciar Jornada ⚔️"):
        if nome_temp:
            st.session_state.update({
                'nome': nome_temp, 'vida': 100, 'moedas': 20, 'pocoes': 2, 
                'pocoes_furia': 0, 'furia_rodadas': 0,
                'espada': {"nome": "Madeira 🪵", "dano": 7},
                'em_combate': False, 'monstro': None, 'na_vila': False, 
                'achou_vila': False, 'log': [f"{nome_temp} inicia sua jornada!"],
                'missoes_ativas': {}, 'concluidas': [],
                'em_dungeon': False, 'dungeon_tipo': None, 'dungeon_progresso': 0
            })
            st.rerun()
        else:
            st.warning("Um herói precisa de um nome!")
    
    st.write("---")
    uploaded = st.file_uploader("Já tem um save? Carregue aqui:", type="json")
    if uploaded:
        import_save(uploaded)
    st.stop()

# --- FUNÇÕES DE APOIO ---
def add_log(txt):
    st.session_state.log.append(txt)

def spawn(tipo_nome=None):
    m_list = {
        "Gosma 🟢": {"n": "Gosma 🟢", "v": 30, "d": 4, "o": 15},
        "Goblin 👺": {"n": "Goblin 👺", "v": 50, "d": 9, "o": 30},
        "Dragão 🐲": {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 60}
    }
    if tipo_nome:
        st.session_state.monstro = m_list[tipo_nome].copy()
    else:
        st.session_state.monstro = random.choice(list(m_list.values())).copy()
    st.session_state.em_combate = True

# --- UI SIDEBAR ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome}")
    st.write(f"❤️ Vida: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    
    # MOEDAS COM DESTAQUE (Texto escuro em fundo amarelo para leitura)
    st.markdown(f"""
        <div style="background-color: #FFD700; padding: 10px; border-radius: 5px; text-align: center;">
            <span style="color: #000000; font-weight: bold; font-size: 20px;">💰 Moedas: {st.session_state.moedas}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 Fúria: {st.session_state.furia_rodadas} rodadas")

    if st.session_state.em_dungeon:
        st.info(f"🏰 Dungeon: {st.session_state.dungeon_tipo} ({st.session_state.dungeon_progresso}/7)")

    st.write("---")
    # BOTÕES DE SAVE/RESET
    st.download_button("💾 Baixar Save Game", data=export_save(), file_name=f"save_{st.session_state.nome}.json", mime="application/json")
    
    if st.button("🔄 Reiniciar Tudo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA DE TELAS ---
st.title(f"🐲 Dragões e Espadas: A Saga de {st.session_state.nome}")

# [O restante da lógica de Combate, Dungeon e Vila permanece igual à anterior]
# (Para economizar espaço, a lógica de combate e exploração segue o padrão da sua última versão)

if st.session_state.vida <= 0:
    st.error("💀 VOCÊ FOI DERROTADO!")
    if st.button("Pagar Resgate (50 💰)"):
        st.session_state.moedas -= 50; st.session_state.vida = 100; st.session_state.em_combate = False; st.rerun()
    if st.button("Sair"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    d_at = int(st.session_state.espada['dano'] * (1.7 if st.session_state.furia_rodadas > 0 else 1))
    
    col1, col2 = st.columns(2)
    col1.metric("HP Monstro", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    if st.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            if st.session_state.em_dungeon:
                st.session_state.dungeon_progresso += 1
                if st.session_state.dungeon_progresso >= 7:
                    premios = {"Gosmas (Fácil)": 200, "Goblins (Médio)": 450, "Dragões (Difícil)": 800}
                    st.session_state.moedas += premios.get(st.session_state.dungeon_tipo, 0)
                    st.session_state.em_dungeon = False
                    st.session_state.em_combate = False
                    add_log("DUNGEON CONCLUÍDA!")
                else: spawn(m['n'])
            else: st.session_state.em_combate = False
            st.rerun()
        else:
            st.session_state.vida -= m['d']
            st.rerun()
    
    if st.button("Usar Poção de Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(100, st.session_state.vida + 40); st.session_state.pocoes -= 1; st.rerun()

# [Exploração e Vila aqui...]
else:
    st.subheader("🗺️ O que deseja fazer?")
    c1, c2 = st.columns(2)
    if c1.button("Explorar (Andar) 🥾"):
        sorte = random.randint(1, 100)
        if random.randint(1, 5) == 1: st.session_state.achou_vila = True
        elif sorte <= 2: st.session_state.dungeon_tipo = "Dragões (Difícil)"; st.session_state.em_dungeon = True
        elif sorte <= 16: st.session_state.dungeon_tipo = "Gosmas (Fácil)"; st.session_state.em_dungeon = True
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.achou_vila:
        if st.button("Entrar na Vila"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()

st.write("---")
for m in reversed(st.session_state.log[-3:]): st.write(m)
