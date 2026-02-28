O desafio aumentou! Agora as Dungeons são verdadeiros testes de resistência. Enfrentar 7 monstros em sequência sem poder voltar à vila para comprar suprimentos exige que o Arthur se prepare muito bem antes de entrar.

Ajustei a lógica para que o bônus de moedas (200, 450 ou 800) só seja entregue após a sétima vitória consecutiva.

🏰 O que mudou no código:
Contador de 0 a 7: O progresso agora vai até 7.

Persistência: O monstro renasce automaticamente após cada vitória dentro da Dungeon até atingir a meta.

Recompensa Acumulada: Ele ganha as moedas normais de cada monstro + o bônus gigante no final.

Python

import streamlit as st
import random

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

# Inicialização segura das variáveis
if 'vida' not in st.session_state:
    st.session_state.update({
        'vida': 100, 'moedas': 20, 'pocoes': 2, 'pocoes_furia': 0,
        'furia_rodadas': 0,
        'espada': {"nome": "Madeira 🪵", "dano": 7},
        'em_combate': False, 'monstro': None,
        'na_vila': False, 'achou_vila': False,
        'log': ["Arthur inicia sua jornada!"],
        'missoes_ativas': {}, 'concluidas': [],
        'em_dungeon': False, 'dungeon_tipo': None, 'dungeon_progresso': 0
    })

# Garantia de variáveis de Dungeon
if 'em_dungeon' not in st.session_state:
    st.session_state.em_dungeon = False
    st.session_state.dungeon_progresso = 0

def add_log(txt):
    st.session_state.log.append(txt)

def spawn(tipo_nome=None, especial_boss=False):
    if especial_boss:
        st.session_state.monstro = {"n": "🔥 REI DRAGÃO 🔥", "v": 500, "d": 17, "o": 500}
    elif tipo_nome:
        m_list = {
            "Gosma 🟢": {"n": "Gosma 🟢", "v": 30, "d": 4, "o": 15},
            "Goblin 👺": {"n": "Goblin 👺", "v": 50, "d": 9, "o": 30},
            "Dragão 🐲": {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 60}
        }
        st.session_state.monstro = m_list[tipo_nome].copy()
    else:
        m = [{"n": "Gosma 🟢", "v": 30, "d": 4, "o": 15}, 
             {"n": "Goblin 👺", "v": 50, "d": 9, "o": 30},
             {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 60}]
        st.session_state.monstro = random.choice(m).copy()
    st.session_state.em_combate = True

# --- UI SIDEBAR ---
with st.sidebar:
    st.header("👤 Status")
    st.write(f"❤️ Vida: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    
    color = "#FF4B4B" if st.session_state.moedas < 0 else "#FFFFFF"
    st.markdown(f"<h3 style='color:{color}'>💰 Moedas: {st.session_state.moedas}</h3>", unsafe_allow_html=True)
    
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 Fúria: {st.session_state.furia_rodadas} rodadas")

    if st.session_state.em_dungeon:
        st.info(f"🏰 Dungeon: {st.session_state.dungeon_tipo}")
        st.write(f"Progresso: {st.session_state.dungeon_progresso} / 7 💀")
        st.progress(st.session_state.dungeon_progresso / 7)

    st.write("---")
    if st.button("🔄 Reiniciar Jogo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA PRINCIPAL ---
st.title("🐲 Dragões e Espadas")

# MORTE
if st.session_state.vida <= 0:
    st.error("💀 ARTHUR FOI DERROTADO!")
    st.session_state.em_dungeon = False 
    col_m1, col_m2 = st.columns(2)
    if col_m1.button("Pagar Resgate (50 💰)"):
        st.session_state.moedas -= 50; st.session_state.vida = 100; st.session_state.em_combate = False; st.rerun()
    if col_m2.button("Recomeçar 🔄"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# COMBATE
elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    
    d_atual = st.session_state.espada['dano']
    if st.session_state.furia_rodadas > 0: d_atual = int(d_atual * 1.7)

    c1, c2 = st.columns(2)
    c1.metric("HP Monstro", m['v'])
    c2.metric("Seu HP", st.session_state.vida)
    
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("Atacar!"):
        m['v'] -= d_atual
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            # Missões
            for n, i in st.session_state.missoes_ativas.items():
                if m['n'] in i['p']: i['p'][m['n']] = min(i['a'][m['n']], i['p'][m['n']] + 1)
            
            # Lógica de Dungeon (7 Monstros)
            if st.session_state.em_dungeon:
                st.session_state.dungeon_progresso += 1
                if st.session_state.dungeon_progresso >= 7:
                    recompensas = {"Gosmas (Fácil)": 200, "Goblins (Médio)": 450, "Dragões (Difícil)": 800}
                    premio = recompensas[st.session_state.dungeon_tipo]
                    st.session_state.moedas += premio
                    add_log(f"🏰 DUNGEON LIMPA! Você sobreviveu aos 7 monstros! +{premio} moedas!")
                    st.session_state.em_dungeon = False
                    st.session_state.em_combate = False
                else:
                    add_log(f"Inimigo {st.session_state.dungeon_progresso}/7 derrotado!")
                    spawn(m['n']) # Próximo monstro do mesmo tipo
            else:
                st.session_state.em_combate = False
                add_log(f"Vitória! +{m['o']} moedas.")
            st.rerun()
        else: 
            st.session_state.vida -= m['d']
        st.rerun()
    
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(100, st.session_state.vida + 40); st.session_state.pocoes -= 1; st.rerun()
    if b3.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas = 3; st.session_state.pocoes_furia -= 1; st.rerun()
    if b4.button("Fugir 🏃") and not st.session_state.em_dungeon:
        st.session_state.em_combate = False; st.rerun()

# EXPLORAÇÃO E VILA
elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    # ... abas de loja e missões (idênticas ao anterior)
    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

else:
    st.subheader("🗺️ Exploração")
    if st.session_state.em_dungeon:
        st.warning(f"🏰 Você está na entrada da Dungeon: {st.session_state.dungeon_tipo}")
        if st.button("INICIAR DESAFIO (7 Monstros) ⚔️"):
            tipo_m = "Gosma 🟢" if "Gosmas" in st.session_state.dungeon_tipo else "Goblin 👺" if "Goblins" in st.session_state.dungeon_tipo else "Dragão 🐲"
            st.session_state.dungeon_progresso = 0
            spawn(tipo_m)
            st.rerun()
        if st.button("DESISTIR E VOLTAR"): st.session_state.em_dungeon = False; st.rerun()
    else:
        c1, c2 = st.columns(2)
        if c1.button("Andar 🥾"):
            sorte = random.randint(1, 100)
            if random.randint(1, 5) == 1: st.session_state.achou_vila = True
            elif sorte <= 2: st.session_state.dungeon_tipo = "Dragões (Difícil)"; st.session_state.em_dungeon = True
            elif sorte <= 6: st.session_state.dungeon_tipo = "Goblins (Médio)"; st.session_state.em_dungeon = True
            elif sorte <= 16: st.session_state.dungeon_tipo = "Gosmas (Fácil)"; st.session_state.em_dungeon = True
            else: add_log("Caminhando...")
            st.rerun()
        if c2.button("Lutar 👾"): spawn(); st.rerun()

    if st.session_state.achou_vila:
        st.success("🏘️ Vila à vista!")
        if st.button("Entrar"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()

st.write("---")
for m in reversed(st.session_state.log[-5:]): st.write(m)
    
