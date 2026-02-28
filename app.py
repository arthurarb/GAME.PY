import streamlit as st
import random

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

if 'vida' not in st.session_state:
    st.session_state.update({
        'vida': 100, 'moedas': 20, 'pocoes': 2,
        'espada': {"nome": "Madeira 🪵", "dano": 7},
        'em_combate': False, 'monstro': None,
        'na_vila': False, 'achou_vila': False,
        'log': ["Arthur inicia sua jornada!"],
        'missoes_ativas': {}, 'concluidas': []
    })

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
        m = [{"n": "Gosma 🟢", "v": 30, "d": 5, "o": 15}, 
             {"n": "Goblin 👺", "v": 50, "d": 12, "o": 30},
             {"n": "Dragão 🐲", "v": 80, "d": 18, "o": 60}]
        st.session_state.monstro = random.choice(m)
    st.session_state.em_combate = True

# --- UI ---
st.title("🐲 Dragões e Espadas")

with st.sidebar:
    st.header("👤 Status")
    st.write(f"❤️ Vida: {st.session_state.vida}/100")
    st.write(f"💰 Moedas: {st.session_state.moedas}")
    st.write(f"🗡️ {st.session_state.espada['nome']}")
    st.write(f"🧪 Poções: {st.session_state.pocoes}")
    if st.button("Resetar Jogo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

if st.session_state.vida <= 0:
    st.error("💀 Arthur caiu!")
    if st.button("Renascer"):
        st.session_state.vida = 100
        st.rerun()

elif st.session_state.em_combate:
    m = st.session_state.monstro
    st.subheader(f"⚔️ Batalha: {m['n']}")
    c1, c2 = st.columns(2)
    c1.metric("HP Monstro", m['v'])
    c2.metric("Seu HP", st.session_state.vida)
    b1, b2, b3 = st.columns(3)
    if b1.button("Atacar!"):
        m['v'] -= st.session_state.espada['dano']
        if m['v'] <= 0:
            st.session_state.moedas += m['o']
            for n, i in st.session_state.missoes_ativas.items():
                if m['n'] in i['p']: i['p'][m['n']] = min(i['a'][m['n']], i['p'][m['n']] + 1)
            st.session_state.em_combate = False
        else:
            st.session_state.vida -= m['d']
        st.rerun()
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(100, st.session_state.vida + 40)
        st.session_state.pocoes -= 1
        st.rerun()
    if b3.button("Fugir 🏃"):
        st.session_state.em_combate = False
        st.rerun()

elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3 = st.tabs(["Aldeões", "Ferreiro", "Poções"])
    with t1:
        miss = [
            {"i": "Joshua", "de": "2 Goblins", "a": {"Goblin 👺": 2}, "p": 10, "u": False},
            {"i": "Silas", "de": "5 Goblins", "a": {"Goblin 👺": 5}, "p": 20, "u": False},
            {"i": "Maria", "de": "3 Gosmas", "a": {"Gosma 🟢": 3}, "p": 40, "u": False},
            {"i": "Bram", "de": "5 Gosmas/3 Gobs", "a": {"Gosma 🟢": 5, "Goblin 👺": 3}, "p": 70, "u": False},
            {"i": "Elara", "de": "1 Dragão", "a": {"Dragão 🐲": 1}, "p": 100, "u": False},
            {"i": "Cedric", "de": "3 Dragões", "a": {"Dragão 🐲": 3}, "p": 120, "u": False},
            {"i": "REI", "de": "REI DRAGÃO", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500, "u": True}
        ]
        for x in miss:
            if x['i'] not in st.session_state.concluidas:
                if x['i'] not in st.session_state.missoes_ativas:
                    if st.button(f"Missão {x['i']}: {x['de']}"):
                        if x['i'] == "REI" and random.randint(1,100) != 1: st.warning("Rei Ocupado")
                        elif x['i'] == "REI": spawn("b"); st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p'], "u": True}; st.rerun()
                        else: st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p'], "u": False}; st.rerun()
                else:
                    at = st.session_state.missoes_ativas[x['i']]
                    if all(at['p'][k] >= at['a'][k] for k in at['a']):
                        if st.button(f"Entregar {x['i']} ✅"):
                            st.session_state.moedas += at['pago']
                            if at['u']: st.session_state.concluidas.append(x['i'])
                            del st.session_state.missoes_ativas[x['i']]
                            st.rerun()
                    else: st.write(f"{x['i']} espera...")
    with t2:
        for n, i in loja.items():
            if st.button(f"{n} ({i['d']} Dano) - {i['c']}💰"):
                if st.session_state.moedas >= i['c']:
                    st.session_state.moedas -= i['c']; st.session_state.espada = {"nome": n, "dano": i['d']}; st.rerun()
