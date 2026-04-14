import streamlit as st
import random
import json
import time

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas Pro", page_icon="🐲", layout="wide")

# --- SISTEMA DE SAVE/LOAD ---
def export_save():
    dados = {k: v for k, v in st.session_state.items() if k not in ['log', 'last_autosave']}
    return json.dumps(dados, indent=4)

def carregar_save(arquivo):
    if arquivo:
        dados = json.load(arquivo)
        st.session_state.update(dados)
        st.rerun()

# --- INICIALIZAÇÃO ---
if 'nome_heroi' not in st.session_state:
    st.title("🐲 Dragões e Espadas: Level System")
    st.subheader("Retornar à Jornada")
    arquivo_save = st.file_uploader("Arraste seu arquivo .json aqui:", type=["json"])
    if arquivo_save and st.button("Confirmar Carregamento 📂"):
        carregar_save(arquivo_save)
    st.write("---")
    st.subheader("Nova Jornada")
    nome = st.text_input("Nome do novo herói:", placeholder="Ex: Arthur")
    autosave_opt = st.checkbox("Ativar Auto-Save Interno (30s)", value=True)
    
    if st.button("Iniciar Nova Jornada ⚔️"):
        if nome:
            st.session_state.update({
                'nome_heroi': nome, 'classe': "Nenhuma 👤", 'nivel': 1, 'xp': 0,
                'vezes_mudou_classe': 0, 'vida_max': 100, 'vida': 100, 'moedas': 20, 
                'pocoes': 2, 'pocoes_furia': 0, 'furia_rodadas': 0,
                'espada': {"nome": "Madeira 🪵", "dano": 7},
                'armadura': {"nome": "Madeira 🪵", "bonus": 0},
                'em_combate': False, 'monstro': None, 'na_vila': False,
                'achou_vila': False, 'log': [],
                'missoes_ativas': {}, 'em_dungeon': False, 'dungeon_tipo': None,
                'autosave_ativo': autosave_opt, 'last_autosave': time.time()
            })
            st.rerun()
    st.stop()

# --- LÓGICA DE LEVEL UP ---
xp_necessario = st.session_state.nivel * 100
if st.session_state.xp >= xp_necessario and st.session_state.nivel < 10:
    st.session_state.nivel += 1
    st.session_state.xp = 0
    # Atualiza vida máxima ao upar
    bonus_guerreiro = (st.session_state.nivel * 3) if st.session_state.classe == "Guerreiro ⚔️" else 0
    st.session_state.vida_max = (115 if st.session_state.classe == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus'] + bonus_guerreiro
    st.session_state.vida = st.session_state.vida_max
    st.balloons()
    st.toast(f"🎉 LEVEL UP! Agora você é nível {st.session_state.nivel}!")

# --- AUTO-SAVE ---
if st.session_state.get('autosave_ativo'):
    if time.time() - st.session_state.last_autosave >= 30:
        st.session_state.last_autosave = time.time()
        st.toast("💾 Progresso salvo internamente!")

# --- FUNÇÕES DE SPAWN ---
def spawn(tipo_nome=None):
    lvl = st.session_state.nivel
    # Monstros ganham 10% de vida por nível do jogador
    multi_hp = 1 + (lvl * 0.10)
    
    m_data = {
        "Gosma 🟢": {"n": "Gosma 🟢", "v": int(30 * multi_hp), "d": 4, "o": 5, "xp": 25},
        "Goblin 👺": {"n": "Goblin 👺", "v": int(50 * multi_hp), "d": 9, "o": 10, "xp": 50},
        "Dragão 🐲": {"n": "Dragão 🐲", "v": int(80 * multi_hp), "d": 15, "o": 30, "xp": 100},
        "🔥 REI DRAGÃO 🔥": {"n": "🔥 REI DRAGÃO 🔥", "v": int(500 * multi_hp), "d": 25, "o": 500, "xp": 1000},
        "🌌 DRAGÃO DEUS 🌌": {"n": "🌌 DRAGÃO DEUS 🌌", "v": 9999, "d": 999, "o": 9999, "xp": 0}
    }
    
    if tipo_nome and tipo_nome in m_data:
        st.session_state.monstro = m_data[tipo_nome].copy()
    else:
        st.session_state.monstro = m_data[random.choice(["Gosma 🟢", "Goblin 👺", "Dragão 🐲"])].copy()
    st.session_state.em_combate = True

# --- SIDEBAR ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi} (Lvl {st.session_state.nivel})")
    st.caption(f"XP: {st.session_state.xp} / {xp_necessario}")
    st.progress(st.session_state.xp / xp_necessario if st.session_state.nivel < 10 else 1.0)
    
    st.success(f"Classe: {st.session_state.classe}")
    st.write(f"❤️ HP: {st.session_state.vida} / {st.session_state.vida_max}")
    st.progress(max(0.0, min(1.0, st.session_state.vida / st.session_state.vida_max)))
    
    # Exibir Buffs Atuais por Nível
    with st.expander("✨ Bônus de Nível"):
        lvl = st.session_state.nivel
        if st.session_state.classe == "Guerreiro ⚔️": st.write(f"HP Bonus: +{lvl*3}")
        if st.session_state.classe == "Bárbaro 🪓": st.write(f"Dano Extra: +{lvl}")
        if st.session_state.classe == "Mago 🧙": st.write(f"Fúria Multi: {2.5 + (lvl*0.05):.2f}x")
        if st.session_state.classe == "Arqueiro 🏹": st.write(f"Crítico: {20+(lvl*5)}% | Dano: +{lvl*0.05:.2f}")
        if st.session_state.classe == "Clérigo ⛪": st.write(f"Regen: {3 + (lvl//2)}")

    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    st.markdown(f"### 💰 {st.session_state.moedas} Moedas")
    
    st.download_button("💾 EXPORTAR SAVE (.json)", data=export_save(), file_name=f"save_{st.session_state.nome_heroi}.json")
    if st.session_state.autosave_ativo:
        st.caption(f"⏱️ Próximo Auto-save em {max(0, 30 - int(time.time() - st.session_state.last_autosave))}s")

# --- LÓGICA DE COMBATE ---
if st.session_state.em_combate:
    m = st.session_state.monstro
    lvl = st.session_state.nivel
    st.subheader(f"⚔️ Batalha: {m['n']} (Escalado Lvl {lvl})")
    
    # Cálculo de Dano com Buffs de Nível
    d_base = st.session_state.espada['dano']
    if st.session_state.classe == "Bárbaro 🪓": d_base += (5 + lvl) # +1 por nível
    
    # Multiplicador Mago: 2.5x base + 0.05x por nível
    mago_mult = 2.5 + (lvl * 0.05)
    mult = mago_mult if (st.session_state.furia_rodadas > 0 and st.session_state.classe == "Mago 🧙") else (1.7 if st.session_state.furia_rodadas > 0 else 1.0)
    
    d_at = int(d_base * mult)
    
    # Arqueiro: 20% base + 5% por nível de chance. Dano base aumenta 0.05 por nível.
    if st.session_state.classe == "Arqueiro 🏹":
        d_at = int(d_at * (1 + (lvl * 0.05)))
        if random.random() < (0.20 + (lvl * 0.05)):
            d_at *= 2
            st.warning("🎯 CRÍTICO CERTEIRO!")

    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("ATACAR!"):
        m['v'] -= d_at
        # Regen Clérigo: 3 base + 1 a cada 2 níveis
        if st.session_state.classe == "Clérigo ⛪":
            regen = 3 + (lvl // 2)
            st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + regen)
        
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            st.session_state.xp += m['xp']
            st.session_state.em_combate = False
            st.success(f"Vitória! Ganhou {m['o']} moedas e {m['xp']} XP!")
            if st.button("Continuar"): st.rerun()
        else:
            st.session_state.vida -= m['d']
            st.rerun()
    
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + 40)
        st.session_state.pocoes -= 1
        st.rerun()
    
    if b4.button("FUGIR"):
        st.session_state.em_combate = False
        st.rerun()

# --- EXPLORAÇÃO E VILA ---
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3, t4, t5 = st.tabs(["📜 Missões", "⚔️ Armas", "🛡️ Armaduras", "🧪 Alquimia", "🧙 Mago"])
    
    with t5:
        st.write("### Mago das Classes")
        custo = 50 if st.session_state.vezes_mudou_classe == 0 else 450
        if st.button(f"🔮 Ritual ({custo} 💰)"):
            if st.session_state.moedas >= custo:
                st.session_state.moedas -= custo
                st.session_state.vezes_mudou_classe += 1
                st.session_state.classe = random.choice(["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰"])
                st.rerun()
    
    with t4:
        if st.button("Comprar Poção (35💰)"):
            if st.session_state.moedas >= 35:
                st.session_state.moedas -= 35
                st.session_state.pocoes += 1
                st.rerun()

    if st.button("Sair da Vila 🚪"):
        st.session_state.na_vila = False
        st.rerun()

else:
    st.subheader("🗺️ Exploração")
    c1, c2 = st.columns(2)
    if c1.button("Andar 🥾"):
        if random.randint(1, 10) <= 2: st.session_state.em_dungeon = True
        elif random.randint(1, 5) == 1: st.session_state.achou_vila = True
        else: st.write("Você caminhou tranquilamente.")
        st.rerun()
    
    if c2.button("Lutar 👾"):
        spawn()
        st.rerun()

    if st.session_state.achou_vila:
        if st.button("Entrar na Vila 🏘️"):
            st.session_state.na_vila = True
            st.session_state.achou_vila = False
            st.rerun()
            st.rerun()
        if st.button("Ignorar Dungeon"): st.session_state.em_dungeon = False; st.rerun()
    
