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

# --- SIDEBAR ---
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
            lista_adm = ["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰", "ADM ⚡"]
            escolha = st.selectbox("Selecione:", lista_adm)
            if st.button("Equipar Classe"):
                st.session_state.classe = escolha
                if escolha == "ADM ⚡": st.session_state.vida_max = 100000
                else: st.session_state.vida_max = (115 if escolha == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max; st.rerun()

            if st.button("🏘️ Spawnar Vila"): st.session_state.achou_vila = True; st.rerun()
            st.write("🏰 Spawnar Dungeon:")
            d_adm = ["Gosmas (Fácil)", "Goblins (Médio)", "Dragões (Difícil)", "COVIL DO REI DRAGÃO 👑"]
            sel_d = st.selectbox("Dungeon:", d_adm)
            if st.button("Ir para Dungeon"): st.session_state.dungeon_tipo = sel_d; st.session_state.em_dungeon = True; st.rerun()

    if st.button("🔄 Reset Total"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name="save_dragao.json")

# --- LÓGICA PRINCIPAL ---
if st.session_state.vida <= 0:
    st.error("💀 VOCÊ MORREU!")
    if st.button("Renascer (50 💰)"):
        if st.session_state.moedas >= 50: st.session_state.moedas -= 50; st.session_state.vida = 25; st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    d_base = st.session_state.espada['dano']
    if st.session_state.classe == "Bárbaro 🪓": d_base += 5
    
    mult = 2.5 if (st.session_state.furia_rodadas > 0 and st.session_state.classe == "Mago 🧙") else (1.7 if st.session_state.furia_rodadas > 0 else 1.0)
    d_at = int(d_base * mult)
    
    if st.session_state.classe == "ADM ⚡": d_at *= 11 
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
            if st.session_state.classe == "ADM ⚡": rec *= 11
            st.session_state.moedas += int(rec)
            st.session_state.em_combate = False; st.session_state.em_dungeon = False; st.rerun()
        else:
            st.session_state.vida -= m['d']; st.rerun()
    
    if st.button("Cura 🧪") and st.session_state.pocoes > 0:
        v_c = 60 if st.session_state.classe == "Paladino 🛡️" else 40
        st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + v_c); st.session_state.pocoes -= 1; st.rerun()

elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3, t4, t5 = st.tabs(["📜 Missões", "⚔️ Armas", "🛡️ Armaduras", "🧪 Alquimia", "🧙 Mago"])
    
    with t5:
        st.write("### Mago das Classes")
        st.info("Sorteio aleatório! 50 moedas na 1ª vez, 450 depois.")
        st.write("**O que cada uma faz:**")
        st.write("- **Guerreiro:** +15 HP Max | **Mago:** Fúria 2.5x dano | **Ladino:** +Sorte Mapa")
        st.write("- **Paladino:** Cura Forte | **Bárbaro:** +5 Dano Fixo | **Arqueiro:** Crítico (2x)")
        st.write("- **Clérigo:** Regen HP turno | **Mercador:** +50% Ouro")
        
        custo = 50 if st.session_state.vezes_mudou_classe == 0 else 450
        if st.button(f"🔮 Ritual Aleatório ({custo} 💰)"):
            if st.session_state.moedas >= custo:
                st.session_state.moedas -= custo
                st.session_state.vezes_mudou_classe += 1
                nova = random.choice(["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰"])
                st.session_state.classe = nova
                st.session_state.vida_max = (115 if nova == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus']
                st.session_state.vida = st.session_state.vida_max; st.rerun()
    
    with t2:
        if st.button("Ferro ⚔️ (250💰)"): st.session_state.espada = {"nome": "Ferro ⚔️", "dano": 14}; st.rerun()

    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

else:
    st.subheader("🗺️ Exploração")
    prob = 1
    if st.session_state.classe == "Ladino 🗡️": prob = 2
    if st.session_state.classe == "ADM ⚡": prob = 75
    
    c1, c2 = st.columns(2)
    if c1.button("Andar 🥾"):
        roll = random.randint(1, 100)
        if roll <= prob: st.session_state.dungeon_tipo = "Dungeon"; st.session_state.em_dungeon = True
        elif random.randint(1, 5) == 1: st.session_state.achou_vila = True
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.em_dungeon:
        st.warning(f"📍 {st.session_state.dungeon_tipo} avistada!")
        if st.button("ENTRAR!"): spawn(); st.rerun()
        if st.button("Ignorar Dung"): st.session_state.em_dungeon = False; st.rerun()
    
    if st.session_state.achou_vila:
        st.success("🏘️ Vila à vista!")
        if st.button("Entrar"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if st.button("Passar direto"): st.session_state.achou_vila = False; st.rerun()
