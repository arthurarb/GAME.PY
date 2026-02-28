import streamlit as st
import random

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'vida' not in st.session_state:
    st.session_state.update({
        'vida': 100, 'moedas': 20, 'pocoes': 2,
        'espada': {"nome": "Madeira 🪵", "dano": 7},
        'em_combate': False, 'monstro_atual': None,
        'na_vila': False, 'achou_vila': False,
        'log': ["O jovem Arthur inicia sua jornada!"],
        'missoes_ativas': {}, 
        'missoes_concluidas': [] # Para rastrear missões únicas (como a do Rei)
    })

def add_log(texto):
    st.session_state.log.append(texto)

# --- TABELA DE ESPADAS ---
loja_espadas = {
    "Pedra 🪨": {"custo": 150, "dano": 10},
    "Ferro ⚔️": {"custo": 250, "dano": 14},
    "Ouro 👑": {"custo": 400, "dano": 18},
    "Cavaleiro 🛡️": {"custo": 750, "dano": 22},
    "Rei Caído 💀": {"custo": 3500, "dano": 50} # Preço atualizado para 3500
}

# --- FUNÇÕES DE COMBATE ---
def iniciar_combate(tipo="normal"):
    if tipo == "boss":
        # Vida do Rei atualizada para 500
        st.session_state.monstro_atual = {"nome": "🔥 REI DOS DRAGÕES 🔥", "vida": 500, "dano": 17, "ouro": 500}
        add_log("😱 O CÉU ESCURECEU! O REI DOS DRAGÕES APARECEU!")
    else:
        monstros = [
            {"nome": "Gosma 🟢", "vida": 30, "dano": 5, "ouro": 15},
            {"nome": "Goblin 👺", "vida": 50, "dano": 12, "ouro": 30},
            {"nome": "Dragão Jovem 🐲", "vida": 80, "dano": 18, "ouro": 60}
        ]
        st.session_state.monstro_atual = random.choice(monstros)
        add_log(f"⚠️ Um {st.session_state.monstro_atual['nome']} apareceu!")
    st.session_state.em_combate = True

# --- INTERFACE ---
st.title("🐲 Dragões e Espadas")

with st.sidebar:
    st.header("👤 Status")
    st.write(f"❤️ Vida: {st.session_state.vida}/100")
    st.progress(max(0, st.session_state.vida / 100))
    st.write(f"💰 Moedas: {st.session_state.moedas}")
    st.write(f"🗡️ Arma: {st.session_state.espada['nome']}")
    st.write(f"🧪 Poções: {st.session_state.pocoes}")
    
    st.write("---")
    st.header("📜 Missões Ativas")
    if not st.session_state.missoes_ativas:
        st.write("Nenhuma missão
