import streamlit as st

# Configurações do Mundo
LARGURA = 7
ALTURA = 5

if 'pos' not in st.session_state:
    st.session_state.pos = [2, 3] # [X, Y]

st.title("🕹️ Arthur's Adventure 2D")

# Criando o Mapa Visual
mundo = ""
for y in range(ALTURA):
    linha = ""
    for x in range(LARGURA):
        if [x, y] == st.session_state.pos:
            linha += "👤" # Personagem do Arthur
        elif y == 0 or y == ALTURA-1 or x == 0 or x == LARGURA-1:
            linha += "🧱" # Paredes/Bordas
        else:
            linha += "🟩" # Grama
    mundo += linha + "\n"

# Exibe o jogo com fonte grande (estilo retro)
st.code(mundo, language="")

# Controles de Direção
st.write("Use os botões para mover seu personagem:")
col1, col2, col3 = st.columns([1,1,1])

with col2:
    if st.button("🔼"): st.session_state.pos[1] -= 1
with col1:
    if st.button("◀️"): st.session_state.pos[0] -= 1
with col3:
    if st.button("▶️"): st.session_state.pos[0] += 1
with col2:
    if st.button("🔽"): st.session_state.pos[1] += 1

# Limites do mapa (para não fugir da tela)
st.session_state.pos[0] = max(1, min(st.session_state.pos[0], LARGURA-2))
st.session_state.pos[1] = max(1, min(st.session_state.pos[1], ALTURA-2))
