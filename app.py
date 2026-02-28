import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas - ADMIN", page_icon="🐲", layout="wide")

# --- SISTEMA DE SAVE/LOAD ---
def export_save():
    dados = {k: v for k, v in st.session_state.items() if k not in ['log']}
    return json.dumps(dados, indent=4)

def carregar_save(arquivo):
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.update(dados)
        st.rerun()

# --- INICIALIZAÇÃO ---
if 'nome_heroi' not in st.session_state:
    st.title("🐲 Dragões e Espadas")
    nome = st.text_input("Nome do herói:", placeholder="Ex: Arthur")
    
    c_ini1, c_ini2 = st.columns(2)
    with c_ini1:
        if st.button("Iniciar Nova Jornada ⚔️"):
            if nome:
                st.session_state.update({
                    'nome_heroi': nome, 'vida': 100, 'moedas': 20, 'pocoes': 2,
                    'pocoes_furia': 0, 'furia_rodadas': 0,
                    'espada': {"nome": "Madeira 🪵", "dano": 7},
                    'em_combate': False, 'monstro': None, 'na_vila': False,
                    'achou_vila': False, 'log': [f"{nome} iniciou a jornada!"],
                    'missoes_ativas': {}, 'concluidas': [],
                    'em_dungeon': False, 'dungeon_tipo': None, 'dungeon_progresso': 0
                })
                st.rerun()
    with c_ini2:
        up = st.file_uploader("Carregar Save (.json)", type="json")
        if up: carregar_save(up)
    st.stop()

# --- FUNÇÕES ---
def add_log(txt): st.session_state.log.append(txt)

def spawn(tipo_nome=None, boss=False):
    m_data = {
        "Gosma 🟢": {"n": "Gosma 🟢", "v": 30, "d": 4, "o": 5},
        "Goblin 👺": {"n": "Goblin 👺", "v": 50, "d": 9, "o": 10},
        "Dragão 🐲": {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 30}
    }
    if boss: st.session_state.monstro = {"n": "🔥 REI DRAGÃO 🔥", "v": 500, "d": 17, "o": 500}
    elif tipo_nome: st.session_state.monstro = m_data[tipo_nome].copy()
    else: st.session_state.monstro = random.choice(list(m_data.values())).copy()
    st.session_state.em_combate = True

# --- SIDEBAR E PAINEL ADMIN ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.write(f"❤️ HP: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    st.markdown(f"<div style='background-color:#FFD700;padding:10px;border-radius:10px;text-align:center;border:2px solid #B8860B;'><span style='color:#000;font-weight:bold;font-size:20px;'>💰 {st.session_state.moedas} Moedas</span></div>", unsafe_allow_html=True)
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    st.write("---")
    with st.expander("🔐 Acesso Admin"):
        senha = st.text_input("Senha Admin", type="password")
        if senha == "admin123":
            st.success("Painel do Dono Ativo")
            if st.button("💰 +9999 Moedas"): 
                st.session_state.moedas += 9999; st.rerun()
            if st.button("❤️ HP Infinito (999)"): 
                st.session_state.vida = 999; st.rerun()
            if st.button("🧪 99 Poções"): 
                st.session_state.pocoes = 99; st.session_state.pocoes_furia = 99; st.rerun()
            
            st.write("🗡️ Pegar Espada:")
            espada_adm = st.selectbox("Escolha:", ["Cavaleiro 🛡️", "Rei Caído 💀"])
            if st.button("Equipar"):
                if "Cavaleiro" in espada_adm: st.session_state.espada = {"nome": "Cavaleiro 🛡️", "dano": 22}
                else: st.session_state.espada = {"nome": "Rei Caído 💀", "dano": 50}
                st.rerun()
            
            st.write("👾 Invocar Monstro:")
            monst_adm = st.selectbox("Escolha:", ["Gosma 🟢", "Goblin 👺", "Dragão 🐲", "REI DRAGÃO"])
            if st.button("Spawn Agora"):
                if monst_adm == "REI DRAGÃO": spawn(boss=True)
                else: spawn(monst_adm)
                st.rerun()
    
    st.write("---")
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name=f"save_{st.session_state.nome_heroi}.json")
    if st.button("🔄 Reiniciar Tudo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA PRINCIPAL ---
st.title("🐲 Dragões e Espadas")

if st.session_state.vida <= 0:
    st.error("💀 DERROTADO!")
    if st.button("Pagar Resgate (50 💰) e Renascer (25 HP)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50; st.session_state.vida = 25; st.session_state.em_combate = False; st.rerun()
    if st.button("Novo Jogo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    d_at = int(st.session_state.espada['dano'] * (1.7 if st.session_state.furia_rodadas > 0 else 1))
    
    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            for npc, dados in st.session_state.missoes_ativas.items():
                if m['n'] in dados['p']: dados['p'][m['n']] = min(dados['a'][m['n']], dados['p'][m['n']] + 1)
            st.session_state.em_combate = False; st.rerun()
        else: st.session_state.vida -= m['d']; st.rerun()
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(999, st.session_state.vida + 40); st.session_state.pocoes -= 1; st.rerun()
    if b3.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas = 3; st.session_state.pocoes_furia -= 1; st.rerun()
    if b4.button("FUGIR 🏃"):
        st.session_state.em_combate = False; st.rerun()

elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3 = st.tabs(["📜 Missões", "⚒️ Ferreiro", "🧪 Alquimia"])
    with t1:
        if st.button("Procurar monstros ao redor 👾"): spawn(); st.rerun()
        st.write("---")
        miss = [
            {"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 25},
            {"i": "Silas", "de": "5 Gosmas", "a": {"Gosma 🟢": 5}, "p": 40},
            {"i": "Maria", "de": "3 Goblins", "a": {"Goblin 👺": 3}, "p": 70},
            {"i": "Bram", "de": "5 Gobs e 3 Gosmas", "a": {"Goblin 👺": 5, "Gosma 🟢": 3}, "p": 120},
            {"i": "Elara", "de": "1 Dragão", "a": {"Dragão 🐲": 1}, "p": 150},
            {"i": "REI", "de": "Derrotar o REI DRAGÃO", "a": {"🔥 REI
