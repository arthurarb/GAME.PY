import streamlit as st
import random
import json
import time
import os

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

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
    st.title("🐲 Dragões e Espadas")
    st.subheader("Retornar à Jornada")
    arquivo_save = st.file_uploader("Arraste seu arquivo .json aqui:", type=["json"])
    if arquivo_save and st.button("Confirmar Carregamento 📂"):
        carregar_save(arquivo_save)
    st.write("---")
    st.subheader("Nova Jornada")
    nome = st.text_input("Nome do novo herói:", placeholder="Ex: Arthur")
    
    autosave_opt = st.checkbox("Ativar Auto-Save (Lembrete de Download)", value=True)
    
    if st.button("Iniciar Nova Jornada ⚔️"):
        if nome:
            st.session_state.update({
                'nome_heroi': nome, 'classe': "Nenhuma 👤", 'vezes_mudou_classe': 0, 
                'nivel': 1, 'xp': 0, 'vida_max': 100, 'vida': 100, 'moedas': 20, 
                'pocoes': 2, 'pocoes_furia': 0, 'furia_rodadas': 0,
                'espada': {"nome": "Madeira 🪵", "dano": 7},
                'armadura': {"nome": "Madeira 🪵", "bonus": 0},
                'em_combate': False, 'monstro': None, 'na_vila': False,
                'achou_vila': False, 'log': [f"{nome} iniciou a jornada!"],
                'missoes_ativas': {}, 'em_dungeon': False, 'dungeon_tipo': None,
                'autosave_ativo': autosave_opt, 'last_autosave': time.time()
            })
            st.rerun()
    st.stop()

# --- LÓGICA DE NÍVEL (LEVEL UP) ---
xp_para_subir = st.session_state.nivel * 100
if st.session_state.xp >= xp_para_subir and st.session_state.nivel < 10:
    st.session_state.nivel += 1
    st.session_state.xp = 0
    # Atualiza vida máxima se for guerreiro (+3 por nível)
    if st.session_state.classe == "Guerreiro ⚔️":
        st.session_state.vida_max += 3
    st.session_state.vida = st.session_state.vida_max
    st.balloons()
    st.success(f"🎊 LEVEL UP! Você agora está no Nível {st.session_state.nivel}!")

# --- LÓGICA DE AUTO-SAVE ---
if st.session_state.get('autosave_ativo'):
    tempo_atual = time.time()
    if tempo_atual - st.session_state.last_autosave >= 30:
        st.session_state.last_autosave = tempo_atual
        st.toast("⚠️ HORA DE SALVAR! Clique em 'SALVAR JOGO MANUAL' para não perder progresso.")

# --- FUNÇÕES ---
def spawn(tipo_nome=None):
    # Vida do monstro aumenta 10% por nível do jogador
    mult_vida = 1.0 + (st.session_state.nivel - 1) * 0.10
    
    m_data = {
        "Gosma 🟢": {"n": "Gosma 🟢", "v": int(30 * mult_vida), "d": 4, "o": 5, "xp": 20},
        "Goblin 👺": {"n": "Goblin 👺", "v": int(50 * mult_vida), "d": 9, "o": 10, "xp": 45},
        "Dragão 🐲": {"n": "Dragão 🐲", "v": int(80 * mult_vida), "d": 15, "o": 30, "xp": 100},
        "🔥 REI DRAGÃO 🔥": {"n": "🔥 REI DRAGÃO 🔥", "v": int(500 * mult_vida), "d": 25, "o": 500, "xp": 500},
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
    st.caption(f"XP: {st.session_state.xp} / {xp_para_subir}")
    st.success(f"Classe: {st.session_state.classe}")
    st.write(f"❤️ HP: {st.session_state.vida} / {st.session_state.vida_max}")
    st.progress(max(0.0, min(1.0, st.session_state.vida / st.session_state.vida_max)))
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    st.markdown(f"### 💰 {st.session_state.moedas} Moedas")
    
    # --- INTERFACE DE SALVAMENTO ---
    st.download_button("💾 SALVAR JOGO MANUAL", data=export_save(), file_name=f"save_{st.session_state.nome_heroi}.json")

# --- LÓGICA DE COMBATE ---
if st.session_state.vida <= 0:
    st.error("💀 VOCÊ MORREU!")
    if st.button("Pagar Resgate (50 💰)"):
        if st.session_state.moedas >= 50: st.session_state.moedas -= 50; st.session_state.vida = 25; st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    lvl = st.session_state.nivel
    st.subheader(f"⚔️ Batalha: {m['n']} (Nível Inimigo Equiv. {lvl})")
    
    # Cálculos de Dano com Buffs de Nível
    d_base = st.session_state.espada['dano']
    
    # Bônus Bárbaro: +5 base e +1 por nível
    if st.session_state.classe == "Bárbaro 🪓": 
        d_base += (5 + (lvl - 1))
    
    # Multiplicador Mago: 2.5 base + 0.05 por nível
    mag_mult = 2.5 + ((lvl - 1) * 0.05)
    mult = mag_mult if (st.session_state.furia_rodadas > 0 and st.session_state.classe == "Mago 🧙") else (1.7 if st.session_state.furia_rodadas > 0 else 1.0)
    
    d_at = int(d_base * mult)
    
    # ADM Bônus
    if st.session_state.classe == "ADM ⚡": d_at *= 11
    
    # Arqueiro: +5% chance e +0.05 dano por nível
    if st.session_state.classe == "Arqueiro 🏹":
        chance_crit = 0.2 + ((lvl - 1) * 0.05)
        d_at = int(d_at * (1 + (lvl-1)*0.05))
        if random.random() < chance_crit:
            d_at *= 2
            st.warning("🎯 CRÍTICO!")
    
    col1, col2 = st.columns(2)
    col1.metric("HP Inimigo", m['v'])
    col2.metric("Seu HP", st.session_state.vida)
    
    if st.button("ATACAR!"):
        m['v'] -= d_at
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        
        # Clérigo: 3 regen base + 1 a cada 2 níveis
        if st.session_state.classe == "Clérigo ⛪": 
            regen = 3 + ((lvl - 1) // 2)
            st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + regen)
            
        if m['v'] <= 0:
            rec_o = int(m['o'] * (1.5 if st.session_state.classe == "Mercador 💰" else 1.0))
            if st.session_state.classe == "ADM ⚡": rec_o *= 11
            st.session_state.moedas += rec_o
            st.session_state.xp += m['xp']
            st.session_state.em_combate = False
            st.success(f"Vitória! +{rec_o} moedas e +{m['xp']} XP!")
            if st.button("Continuar"): st.rerun()
        else:
            st.session_state.vida -= m['d']
            st.rerun()
    
    if st.button("Cura 🧪") and st.session_state.pocoes > 0:
        v_c = 60 if st.session_state.classe == "Paladino 🛡️" else 40
        st.session_state.vida = min(st.session_state.vida_max, st.session_state.vida + v_c)
        st.session_state.pocoes -= 1
        st.rerun()

    if st.button("FUGIR 🏃"):
        st.session_state.em_combate = False
        st.rerun()

# --- VILA E EXPLORAÇÃO (Restante do código original mantido) ---
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3, t4, t5 = st.tabs(["📜 Missões", "⚔️ Armas", "🛡️ Armaduras", "🧪 Alquimia", "🧙 Mago"])
    
    with t5:
        custo = 50 if st.session_state.vezes_mudou_classe == 0 else 450
        if st.button(f"🔮 Ritual de Classe ({custo} 💰)"):
            if st.session_state.moedas >= custo:
                st.session_state.moedas -= custo
                st.session_state.vezes_mudou_classe += 1
                nova = random.choice(["Guerreiro ⚔️", "Mago 🧙", "Ladino 🗡️", "Paladino 🛡️", "Bárbaro 🪓", "Arqueiro 🏹", "Clérigo ⛪", "Mercador 💰"])
                st.session_state.classe = nova
                st.session_state.vida_max = (115 if nova == "Guerreiro ⚔️" else 100) + st.session_state.armadura['bonus'] + ((st.session_state.nivel-1)*3 if nova == "Guerreiro ⚔️" else 0)
                st.session_state.vida = st.session_state.vida_max
                st.rerun()
    
    with t4:
        if st.button("Cura (35💰)"): 
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes += 1; st.rerun()

    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

else:
    st.subheader("🗺️ Exploração")
    c1, c2 = st.columns(2)
    if c1.button("Andar 🥾"):
        if random.randint(1, 5) == 1: st.session_state.achou_vila = True
        else: st.write("Você andou um pouco...")
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.achou_vila:
        if st.button("Entrar na Vila"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
