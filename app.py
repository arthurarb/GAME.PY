import streamlit as st
import random

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'vida' not in st.session_state:
    st.session_state.update({
        'vida': 100, 'moedas': 20, 'nivel': 1, 'pocoes': 2,
        'espada': {"nome": "Madeira 🪵", "dano": 7},
        'em_combate': False, 'monstro_atual': None,
        'na_vila': False, 'log': ["O jovem Arthur inicia sua jornada!"]
    })

def add_log(texto):
    st.session_state.log.append(texto)

# --- TABELA DE ESPADAS (FERREIRO) ---
loja_espadas = {
    "Pedra 🪨": {"custo": 150, "dano": 10},
    "Ferro ⚔️": {"custo": 250, "dano": 14},
    "Ouro 👑": {"custo": 400, "dano": 18},
    "Cavaleiro 🛡️": {"custo": 750, "dano": 22},
    "Rei Caído 💀": {"custo": 2000, "dano": 50}
}

# --- FUNÇÕES DE COMBATE ---
def iniciar_combate(tipo="normal"):
    if tipo == "boss":
        st.session_state.monstro_atual = {"nome": "🔥 REI DOS DRAGÕES 🔥", "vida": 300, "dano": 17, "ouro": 1000}
        add_log("😱 O CÉU ESCURECEU! O REI DOS DRAGÕES APARECEU PARA DESTRUIR A VILA!")
    else:
        monstros = [
            {"nome": "Slime 🟢", "vida": 30, "dano": 5, "ouro": 15},
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
    st.write(f"🗡️ Arma: {st.session_state.espada['nome']} (Dano: {st.session_state.espada['dano']})")
    st.write(f"🧪 Poções: {st.session_state.pocoes}")
    if st.button("Reiniciar Jogo"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- LÓGICA DE TELAS ---

# 1. MORTE
if st.session_state.vida <= 0:
    st.error("💀 Você foi derrotado!")
    if st.button("Renascer"):
        st.session_state.vida = 100
        st.rerun()

# 2. COMBATE
elif st.session_state.em_combate:
    m = st.session_state.monstro_atual
    st.subheader(f"⚔️ Lutando contra {m['nome']}")
    col1, col2 = st.columns(2)
    col1.metric("HP do Monstro", f"{m['vida']}")
    col2.metric("Seu HP", f"{st.session_state.vida}")

    c1, c2, c3 = st.columns(3)
    if c1.button("Atacar! ⚔️"):
        dano_a = st.session_state.espada['dano']
        m['vida'] -= dano_a
        add_log(f"Você causou {dano_a} de dano!")
        if m['vida'] <= 0:
            st.session_state.moedas += m['ouro']
            add_log(f"Vitória! +{m['ouro']} moedas.")
            st.session_state.em_combate = False
        else:
            dano_m = m['dano']
            st.session_state.vida -= dano_m
            add_log(f"O {m['nome']} tirou {dano_m} de vida sua!")
        st.rerun()
    
    if c2.button("Poção 🧪"):
        if st.session_state.pocoes > 0:
            st.session_state.vida = min(100, st.session_state.vida + 40)
            st.session_state.pocoes -= 1
            add_log("Você usou uma poção!")
            st.rerun()
            
    if c3.button("Fugir 🏃"):
        st.session_state.em_combate = False
        add_log("Você fugiu da luta!")
        st.rerun()

# 3. NA VILA
elif st.session_state.na_vila:
    st.subheader("🏘️ Bem-vindo à Vila")
    tab1, tab2 = st.tabs(["👨‍🌾 Aldeões", "🔨 Ferreiro"])
    
    with tab1:
        if st.button("Falar com Aldeões"):
            if random.randint(1, 100) == 1: # 1 em 100 chance de Boss
                iniciar_combate(tipo="boss")
            else:
                st.info("Eles te deram uma missão!")
                if random.random() > 0.5:
                    st.session_state.moedas += 50
                    add_log("Missão cumprida! +50 moedas.")
                else:
                    add_log("A missão falhou...")
            st.rerun()

    with tab2:
        for nome, info in loja_espadas.items():
            if st.button(f"Comprar Espada de {nome} ({info['custo']} 💰)"):
                if st.session_state.moedas >= info['custo']:
                    st.session_state.moedas -= info['custo']
                    st.session_state.espada = {"nome": nome, "dano": info['dano']}
                    st.success(f"Agora você tem a espada de {nome}!")
                else: st.error("Você não tem dinheiro!")

    if st.button("Sair da Vila 🚪"):
        st.session_state.na_vila = False
        st.rerun()

# 4. EXPLORANDO
else:
    st.subheader("🗺️ O que deseja fazer?")
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        if st.button("Explorar o Mapa 🥾"):
            if random.randint(1, 5) == 1: # 1 em 5 chance de achar vila
                st.session_state.achou_vila = True
            else:
                add_log("Você andou mas não encontrou nada.")
            st.rerun()

    with col_exp2:
        if st.button("Procurar Monstros 👾"):
            if random.randint(1, 3) == 1: # 1 em 3 chance de monstro
                iniciar_combate()
            else:
                add_log("Não há monstros por aqui.")
            st.rerun()

    if st.get('achou_vila'):
        st.success("🏘️ Você avistou uma vila ao longe!")
        if st.button("Entrar na Vila"):
            st.session_state.na_vila = True
            st.session_state.achou_vila = False
            st.rerun()
        if st.button("Ignorar Vila"):
            st.session_state.achou_vila = False
            st.rerun()

# DIÁRIO
st.write("---")
for msg in reversed(st.session_state.log[-5:]):
    st.write(msg)
