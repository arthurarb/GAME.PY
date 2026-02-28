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
        'missoes_concluidas': []
    })

def add_log(texto):
    st.session_state.log.append(texto)

# --- TABELA DE ESPADAS ---
loja_espadas = {
    "Pedra 🪨": {"custo": 150, "dano": 10},
    "Ferro ⚔️": {"custo": 250, "dano": 14},
    "Ouro 👑": {"custo": 400, "dano": 18},
    "Cavaleiro 🛡️": {"custo": 750, "dano": 22},
    "Rei Caído 💀": {"custo": 3500, "dano": 50}
}

# --- FUNÇÕES DE COMBATE ---
def iniciar_combate(tipo="normal"):
    if tipo == "boss":
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
    st.header("📜 Missões")
    if not st.session_state.missoes_ativas:
        st.write("Nenhuma missão aceita.")
    for m_nome, m_info in st.session_state.missoes_ativas.items():
        st.write(f"**{m_nome}**")
        for alvo, qtd in m_info['alvos'].items():
            st.write(f"- {alvo}: {m_info['progresso'][alvo]}/{qtd}")
    if st.button("Reiniciar Jogo"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- LÓGICA DE TELAS ---
if st.session_state.vida <= 0:
    st.error("💀 Você foi derrotado!")
    if st.button("Renascer"):
        st.session_state.vida = 100
        st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro_atual
    st.subheader(f"⚔️ Lutando contra {m['nome']}")
    c1, c2 = st.columns(2)
    c1.metric("HP do Monstro", f"{m['vida']}")
    c2.metric("Seu HP", f"{st.session_state.vida}")
    col1, col2, col3 = st.columns(3)
    if col1.button("Atacar! ⚔️"):
        dano_a = st.session_state.espada['dano']
        m['vida'] -= dano_a
        if m['vida'] <= 0:
            st.session_state.moedas += m['ouro']
            add_log(f"Vitória! +{m['ouro']} moedas.")
            for m_nome, m_info in st.session_state.missoes_ativas.items():
                if m['nome'] in m_info['progresso']:
                    if m_info['progresso'][m['nome']] < m_info['alvos'][m['nome']]:
                        m_info['progresso'][m['nome']] += 1
            st.session_state.em_combate = False
        else:
            dano_m = m['dano']
            st.session_state.vida -= dano_m
            add_log(f"O {m['nome']} tirou {dano_m} de vida!")
        st.rerun()
    if col2.button("Poção 🧪"):
        if st.session_state.pocoes > 0:
            st.session_state.vida = min(100, st.session_state.vida + 40)
            st.session_state.pocoes -= 1
            st.rerun()
    if col3.button("Fugir 🏃"):
        st.session_state.em_combate =
