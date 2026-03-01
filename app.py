import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas - FINAL ADM", page_icon="🐲", layout="wide")

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
    st.subheader("Retornar à Jornada")
    arquivo_save = st.file_uploader("Arraste seu arquivo .json aqui:", type=["json"])
    if arquivo_save and st.button("Confirmar Carregamento 📂"):
        carregar_save(arquivo_save)
    st.write("---")
    st.subheader("Nova Jornada")
    nome = st.text_input("Nome do novo herói:", placeholder="Ex: Arthur")
    if st.button("Iniciar Nova Jornada ⚔️"):
        if nome:
            st.session_state.update({
                'nome_heroi': nome, 'classe': "Nenhuma 👤", 'vezes_mudou_classe': 0, 'vida_max': 100, 'vida': 100, 'moedas': 20, 
                'pocoes': 2, 'pocoes_furia': 0, 'furia_rodadas': 0,
                'espada': {"nome": "Madeira 🪵", "dano": 7},
                'armadura': {"nome": "Madeira 🪵", "bonus": 0},
                'em_combate': False, 'monstro': None, 'na_vila': False,
                'achou_vila': False, 'log': [f"{nome} iniciou a jornada!"],
                'missoes_ativas': {}, 'em_dungeon': False, 'dungeon_tipo': None
            })
            st.rerun()
    st.stop()

if 'vezes_mudou_classe' not in st.session_state: st.session_state.vezes_mudou_classe = 0

# --- FUNÇÕES ---
def spawn(tipo_nome=None):
    m_data = {
        "Gosma 🟢": {"n": "Gosma 🟢", "v": 30, "d": 4, "o": 5},
        "Goblin 👺": {"n": "Goblin 👺", "v": 50, "d": 9, "o": 10},
        "Dragão 🐲": {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 30},
        "🔥 REI DRAGÃO 🔥": {"n": "🔥 REI DRAGÃO 🔥", "v": 500, "d": 25, "o": 500},
        "🌌 DRAGÃO DEUS 🌌": {"n": "🌌 DRAGÃO DEUS 🌌", "v": 9999, "d": 999, "o": 9999}
    }
    if tipo_nome and tipo_nome in m_data:
        st.session_state.monstro = m_data[tipo_nome].copy()
    else:
        st.session_state.monstro = m_data[random.choice(["Gosma 🟢", "Goblin 👺", "Dragão 🐲"])].copy()
    st.session_state.em_combate = True

# --- SIDEBAR E PAINEL ADMIN ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.success(f"Classe: {st.session_state.classe}")
    st.write(f"❤️ HP: {st.session_state.vida} / {st.session_state.vida_max}")
    st.progress(max(0.0, min(1.0, st.session_state.vida / st.session_state.vida_max)) if st.session_state.vida_max > 0 else 0.0)
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    st.write(f"🗡️ Arma: {st.session_state.espada['nome']} | 🛡️ Armadura: {st.session_state.armadura['nome']}")
    st.markdown(f"### 💰 {st.session_state.moedas} Moedas")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 FÚRIA ATIVA: {st.session_state.furia_rodadas} rodadas!")
    
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name="save_dragao.json")
    
    with st.expander("🔐 Painel do Dono"):
        senha = st.text_input("Senha Admin", type="password")
        if senha == "05062012":
            if st.button("⭐ VIRAR CLASSE ADM ⭐"):
                st.session_state.classe = "ADM ⚡"
                st.session_state.vida_max = 100000
                st.session_state.vida = 100000; st.rerun()
            
            if st.button("💰 Dinheiro Infinito"): st.session_state.moedas += 999999; st.rerun()
            if st.button("🧪 Kit Poções (99)"): st.session_state.pocoes = 99; st.session_state.pocoes_furia = 99; st.rerun()
            
            st.write("✨ Escolher Classe:")
            lista_classes_adm = ["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰", "ADM ⚡"]
            classe_escolhida_adm = st.selectbox("Selecione:", lista_classes_adm)
            if st.button("Equipar Classe"):
                st.session_state.classe = classe_escolhida_adm
                if classe_escolhida_adm == "ADM ⚡": st.session_state.vida_max = 100000
                else: st.session_state.vida_max = (115 if classe_escolhida_adm == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max; st.rerun()

            st.write("🏰 Spawnar Dungeon:")
            dungs_adm = ["Gosmas (Fácil)", "Goblins (Médio)", "Dragões (Difícil)", "COVIL DO REI DRAGÃO 👑"]
            sel_dung = st.selectbox("Dungeon:", dungs_adm, key="adm_d")
            if st.button("Spawnar Dungeon"):
                st.session_state.dungeon_tipo = sel_dung; st.session_state.em_dungeon = True; st.rerun()

            st.write("👾 Spawnar Monstro:")
            esc_m = st.selectbox("Monstro:", ["Gosma 🟢", "Goblin 👺", "Dragão 🐲", "🔥 REI DRAGÃO 🔥", "🌌 DRAGÃO DEUS 🌌"])
            if st.button("Spawnar Monstro"): spawn(esc_m); st.rerun()

            st.write("⚔️ Equipamentos:")
            armas_adm = {"Madeira 🪵": 7, "CRIADOR ⚡": 99999}
            sel_arma = st.selectbox("Armas:", list(armas_adm.keys()), key="adm_w")
            if st.button("Equipar Arma"): st.session_state.espada = {"nome": sel_arma, "dano": armas_adm[sel_arma]}; st.rerun()

    if st.button("🔄 Reset Total"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- BATALHA ---
elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    d_base = st.session_state.espada['dano']
    if st.session_state.classe == "Bárbaro 🪓": d_base += 5
    
    # Cálculo de Dano Final
    mult = 2.5 if (st.session_state.furia_rodadas > 0 and st.session_state.classe == "Mago 🧙") else (1.7 if st.session_state.furia_rodadas > 0 else 1.0)
    d_at = int(d_base * mult)
    
    if st.session_state.classe == "ADM ⚡": d_at *= 11 # +1000% (1x original + 10x bônus)
    if st.session_state.classe == "Arqueiro 🏹" and random.random() < 0.2: d_at *= 2; st.warning("🎯 CRÍTICO!")
    
    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    if st.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if st.session_state.classe == "Clérigo ⛪": st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + 5)
        if m['v'] <= 0:
            rec = m['o']
            if st.session_state.classe == "Mercador 💰": rec = int(rec * 1.5)
            if st.session_state.classe == "ADM ⚡": rec *= 11 # +1000% Moedas
            st.session_state.moedas += int(rec)
            st.session_state.em_combate = False; st.session_state.em_dungeon = False; st.rerun()
        else:
            st.session_state.vida -= m['d']; st.rerun()
    
    if st.button("Cura 🧪") and st.session_state.pocoes > 0:
        v_c = 60 if st.session_state.classe == "Paladino 🛡️" else 40
        st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + v_c); st.session_state.pocoes -= 1; st.rerun()

# --- VILA ---
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    tabs = st.tabs(["📜 Missões", "⚔️ Armas", "🛡️ Armaduras", "🧪 Alquimia", "🧙 Mago"])
    with tabs[4]:
        st.write("### Mago das Classes")
        st.write("O ritual custa 50 moedas na primeira vez e 450 nas próximas. A classe será aleatória!")
        
        # EXIBINDO O QUE CADA UMA FAZ
        st.info("""
        🛡️ **Guerreiro:** +15 de HP Máximo.  
        🧙 **Mago:** Fúria dá 2.5x de dano.  
        🗡️ **Ladino:** Aumenta chance de achar Vila/Dungeon.  
        🛡️ **Paladino:** Poções curam 60 HP.  
        🪓 **Bárbaro:** +5 de Dano base fixo.  
        🏹 **Arqueiro:** 20% de chance de Dano Dobrado (Crítico).  
        ⛪ **Clérigo:** Regenera 5 de HP por turno na luta.  
        💰 **Mercador:** Ganha 50% a mais de moedas.
        """)
        
        custo = 50 if st.session_state.vezes_mudou_classe == 0 else 450
        if st.button(f"🔮 Realizar Ritual ({custo} 💰)"):
            if st.session_state.moedas >= custo:
                st.session_state.moedas -= custo
                st.session_state.vezes_mudou_classe += 1
                nova_cl = random.choice(["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰"])
                st.session_state.classe = nova_cl
                st.session_state.vida_max = (115 if nova_cl == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max; st.rerun()

    with tabs[1]:
        loja_w = {"Ferro ⚔️": (250, 14), "Rei Caído 💀": (3500, 50)}
        for n, (c, d) in loja_w.items():
            if st.button(f"{n} ({d} D) - {c}💰") and st.session_state.moedas >= c:
                st.session_state.moedas -= c; st.session_state.espada = {"nome": n, "dano": d}; st.rerun()
    
    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

# --- MAPA ---
else:
    st.subheader("🗺️ Exploração")
    c1, c2 = st.columns(2)
    
    # Chance de Dungeon
    prob_base = 1
    if st.session_state.classe == "Ladino 🗡️": prob_base = 2
    if st.session_state.classe == "ADM ⚡": prob_base = 75 # Aumenta 75%
    
    if c1.button("Andar 🥾"):
        roll = random.randint(1, 100)
        if roll <= prob_base: st.session_state.dungeon_tipo = "Dungeon Rara"; st.session_state.em_dungeon = True
        elif random.randint(1, 5) == 1: st.session_state.achou_vila = True
        st.rerun()
    
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.em_dungeon:
        st.warning(f"📍 Dungeon: {st.session_state.dungeon_tipo}")
        if st.button("ENTRAR!"): spawn(); st.rerun()
        if st.button("Ignorar"): st.session_state.em_dungeon = False; st.rerun()
    
    if st.session_state.achou_vila:
        st.success("🏘️ Vila avistada!")
        if st.button("Entrar na Vila"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if st.button("Ignorar"): st.session_state.achou_vila = False; st.rerun()
