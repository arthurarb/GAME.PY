import streamlit as st

# 1. Configuração de Estilo (Deixa a tela mais larga)
st.set_page_config(layout="wide")

# 2. Inicialização do Jogador
if 'local' not in st.session_state:
    st.session_state.local = "Vila Inicial"
    st.session_state.hp = 100

st.title(f"🏰 Aventura do Arthur: {st.session_state.local}")

# 3. Layout em Colunas (Interface de App)
col_img, col_status = st.columns([2, 1])

with col_img:
    # Aqui você coloca a imagem do cenário ou do personagem
    # Se você tiver a imagem no GitHub, o caminho seria "assets/cenario.jpg"
    st.image("https://via.placeholder.com/600x300.png?text=Imagem+do+Cenario", 
             caption="Você está explorando as terras desconhecidas")

with col_status:
    st.subheader("📊 Status do Herói")
    st.progress(st.session_state.hp / 100) # Barra de vida visual
    st.write(f"❤️ Vida: {st.session_state.hp}")
    
    st.subheader("🎒 Mochila")
    st.write("⚔️ Espada de Madeira")

# 4. Botões de Interface (O "Controle")
st.write("---")
st.subheader("O que você deseja fazer?")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Ir para a Floresta"):
        st.session_state.local = "Floresta Sombria"
        st.rerun()

with c2:
    if st.button("Descansar (Recuperar Vida)"):
        st.session_state.hp = min(100, st.session_state.hp + 10)
        st.success("Você descansou!")

with c3:
    if st.button("Falar com o Velho Sábio"):
        st.info("O Sábio diz: 'O Streamlit é poderoso para RPGs!'")
        
