import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

# --- SISTEMA DE PERSISTÊNCIA ---
def export_save():
    dados = {k: v for k, v in st.session_state.items() if k not in ['log']}
    return json.dumps(dados, indent=4)

def carregar_save(arquivo):
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.update(dados)
        st.rerun()

# --- INICIALIZAÇÃO E TELA DE NOME ---
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
                st.error("Digite um nome para começar.")
    with col_ini2:
        uploaded_file = st.file_uploader("Carregar Progresso (.json)", type="json")
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

# --- SIDEBAR ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.write(f"❤️ HP: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    
    # Moedas em Destaque
    st.markdown(f"""
        <div style="background-color: #FFD700; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #B8860B;">
            <span style="color: #000000; font-weight: bold; font-size: 20px;">💰 {st.session_state.moedas} Moedas</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 Fúria: {st.session_state.furia_rodadas} rodadas")

    st.write("---")
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name=f"save_{st.session_state.nome_heroi}.json", mime="application/json")
    if st.button("🔄 Reiniciar Tudo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA PRINCIPAL ---
st.title("🐲 Dragões e Espadas")

# 1. TELA DE MORTE
if st.session_state.vida <= 0:
    st.error(f"💀 {st.session_state.nome_heroi} foi derrotado!")
    if st.button("Pagar Resgate (50 💰)"):
        st.session_state.moedas -= 50; st.session_state.vida = 100; st.session_state.em_combate = False; st.rerun()
    if st.button("Reiniciar"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# 2. TELA DE COMBATE (Inclui Dungeon)
elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha contra {m['n']}")
    d_at = int(st.session_state.espada['dano'] * (1.7 if st.session_state.furia_rodadas > 0 else 1))
    
    c1, c2 = st.columns(2)
    c1.metric("HP Monstro", m['v'])
    c2.metric("Seu HP", st.session_state.vida)
    
    col_b1, col_b2, col_b3 = st.columns(3)
    if col_b1.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            if st.session_state.em_dungeon:
                st.session_state.dungeon_progresso += 1
                if st.session_state.dungeon_progresso >= 7:
                    premios = {"Gosmas (Fácil)": 200, "Goblins (Médio)": 450, "Dragões (Difícil)": 800}
                    st.session_state.moedas += premios.get(st.session_state.dungeon_tipo, 0)
                    st.session_state.em_dungeon = False; st.session_state.em_combate = False
                    add_log("DUNGEON CONCLUÍDA! Bônus recebido.")
                else: spawn(m['n'])
            else: st.session_state.em_combate = False
            st.rerun()
        else:
            st.session_state.vida -= m['d']
            st.rerun()
    if col_b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(100, st.session_state.vida + 40); st.session_state.pocoes -= 1; st.rerun()
    if col_b3.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas = 3; st.session_state.pocoes_furia -= 1; st.rerun()

# 3. TELA DA VILA
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila de Ravenwood")
    tab1, tab2 = st.tabs(["Ferreiro & Alquimia", "Sair"])
    with tab1:
        if st.button("Poção de Cura (35💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes += 1; st.rerun()
        if st.button("Poção de Fúria (35💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes_furia += 1; st.rerun()
    with tab2:
        if st.button("Voltar para a Estrada"): st.session_state.na_vila = False; st.rerun()

# 4. TELA DE EXPLORAÇÃO (Padrão)
else:
    st.subheader("🗺️ O que deseja fazer?")
    col_ex1, col_ex2 = st.columns(2)
    
    if col_ex1.button("Andar 🥾"):
        sorte = random.randint(1, 100)
        if random.randint(1, 5) == 1: 
            st.session_state.achou_vila = True
        elif sorte <= 2: 
            st.session_state.dungeon_tipo = "Dragões (Difícil)"; st.session_state.em_dungeon = True
        elif sorte <= 16: 
            st.session_state.dungeon_tipo = "Gosmas (Fácil)"; st.session_state.em_dungeon = True
        else: 
            add_log("Você andou um pouco pelas planícies.")
        st.rerun()
        
    if col_ex2.button("Lutar 👾"):
        spawn()
        st.rerun()
    
    if st.session_state.em_dungeon:
        st.warning(f"🏰 Dungeon Detectada: {st.session_state.dungeon_tipo}")
        if st.button("ENTRAR (7 Monstros)"):
            st.session_state.dungeon_progresso = 0
            tipo = "Gosma 🟢" if "Gosma" in st.session_state.dungeon_tipo else "Dragão 🐲"
            spawn(tipo); st.rerun()
        if st.button("Ignorar Dungeon"): st.session_state.em_dungeon = False; st.rerun()

    if st.session_state.achou_vila:
        st.success("🏘️ Você avistou uma Vila!")
        if st.button("Entrar na Vila"):
            st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if st.button("Continuar Andando"): st.session_state.achou_vila = False; st.rerun()

st.write("---")
for log in reversed(st.session_state.log[-5:]):
    st.write(log)
    
