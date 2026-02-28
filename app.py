Com certeza! Reajustei os valores das recompensas das missões para os novos valores que você pediu: 25, 40, 70, 120 e 150 moedas. Isso vai ajudar o Arthur a conseguir a Espada de Cavaleiro muito mais rápido!

Também mantive a missão do REI com as 500 moedas, já que é o desafio final.

⚔️ Código Atualizado: Dragões e Espadas
Python

import streamlit as st
import random
import json

# --- SETUP ---
st.set_page_config(page_title="Dragões e Espadas", page_icon="🐲", layout="wide")

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

# --- SIDEBAR ---
with st.sidebar:
    st.header(f"👤 {st.session_state.nome_heroi}")
    st.write(f"❤️ HP: {st.session_state.vida}/100")
    st.progress(max(0.0, min(1.0, st.session_state.vida / 100)))
    st.markdown(f"<div style='background-color:#FFD700;padding:10px;border-radius:10px;text-align:center;border:2px solid #B8860B;'><span style='color:#000;font-weight:bold;font-size:20px;'>💰 {st.session_state.moedas} Moedas</span></div>", unsafe_allow_html=True)
    st.write(f"🗡️ {st.session_state.espada['nome']} ({st.session_state.espada['dano']} dano)")
    st.write(f"🧪 Cura: {st.session_state.pocoes} | ⚡ Fúria: {st.session_state.pocoes_furia}")
    
    st.write("---")
    st.download_button("💾 SALVAR JOGO", data=export_save(), file_name=f"save_{st.session_state.nome_heroi}.json")
    if st.button("🔄 Reiniciar Tudo"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- LÓGICA PRINCIPAL ---
st.title("🐲 Dragões e Espadas")

if st.session_state.vida <= 0:
    st.error("💀 DERROTADO!")
    if st.button("Pagar Resgate (50 💰)"):
        st.session_state.moedas -= 50; st.session_state.vida = 100; st.session_state.em_combate = False; st.rerun()

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
            
            if st.session_state.em_dungeon:
                st.session_state.dungeon_progresso += 1
                if st.session_state.dungeon_progresso >= 7:
                    recs = {"Gosmas (Fácil)": 200, "Goblins (Médio)": 450, "Dragões (Difícil)": 800}
                    st.session_state.moedas += recs.get(st.session_state.dungeon_tipo, 0)
                    st.session_state.em_dungeon = False; st.session_state.em_combate = False
                else: spawn(m['n'])
            else: st.session_state.em_combate = False
            st.rerun()
        else: st.session_state.vida -= m['d']; st.rerun()
        
    if b2.button("Cura 🧪") and st.session_state.pocoes > 0:
        st.session_state.vida = min(100, st.session_state.vida + 40); st.session_state.pocoes -= 1; st.rerun()
    if b3.button("Fúria ⚡") and st.session_state.pocoes_furia > 0:
        st.session_state.furia_rodadas = 3; st.session_state.pocoes_furia -= 1; st.rerun()
    if b4.button("FUGIR 🏃"):
        if st.session_state.em_dungeon: st.session_state.em_dungeon = False
        st.session_state.em_combate = False; st.rerun()

elif st.session_state.na_vila:
    st.subheader("🏘️ Vila")
    t1, t2, t3 = st.tabs(["📜 Missões", "⚒️ Ferreiro", "🧪 Alquimia"])
    with t1:
        if st.button("Procurar monstros ao redor 👾"): spawn(); st.rerun()
        st.write("---")
        # NOVAS RECOMPENSAS: 25, 40, 70, 120 e 150
        miss = [
            {"i": "Joshua", "de": "2 Gosmas", "a": {"Gosma 🟢": 2}, "p": 25},
            {"i": "Silas", "de": "5 Gosmas", "a": {"Gosma 🟢": 5}, "p": 40},
            {"i": "Maria", "de": "3 Goblins", "a": {"Goblin 👺": 3}, "p": 70},
            {"i": "Bram", "de": "5 Gobs e 3 Gosmas", "a": {"Goblin 👺": 5, "Gosma 🟢": 3}, "p": 120},
            {"i": "Elara", "de": "1 Dragão", "a": {"Dragão 🐲": 1}, "p": 150},
            {"i": "REI", "de": "Derrotar o REI DRAGÃO", "a": {"🔥 REI DRAGÃO 🔥": 1}, "p": 500}
        ]
        for x in miss:
            if x['i'] not in st.session_state.concluidas:
                if x['i'] not in st.session_state.missoes_ativas:
                    if st.button(f"Falar com {x['i']}: {x['de']}"):
                        st.session_state.missoes_ativas[x['i']] = {"a": x['a'], "p": {k:0 for k in x['a']}, "pago": x['p']}
                        if x['i'] == "REI": spawn(boss=True)
                        st.rerun()
                else:
                    at = st.session_state.missoes_ativas[x['i']]
                    if all(at['p'][k] >= at['a'][k] for k in at['a']):
                        if st.button(f"Entregar para {x['i']} ✅"):
                            st.session_state.moedas += at['pago']; st.session_state.concluidas.append(x['i'])
                            del st.session_state.missoes_ativas[x['i']]; st.rerun()
                    else: st.info(f"Pendente: {x['de']}")
    with t2:
        loja = {"Pedra 🪨": (150, 10), "Ferro ⚔️": (250, 14), "Ouro 👑": (400, 18), "Cavaleiro 🛡️": (1000, 22), "Rei Caído 💀": (3500, 50)}
        for n, (c, d) in loja.items():
            if st.button(f"{n} ({d} Dano) - {c}💰"):
                if st.session_state.moedas >= c:
                    st.session_state.moedas -= c; st.session_state.espada = {"nome": n, "dano": d}; st.rerun()
    with t3:
        if st.button("Poção Cura (35💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes += 1; st.rerun()
        if st.button("Poção Fúria (35💰)"):
            if st.session_state.moedas >= 35: st.session_state.moedas -= 35; st.session_state.pocoes_furia += 1; st.rerun()
    if st.button("Sair da Vila 🚪"): st.session_state.na_vila = False; st.rerun()

else:
    st.subheader("🗺️ Exploração")
    c1, c2 = st.columns(2)
    if c1.button("Andar 🥾"):
        sorte = random.randint(1, 100)
        if random.randint(1, 5) == 1: st.session_state.achou_vila = True
        elif sorte <= 2: st.session_state.dungeon_tipo = "Dragões (Difícil)"; st.session_state.em_dungeon = True
        elif sorte <= 6: st.session_state.dungeon_tipo = "Goblins (Médio)"; st.session_state.em_dungeon = True
        elif sorte <= 16: st.session_state.dungeon_tipo = "Gosmas (Fácil)"; st.session_state.em_dungeon = True
        st.rerun()
    if c2.button("Lutar 👾"): spawn(); st.rerun()
    
    if st.session_state.em_dungeon:
        st.warning(f"🏰 {st.session_state.dungeon_tipo}")
        if st.button("ENTRAR (7 Monstros)"):
            st.session_state.dungeon_progresso = 0
            tp = "Gosma 🟢" if "Gosma" in st.session_state.dungeon_tipo else "Goblin 👺" if "Goblin" in st.session_state.dungeon_tipo else "Dragão 🐲"
            spawn(tp); st.rerun()
        if st.button("Ignorar Dungeon"): st.session_state.em_dungeon = False; st.rerun()
        
    if st.session_state.achou_vila:
        st.success("🏘️ Vila avistada!")
        col_v1, col_v2 = st.columns(2)
        if col_v1.button("Entrar na Vila 🚪"):
            st.session_state.na_vila = True; st.session_state.achou_vila = False; st.rerun()
        if col_v2.button("Ignorar Vila 🚶"):
            st.session_state.achou_vila = False; st.rerun()

st.write("---")
for log in reversed(st.session_state.log[-5:]): st.write(log)
