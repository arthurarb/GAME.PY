import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

# --- SISTEMA DE PERSISTÊNCIA ---
def export_save():
    # Coleta os dados atuais para salvar
    dados = {k: v for k, v in st.session_state.items() if k not in ['log']}
    return json.dumps(dados, indent=4)

def carregar_save(arquivo):
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.update(dados)
        st.rerun()

# --- TELA INICIAL (NOME E LOAD) ---
if 'nome_heroi' not in st.session_state:
    st.title("🐲 Dragões e Espadas")
    st.subheader("O início de uma grande jornada")
    
    nome = st.text_input("Qual o nome do herói?", placeholder="Ex: Arthur")
    
    col_ini1, col_ini2 = st.columns(2)
    with col_ini1:
        if st.button("Iniciar Nova Jornada ⚔️"):
            if nome:
                st.session_state.update({
                    'nome_heroi': nome, 'vida': 100, 'moedas': 20, 'pocoes': 2,
                    'pocoes_furia': 0, 'furia_rodadas': 0,
                    'espada': {"nome": "Madeira 🪵", "dano": 7},
                    'em_combate': False, 'monstro': None, 'na_vila': False,
                    'achou_vila': False, 'log': [f"{nome} entrou no mundo de Dragões e Espadas!"],
                    'missoes_ativas': {}, 'concluidas': [],
                    'em_dungeon': False, 'dungeon_tipo': None, 'dungeon_progresso': 0
                })
                st.rerun()
            else:
                st.error("Por favor, digite um nome para começar.")
                
    with col_ini2:
        uploaded_file = st.file_uploader("Carregar Progresso Antigo", type="json")
        if uploaded_file:
            carregar_save(uploaded_file)
    st.stop()

# --- FUNÇÕES DE JOGO ---
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

# --- SIDEBAR (STATUS E SALVAMENTO) ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.write(f"❤️ HP: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    
    # MOEDAS COM DESTAQUE VISUAL
    st.markdown(f"""
        <div style="background-color: #FFD700; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #B8860B;">
            <span style="color: #000000; font-weight: bold; font-size: 24px;">💰 {st.session_state.moedas} Moedas</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 Fúria Ativa: {st.session_state.furia_rodadas} rds")

    st.write("---")
    # BOTÃO SIMPLES DE SALVAR
    st.download_button(
        label="💾 SALVAR JOGO",
        data=export_save(),
        file_name=f"save_{st.session_state.nome_heroi}.json",
        mime="application/json",
        help="Baixa o arquivo de progresso para carregar depois."
    )
    
    if st.button("🔄 Reiniciar Jogo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA DE TELAS ---
st.title("🐲 Dragões e Espadas")

# O restante da lógica de combate, dungeons de 7 monstros e exploração segue aqui...
# (O código continua com as funções de batalha e dungeons que criamos anteriormente)
