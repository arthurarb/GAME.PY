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
        'missoes_ativas': {}, 'concluidas': []
    })

# Garante que as novas variáveis existam mesmo em saves antigos
if 'pocoes_furia' not in st.session_state:
    st.session_state.pocoes_furia = 0
if 'furia_rodadas' not in st.session_state:
    st.session_state.furia_rodadas = 0

def add_log(txt):
    st.session_state.log.append(txt)

loja = {
    "Pedra 🪨": {"c": 150, "d": 10}, "Ferro ⚔️": {"c": 250, "d": 14},
    "Ouro 👑": {"c": 400, "d": 18}, "Cavaleiro 🛡️": {"c": 750, "d": 22},
    "Rei Caído 💀": {"c": 3500, "d": 50}
}

def spawn(tipo="n"):
    if tipo == "b":
        st.session_state.monstro = {"n": "🔥 REI DRAGÃO 🔥", "v": 500, "d": 17, "o": 500}
    else:
        m = [{"n": "Gosma 🟢", "v": 30, "d": 4, "o": 15}, 
             {"n": "Goblin 👺", "v": 50, "d": 9, "o": 30},
             {"n": "Dragão 🐲", "v": 80, "d": 15, "o": 60}]
        st.session_state.monstro = random.choice(m)
    st.session_state.em_combate = True

# --- UI SIDEBAR ---
with st.sidebar:
    st.header("👤 Status")
    st.write(f"❤️ Vida: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    
    if st.session_state.moedas < 0:
        st.error(f"💰 Moedas: {st.session_state.moedas} (DÍVIDA!)")
    else:
        st.write(f"💰 Moedas: {st.session_state.moedas}")
        
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    if st.session_state.furia_rodadas > 0:
        st.warning(f"🔥 Fúria Ativa: {st.session_state.furia_rodadas} rodadas")

    st.write("---")
    st.header("📜 Missões Ativas")
    if not st.session_state.missoes_ativas:
        st.write("Nenhuma missão.")
    else:
        for npc, dados in st.session_state.missoes_ativas.items():
            with st.expander(f"📍 {npc}", expanded=True):
                for monstro, alvo in dados['a'].items():
                    prog = dados['p'][monstro]
                    st.write(f"{monstro}: {prog}/{alvo}")
                    st.progress(min(1.0, prog/alvo))
    
    st.write("---")
    if st.button("🔄 Reiniciar Jogo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA PRINCIPAL ---
st.title("🐲 Dragões e Espadas")

if st.session_state.vida <= 0:
    st.error("💀 ARTHUR FOI DERROTADO!")
    col_m1, col_m2 = st.columns(2)
    if col_m1.button("Pagar Resgate (50 💰)"):
        st.session_state.moedas -= 50; st.session_state.vida = 100; st.session_state.em_combate = False; st.session_state.furia_rodadas = 0; st.rerun()
    if col_m2.button("Recomeçar 🔄"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    
    d_atual = st.session_state.espada['dano']
    if st.session_state.furia_rodadas > 0:
        d_atual = int(d_atual * 1.7)
        st.info(f"🔥 Modo Fúria! Dano: {d_atual}")

    c1, c2 = st.columns(2)
    c1.metric("HP Monstro", m['v'])
    c2.metric("Seu HP", st.session_state.vida)
    
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("Atacar!"):
        m['v'] -= d_atual
        if st.session_state.furia_rodadas > 0: st.session_state.furia_rodadas -= 1
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            for n, i in st.session_state.missoes_ativas.items():
                if m['n'] in i['p']: i['p'][m['n']] = min(i['a'][m['n']], i['p'][m['n']] + 1)
            st.session_state.em_combate = False
            add_log(f"Vitória! +{m['o']} moedas.")
        else: st.session_state.vida -= m['d']
        st.rerun()
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(100, st.session_state.vida + 40); st.session_state.pocoes -= 1; st.rerun()
    if b3.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas = 3; st.session_state.pocoes_furia -= 1; st.rerun()
    if b4.button("Fugir 🏃"):
        st.session_state.em_combate = False; st.session_state.furia_rodadas = 0; st.rerun()

elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3 = st.tabs(["Aldeões & Caça", "Ferreiro", "Poções"])
    with t1:
        if st.button("Caçar monstros perto da vila 👾"):
            spawn() # 100% DE CHANCE
            st.rerun()
        st.write("--- 👨‍🌾 Missões ---")
        # ... (código das missões igual ao anterior)
        miss = [
            {"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 10},
            {"i": "Silas", "de": "5 Gosmas", "a": {"Gosma 🟢": 5}, "p": 20},
            {"i": "Maria", "de": "3 Goblins", "a": {"Goblin 👺": 3}, "p": 40},
            {"i": "Bram", "de": "5 Gobs/3 Gosmas", "a": {"Goblin 👺": 5, "Gosma 🟢": 3}, "p": 70},
            {"i": "Elara", "de": "1 Dragão", "a": {"Dragão 🐲": 1}, "p": 100},
            {"i": "REI", "de": "REI DRAGÃO", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500}
        ]
        for x in miss:
            if x['i'] not in st.session_state.concluidas:
                if x['i'] not in st.session_state.missoes_ativas:
                    if st.button(f"Falar com {x['i']}: {x['de']}"):
                        if x['i'] == "REI" and random.randint(1,100) != 1: st.warning("Rei Ocupado")
                        elif x['i'] == "REI": spawn("b"); st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}; st.rerun()
                        else: st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}; st.rerun()
                else:
                    at = st.session_state.missoes_ativas[x['i']]
                    if all(at['p'][k] >= at['a'][k] for k in at['a']):
                        if st.button(f"Entregar {x['i']} ✅"):
                            st.session_state.moedas += at['pago']
                            if x['i'] == "REI": st.session_state.concluidas.append(x['i'])
                            del st.session_state.missoes_ativas[x['i']]; st.rerun()
    with t2:
        for n, i in loja.items():
            if st.button(f"{n} ({i['d']} Dano) - {i['c']}💰"):
                if st.session_state.moedas >= i['c']:
                    st.session_state.moedas -= i['c']; st.session_state.espada = {"nome": n, "dano": i['d']}; st.rerun()
    with t3:
        if st.button("Poção de Cura (35 💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes += 1; st.rerun()
        if st.button("Poção de Fúria (35 💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes_furia += 1; st.rerun()
    if st.button("Sair da Vila 🚪"):
        st.session_state.na_vila = False; st.rerun()
else:
    st.subheader("🗺️ Exploração")
    colA, colB = st.columns(2)
    if colA.button("Andar 🥾"):
        if random.randint(1, 5) == 1: st.session_state.achou_vila = True
        else: add_log("Nada aqui."); st.rerun()
    if colB.button("Lutar 👾"):
        spawn() # 100% DE CHANCE
        st.rerun()
    if st.session_state.achou_vila:
        st.success("🏘️ Vila à vista!")
        if st.button("Entrar"): st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if st.button("Ignorar"): st.session_state.achou_vila = False; st.rerun()
st.write("---")
for m in reversed(st.session_state.log[-5:]): st.write(m)
