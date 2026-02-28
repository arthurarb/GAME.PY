import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Arthur's World", layout="wide")

# Inicializar o estado do jogo
if 'pos_x' not in st.session_state:
    st.session_state.pos_x = 5
    st.session_state.pos_y = 5
    st.session_state.inventario = {"Madeira": 0, "Pedra": 0}
    st.session_state.log = ["Bem-vindo ao mundo aberto!"]

st.title("🌳 Arthur's Open World")

# Sidebar para o Inventário
st.sidebar.header("🎒 Inventário")
for item, qtd in st.session_state.inventario.items():
    st.sidebar.write(f"{item}: {qtd}")

# Área Principal - O que o jogador vê
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Localização Atual: ({st.session_state.pos_x}, {st.session_state.pos_y})")
    
    # Simulação de bioma baseada em sorte
    bioma = "Floresta" if (st.session_state.pos_x + st.session_state.pos_y) % 2 == 0 else "Caverna"
    st.info(f"Você está em uma **{bioma}**.")

    # Controles de Movimento
    st.write("### Para onde ir?")
    c1, c2, c3 = st.columns(3)
    with c2:
        if st.button("⬆️ Norte"): st.session_state.pos_y += 1
    with c1:
        if st.button("⬅️ Oeste"): st.session_state.pos_x -= 1
    with c3:
        if st.button("➡️ Leste"): st.session_state.pos_x += 1
    with c2:
        if st.button("⬇️ Sul"): st.session_state.pos_y -= 1

with col2:
    st.subheader("⛏️ Ações")
    if bioma == "Floresta":
        if st.button("Cortar Árvore"):
            st.session_state.inventario["Madeira"] += 1
            st.session_state.log.append("+1 Madeira coletada!")
    else:
        if st.button("Minar Pedra"):
            st.session_state.inventario["Pedra"] += 1
            st.session_state.log.append("+1 Pedra coletada!")

# Log de Aventuras
st.write("---")
st.subheader("📜 Diário de Bordo")
for entrada in reversed(st.session_state.log[-5:]):
    st.write(entrada)
    
