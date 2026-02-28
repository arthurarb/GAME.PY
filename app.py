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
    st.stop()

# --- FUNÇÕES ---
def add_log(txt): st.session_state.log.append(txt)

def spawn(tipo_nome=None, boss=False):
    m_data = {
        "Gosma 🟢": {"n": "Gosma 🟢", "v": 30, "d": 4, "o": 5},
        "Goblin 👺": {"n": "Goblin 👺", "v": 50, "d": 9, "o": 10},
        "Dragão 🐲": {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 30}
    }
    if boss: st.session_state.monstro = {"n": "🔥 REI DRAGÃO 🔥", "v": 500, "d": 25, "o": 500}
    elif tipo_nome: st.session_state.monstro = m_data[tipo_nome].copy()
    else: st.session_state.monstro = random.choice(list(m_data.values())).copy()
    st.session_state.em_combate = True

# --- SIDEBAR E PAINEL ADMIN ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.write(f"❤️ HP: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)) if st.session_state.vida <= 100 else 1.0)
    st.markdown(f"<div style='background-color:#FFD700;padding:10px;border-radius:10px;text-align:center;border:2px solid #B8860B;'><span style='color:#000;font-weight:bold;font-size:20px;'>💰 {st.session_state.moedas} Moedas</span></div>", unsafe_allow_html=True)
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    
    with st.expander("🔐 Painel do Dono"):
        senha = st.text_input("Senha Admin", type="password")
        if senha == "admin123":
            if st.button("💰 Dinheiro Infinito"): st.session_state.moedas += 99999; st.rerun()
            if st.button("❤️ HP Imortal"): st.session_state.vida = 9999; st.rerun()
            
            st.write("⚔️ Arsenal Completo:")
            todas_espadas = {
                "Madeira 🪵": 7, "Pedra 🪨": 10, "Ferro ⚔️": 14, 
                "Ouro 👑": 18, "Cavaleiro 🛡️": 22, "Rei Caído 💀": 50, "EXCALIBUR ✨": 150
            }
            esc_espada = st.selectbox("Escolher Arma:", list(todas_espadas.keys()))
            if st.button("Equipar Agora"):
                st.session_state.espada = {"nome": esc_espada, "dano": todas_espadas[esc_espada]}
                st.rerun()
            
            st.write("🏰 Invocador de Dungeons:")
            dungeons_lista = ["Gosmas (Fácil)", "Goblins (Médio)", "Dragões (Difícil)", "COVIL DO REI DRAGÃO 👑"]
            esc_dung = st.selectbox("Escolher Dungeon:", dungeons_lista)
            if st.button("Forçar Dungeon"):
                st.session_state.dungeon_tipo = esc_dung
                st.session_state.em_dungeon = True
                st.rerun()

    st.download_button("💾 SALVAR", data=export_save(), file_name="save.json")
    if st.button("🔄 Reset"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA DE BATALHA ---
if st.session_state.vida <= 0:
    st.error("💀 DERROTADO!")
    if st.button("Pagar Resgate (50 💰) e Renascer (25 HP)"):
        if st.session_state.moedas >= 50:
            st.session_state.moedas -= 50; st.session_state.vida = 25; st.session_state.em_combate = False; st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    d_at = int(st.session_state.espada['dano'] * (1.7 if st.session_state.furia_rodadas > 0 else 1))
    
    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    if st.button("ATACAR!"):
        m['v'] -= d_at
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            # Atualiza missões
            for npc, dados in st.session_state.missoes_ativas.items():
                if m['n'] in dados['p']: 
                    dados['p'][m['n']] = min(dados['a'][m['n']], dados['p'][m['n']] + 1)
            
            # Se matou o Rei Dragão
            if m['n'] == "🔥 REI DRAGÃO 🔥":
                add_log("VOCÊ MATOU O REI DRAGÃO! Volte à vila para falar com o Rei.")
                st.session_state.em_dungeon = False

            st.session_state.em_combate = False; st.rerun()
        else:
            st.session_state.vida -= m['d']; st.rerun()
    if st.button("FUGIR 🏃"):
        st.session_state.em_combate = False; st.rerun()

# --- VILA ---
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila Real")
    t1, t2, t3 = st.tabs(["📜 Missões", "⚒️ Ferreiro", "🧪 Alquimia"])
    with t1:
        miss = [
            {"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 25},
            {"i": "Bram", "de": "5 Gobs e 3 Gosmas", "a": {"Goblin 👺": 5, "Gosma 🟢": 3}, "p": 120},
            {"i": "REI", "de": "Encontre e mate o REI DRAGÃO no mundo", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500}
        ]
        for x in miss:
            if x['i'] not in st.session_state.missoes_ativas:
                if st.button(f"Falar com {x['i']}: {x['de']}"):
                    st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}
                    st.rerun()
            else:
                at = st.session_state.missoes_ativas[x['i']]
                if all(at['p'][k] >= at['a'][k] for k in at['a']):
                    if st.button(f"ENTREGAR MISSÃO PARA {x['i']} ✅"):
                        st.session_state.moedas += at['pago']
                        del st.session_state.missoes_ativas[x['i']]; st.rerun()
                else:
                    st.info(f"Em progresso: {x['de']}")

    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

# --- MAPA ---
else:
    st.subheader("🗺️ Explorando o Reino")
    c1, c2 = st.columns(2)
    if c1.button("Andar 🥾"):
        sorte = random.randint(1, 100)
        # 1% de chance para o Covil do Rei Dragão se a missão estiver ativa
        if sorte == 1 and "REI" in st.session_state.missoes_ativas:
            st.session_state.dungeon_tipo = "COVIL DO REI DRAGÃO 👑"
            st.session_state.em_dungeon = True
        elif sorte <= 5: st.session_state.achou_vila = True
        elif sorte <= 15: 
            st.session_state.dungeon_tipo = random.choice(["Gosmas (Fácil)", "Goblins (Médio)"])
            st.session_state.em_dungeon = True
        st.rerun()
    
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.em_dungeon:
        st.warning(f"📍 VOCÊ ACHOU: {st.session_state.dungeon_tipo}")
        if st.button("ENTRAR PARA LUTAR! ⚔️"):
            if "REI" in st.session_state.dungeon_tipo: spawn(boss=True)
            else: spawn() # Dungeon normal
            st.rerun()
        if st.button("Ignorar Dungeon"): st.session_state.em_dungeon = False; st.rerun()

    if st.session_state.achou_vila:
        st.success("🏘️ Vila avistada!")
        if st.button("Entrar"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if st.button("Ignorar"): st.session_state.achou_vila = False; st.rerun()

st.write("---")
for log in reversed(st.session_state.log[-5:]): st.write(log)
