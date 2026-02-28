import streamlit as st
import random

# Configuração Inicial
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲")

# --- ESTADO DO JOGO ---
if 'vida' not in st.session_state:
    st.session_state.update({
        'vida': 100, 'moedas': 20, 'nivel': 1, 'xp': 0,
        'pocoes': 2, 'em_combate': False, 'monstro_atual': None,
        'log': ["Bem-vindo ao reino de Dragões e Espadas!"]
    })

def add_log(texto):
    st.session_state.log.append(texto)

# --- SISTEMA DE COMBATE ---
def iniciar_combate():
    # Monstros ficam mais fortes conforme o nível do Arthur
    tipos = [
        {"nome": "Slime 🟢", "vida": 30 * st.session_state.nivel, "dano": 5, "ouro": 15},
        {"nome": "Goblin 👺", "vida": 50 * st.session_state.nivel, "dano": 12, "ouro": 30},
        {"nome": "Dragão 🐲", "vida": 100 * st.session_state.nivel, "dano": 25, "ouro": 100}
    ]
    st.session_state.monstro_atual = random.choice(tipos)
    st.session_state.em_combate = True
    add_log(f"⚠️ Um {st.session_state.monstro_atual['nome']} apareceu!")

# --- INTERFACE ---
st.title("🐲 Dragões e Espadas")

# Barra Lateral de Status
with st.sidebar:
    st.header("📊 Status do Arthur")
    st.write(f"⭐ Nível: {st.session_state.nivel}")
    st.write(f"❤️ Vida: {st.session_state.vida}/100")
    st.progress(max(0, st.session_state.vida / 100))
    st.write(f"💰 Moedas: {st.session_state.moedas}")
    st.write(f"🧪 Poções: {st.session_state.pocoes}")
    if st.button("Reiniciar Aventura"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# --- LÓGICA DE TELA ---
if st.session_state.vida <= 0:
    st.error("💀 Você caiu em batalha...")
    if st.button("Renascer"):
        st.session_state.vida = 100
        st.rerun()

elif not st.session_state.em_combate:
    st.subheader("📍 Estrada Segura")
    st.write("Você está caminhando pelo reino. O que deseja fazer?")
    if st.button("Procurar Perigo (Explorar)"):
        iniciar_combate()
        st.rerun()
    if st.button("Comprar Poção (20 💰)") and st.session_state.moedas >= 20:
        st.session_state.moedas -= 20
        st.session_state.pocoes += 1
        st.success("🧪 Você comprou uma poção!")

else:
    # TELA DE COMBATE
    m = st.session_state.monstro_atual
    st.subheader(f"⚔️ BATALHA: Arthur vs {m['nome']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Vida do Monstro", f"{m['vida']} HP")
    with col2:
        st.metric("Seu HP", f"{st.session_state.vida} HP")

    # AÇÕES DE TURNO
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("Atacar! ⚔️"):
            dano_arthur = random.randint(10, 20) + (st.session_state.nivel * 2)
            m['vida'] -= dano_arthur
            add_log(f"Você causou {dano_arthur} de dano!")
            
            if m['vida'] <= 0:
                st.session_state.moedas += m['ouro']
                st.session_state.xp += 1
                if st.session_state.xp >= 3:
                    st.session_state.nivel += 1
                    st.session_state.xp = 0
                    add_log("🌟 LEVEL UP! Você ficou mais forte!")
                add_log(f"✅ Vitória! Ganhou {m['ouro']} moedas.")
                st.session_state.em_combate = False
            else:
                dano_m = random.randint(1, m['dano'])
                st.session_state.vida -= dano_m
                add_log(f"O {m['nome']} revidou! -{dano_m} HP.")
            st.rerun()

    with c2:
        if st.button("Usar Poção 🧪"):
            if st.session_state.pocoes > 0:
                st.session_state.vida = min(100, st.session_state.vida + 40)
                st.session_state.pocoes -= 1
                add_log("🧪 Você usou uma poção e recuperou vida!")
                # Monstro ataca mesmo se você se curar!
                dano_m = random.randint(1, m['dano'])
                st.session_state.vida -= dano_m
                st.rerun()
            else:
                st.warning("Sem poções!")

    with c3:
        if st.button("Fugir! 🏃"):
            if random.random() > 0.3:
                add_log("💨 Você fugiu com sucesso!")
                st.session_state.em_combate = False
            else:
                dano_m = m['dano']
                st.session_state.vida -= dano_m
                add_log(f"Falhou em fugir! O {m['nome']} te acertou na corrida: -{dano_m} HP.")
            st.rerun()

# Exibir Log
st.write("---")
for msg in reversed(st.session_state.log[-5:]):
    st.write(msg)
    
    
