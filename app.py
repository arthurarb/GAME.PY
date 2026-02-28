import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Arthur's RPG", page_icon="⚔️")

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if 'vida' not in st.session_state:
    st.session_state.vida = 100
if 'moedas' not in st.session_state:
    st.session_state.moedas = 20
if 'inventario' not in st.session_state:
    st.session_state.inventario = []
if 'log' not in st.session_state:
    st.session_state.log = ["O despertar: Você acorda em uma terra mística..."]

# --- FUNÇÕES DO JOGO ---
def adicionar_log(texto):
    st.session_state.log.append(texto)

def reset_jogo():
    st.session_state.vida = 100
    st.session_state.moedas = 20
    st.session_state.inventario = []
    st.session_state.log = ["O jogo recomeçou!"]

# --- INTERFACE LATERAL (STATUS) ---
st.sidebar.title("👤 Status do Herói")
st.sidebar.subheader(f"Vida: {st.session_state.vida} ❤️")
st.sidebar.progress(max(0, min(st.session_state.vida, 100)))
st.sidebar.subheader(f"Moedas: {st.session_state.moedas} 💰")
st.sidebar.write("---")
st.sidebar.write("🎒 **Inventário:**")
if not st.session_state.inventario:
    st.sidebar.write("Vazio")
for item in st.session_state.inventario:
    st.sidebar.write(f"- {item}")

if st.sidebar.button("Reiniciar Jogo"):
    reset_jogo()
    st.rerun()

# --- TELA PRINCIPAL ---
st.title("⚔️ Aventura de Emojis")

if st.session_state.vida <= 0:
    st.error("💀 Você foi derrotado! Que pena...")
    if st.button("Tentar Novamente"):
        reset_jogo()
        st.rerun()
else:
    # Divisão da tela
    col_historia, col_loja = st.columns([2, 1])

    with col_historia:
        st.subheader("📖 O que você faz?")
        
        # Sistema de Perguntas/Caminhos
        escolha = st.radio("Escolha seu caminho:", 
                          ["Explorar a Floresta 🌲", "Entrar na Caverna Escura 🕳️", "Procurar por Monstros 👾"])

        if st.button("Confirmar Ação"):
            sorte = random.randint(1, 10)
            
            if escolha == "Explorar a Floresta 🌲":
                if sorte > 3:
                    ganho = random.randint(5, 15)
                    st.session_state.moedas += ganho
                    adicionar_log(f"🌲 Você explorou a floresta e achou {ganho} moedas!")
                else:
                    dano = random.randint(10, 20)
                    st.session_state.vida -= dano
                    adicionar_log(f"🐝 Você foi picado por abelhas! -{dano} de vida.")

            elif escolha == "Entrar na Caverna Escura 🕳️":
                if sorte > 6:
                    st.session_state.moedas += 50
                    adicionar_log("💎 Tesouro! Você achou um diamante de 50 moedas!")
                else:
                    st.session_state.vida -= 30
                    adicionar_log("🦇 Morcegos te atacaram na caverna! -30 de vida.")

            elif escolha == "Procurar por Monstros 👾":
                monstros = [("Slime 🟢", 10, 10), ("Goblin 👺", 20, 25), ("Dragão 🐲", 50, 100)]
                m_nome, m_dano, m_recompensa = random.choice(monstros)
                st.session_state.vida -= m_dano
                st.session_state.moedas += m_recompensa
                adicionar_log(f"⚔️ Lutou com {m_nome}! Perdeu {m_dano} HP, ganhou {m_recompensa} moedas.")

    with col_loja:
        st.subheader("🛒 Loja da Vila")
        if st.button("Poção de Cura (15 💰)"):
            if st.session_state.moedas >= 15:
                st.session_state.moedas -= 15
                st.session_state.vida = min(100, st.session_state.vida + 30)
                st.success("❤️ +30 de Vida!")
            else:
                st.error("Dinheiro insuficiente!")

        if st.button("Espada de Ferro (40 💰)"):
            if st.session_state.moedas >= 40 and "Espada de Ferro" not in st.session_state.inventario:
                st.session_state.moedas -= 40
                st.session_state.inventario.append("Espada de Ferro")
                st.success("⚔️ Você comprou uma Espada!")
            else:
                st.warning("Já possui ou sem dinheiro.")

    # Exibição do Diário (Log)
    st.write("---")
    st.subheader("📜 Diário de Aventuras")
    for msg in reversed(st.session_state.log[-5:]):
        st.write(msg)
        
