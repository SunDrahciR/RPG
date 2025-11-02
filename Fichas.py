import streamlit as st
import json
from io import StringIO

# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(page_title="Ficha de Personagem - OnePica RPG", layout="wide")

st.title("📜 Ficha de Personagem - OnePica RPG")
st.markdown("---")

# ===============================
# FUNÇÕES DE SALVAR/CARREGAR
# ===============================
def salvar_ficha(data):
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    st.download_button(
        label="💾 Baixar Ficha (.json)",
        data=json_data,
        file_name=f"Ficha_{data['nome'] or 'Personagem'}.json",
        mime="application/json",
    )

def carregar_ficha(upload):
    stringio = StringIO(upload.getvalue().decode("utf-8"))
    return json.load(stringio)

# ===============================
# INICIALIZAÇÃO DO SESSION STATE
# ===============================
chaves = [
    "nome", "titulo", "afiliacao", "raca", "versao", "origem",
    "vida_maxima", "vida_atual",
    "subatributos", "proficiencias", "estilo_luta",
    "historia", "aparencia", "armas",
    "habilidades_passivas", "ataques_nomeados", "modo"
]

for chave in chaves:
    if chave not in st.session_state:
        st.session_state[chave] = "" if chave != "subatributos" else {
            "forca": 10,
            "intelecto": 10,
            "resistencia": 10,
            "velocidade": 10,
            "elemental": 10
        }

# ===============================
# SIDEBAR — GERENCIAR FICHA
# ===============================
st.sidebar.header("📂 Gerenciar Ficha")
upload = st.sidebar.file_uploader("Carregar Ficha (.json)", type="json")

if upload is not None:
    try:
        dados_carregados = carregar_ficha(upload)
        for key, value in dados_carregados.items():
            st.session_state[key] = value
        st.sidebar.success("✅ Ficha carregada com sucesso! Os campos foram atualizados.")
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar ficha: {e}")

# ===============================
# INFORMAÇÕES BÁSICAS
# ===============================
st.header("Informações Gerais")
col1, col2, col3 = st.columns(3)
with col1:
    nome = st.text_input("1. Nome", value=st.session_state["nome"])
with col2:
    titulo = st.text_input("2. Título", value=st.session_state["titulo"])
with col3:
    afiliacao = st.text_input("3. Afiliação", value=st.session_state["afiliacao"])

col1, col2 = st.columns(2)
with col1:
    origem = st.text_input("5. Origem", value=st.session_state["origem"])

# ===============================
# RAÇAS
# ===============================
st.header("Raça")
racas = {
    "Humano": {"V1": "Ganha mais bônus ao upar sub-atributos (mestre decide o quanto).", "V2": "Os Hakis recebem +5."},
    "Tribo (Braço/Perna Longos)": {"V1": "Golpes com o membro respectivo recebem +7 em acerto.", "V2": "Todos os golpes com o membro viram de média distância e grandes."},
    "Tontata": {"V1": "+7 em esquiva e furtividade, -5 em resistência.", "V2": "Esquiva e furtividade +14."},
    "Homem-Peixe": {"V1": "Em água, força e resistência x2.", "V2": "Em água, força e resistência x3."},
    "Gigante": {"V1": "+7 em força, ataque e resistência; golpes grandes.", "V2": "+14 em força, ataque e resistência; golpes gigantes."},
    "Lunarianos": {"V1": "+20 resistência com chama acesa e +20 velocidade com chamas apagadas.", "V2": "+25 resistência com chama acesa e +25 velocidade com chamas apagadas."},
    "Nativo do Céu (Skypheano/Birkano/Shandiano)": {"V1": "+6 em combate aéreo.", "V2": "Movimento dobra em combate aéreo."},
    "Oni": {"V1": "+7 em ambientes de fogo.", "V2": "Força e resistência dobram em ambientes de fogo."},
    "Sereiano": {"V1": "+6 em movimentos dentro da água.", "V2": "Dobra o movimento dentro da água."},
    "Bucaneiro": {"V1": "+6 em força e resistência.", "V2": "+12 em força e resistência."},
    "Mink": {"V1": "+7 movimentação/rastreamento e modo Sulong (+35 dano e velocidade).", "V2": "+13 movimentação/rastreamento e modo Sulong (não muda)."},
    "Híbrido": {"V1": "O gene predominante define o status.", "V2": "A raça secundária começa a se desenvolver."},
}

col1, col2 = st.columns(2)
with col1:
    raca = st.selectbox("4. Raça", list(racas.keys()), index=list(racas.keys()).index(st.session_state["raca"]) if st.session_state["raca"] else 0)
with col2:
    versao = st.selectbox("Versão da Raça", ["V1", "V2"], index=["V1","V2"].index(st.session_state["versao"]) if st.session_state["versao"] else 0)

if raca:
    st.markdown(f"**Descrição da Raça ({raca} - {versao})**")
    st.info(racas[raca][versao])

# ===============================
# ATRIBUTOS E HAKI
# ===============================
st.header("Atributos e Haki")

# Vida
st.header("❤️ Vida")
vida_maxima = st.number_input("Vida Máxima", min_value=1, value=int(st.session_state["vida_maxima"] or 100), step=10)
vida_atual = st.number_input("Vida Atual", min_value=0, max_value=vida_maxima, value=int(st.session_state["vida_atual"] or vida_maxima), step=1)

# Subatributos
st.subheader("Subatributos")
col1, col2, col3 = st.columns(3)
with col1:
    forca = st.number_input("Força", min_value=0, value=st.session_state["subatributos"]["forca"], step=1)
    intelecto = st.number_input("Intelecto", min_value=0, value=st.session_state["subatributos"]["intelecto"], step=1)
with col2:
    resistencia = st.number_input("Resistência", min_value=0, value=st.session_state["subatributos"]["resistencia"], step=1)
    velocidade = st.number_input("Velocidade", min_value=0, value=st.session_state["subatributos"]["velocidade"], step=1)
with col3:
    elemental = st.number_input("Elemento", min_value=0, value=st.session_state["subatributos"]["elemental"], step=1)

subatributos = {"forca": forca, "intelecto": intelecto, "resistencia": resistencia, "velocidade": velocidade, "elemental": elemental}

# Haki
st.subheader("Haki")
st.markdown("""
**Haki do Armamento**  
- V1: +10 dano/defesa  
- V2: +15 dano/defesa  
- V3: +20 dano/defesa + libertação de energia  
- V4: +25 dano/defesa  
- V5: +30 dano/defesa + libertação de energia com efeitos dobrados  

**Haki da Observação**  
- V1: +10 esquiva/acerto  
- V2: +15 esquiva/acerto  
- V3: +20 esquiva/acerto + ignora furtividade  
- V4: +25 esquiva/acerto  
- V5: +30 esquiva/acerto + acerto garantido  

**Haki do Conquistador/Rei**  
- V1: +50 em golpes não-nomeados e remove efeitos negativos  
- V2: +55 e +1 ação de Haki do Rei  
- V3: Pode ser usado em ataque nomeado  
- V4: +60 e +1 ação  
- V5: Uso ilimitado
""")

col1, col2, col3 = st.columns(3)
with col1:
    haki_armamento = st.selectbox("Haki do Armamento", ["Nenhum", "V1", "V2", "V3", "V4", "V5"], index=["Nenhum","V1","V2","V3","V4","V5"].index(st.session_state.get("haki_armamento","Nenhum")))
with col2:
    haki_observacao = st.selectbox("Haki da Observação", ["Nenhum", "V1", "V2", "V3", "V4", "V5"], index=["Nenhum","V1","V2","V3","V4","V5"].index(st.session_state.get("haki_observacao","Nenhum")))
with col3:
    haki_conquistador = st.selectbox("Haki do Conquistador/Rei", ["Nenhum", "V1", "V2", "V3", "V4", "V5"], index=["Nenhum","V1","V2","V3","V4","V5"].index(st.session_state.get("haki_conquistador","Nenhum")))

# ===============================
# PROFICIÊNCIAS, ESTILO, HISTÓRIA, ETC
# ===============================
st.header("Proficiências")
proficiencias = st.text_input("7. Proficiências", value=st.session_state["proficiencias"], placeholder="Ex: Atirador, Corpo-a-Corpo, Armas Brancas...")

st.header("Estilo de Luta")
estilo_luta = st.text_area("8. Estilo de Luta", value=st.session_state["estilo_luta"], placeholder="Descreva o estilo de luta do personagem...")

st.header("História e Aparência")
historia = st.text_area("9. História", value=st.session_state["historia"], height=200)
aparencia = st.text_area("10. Aparência", value=st.session_state["aparencia"], height=150)

st.header("Armas")
armas = st.text_area("11. Armas", value=st.session_state["armas"], placeholder="Liste as armas utilizadas pelo personagem...")

st.header("Habilidades Passivas")
habilidades_passivas = st.text_area("12. Habilidades Passivas", value=st.session_state["habilidades_passivas"], height=150)

st.header("Ataques Nomeados")
ataques_nomeados = st.text_area("13. Ataques Nomeados", value=st.session_state["ataques_nomeados"], height=150)

st.header("Modo")
modo = st.text_area("14. Modo", value=st.session_state["modo"], placeholder="Descreva o modo especial ou transformação do personagem...")

# ===============================
# MOSTRAR FICHA COMPLETA
# ===============================
st.markdown("---")
if st.button("📄 Mostrar Ficha Completa"):
    st.subheader(f"Ficha de {nome or 'Personagem'}")
    st.write(f"**Título:** {titulo}")
    st.write(f"**Afiliação:** {afiliacao}")
    st.write(f"**Raça:** {raca} ({versao}) — {racas[raca][versao]}")
    st.write(f"**Origem:** {origem}")

    st.markdown("### ❤️ Vida")
    st.write(f"Vida Máxima: {vida_maxima}")
    st.write(f"Vida Atual: {vida_atual}")

    st.markdown("### 🌀 Subatributos")
    st.write(f"Força: {forca}")
    st.write(f"Inteligência: {intelecto}")
    st.write(f"Resistência: {resistencia}")
    st.write(f"Velocidade: {velocidade}")
    st.write(f"Elemento: {elemental}")

    st.markdown("### ✨ Haki")
    st.write(f"Haki do Armamento: {haki_armamento}")
    st.write(f"Haki da Observação: {haki_observacao}")
    st.write(f"Haki do Conquistador/Rei: {haki_conquistador}")

    st.markdown("### ⚔️ Proficiências")
    st.write(proficiencias)
    st.markdown("### 🥋 Estilo de Luta")
    st.write(estilo_luta)
    st.markdown("### 📖 História")
    st.write(historia)
    st.markdown("### 👤 Aparência")
    st.write(aparencia)
    st.markdown("### 🗡️ Armas")
    st.write(armas)
    st.markdown("### 💫 Habilidades Passivas")
    st.write(habilidades_passivas)
    st.markdown("### 🌪️ Ataques Nomeados")
    st.write(ataques_nomeados)
    st.markdown("### 🔥 Modo")
    st.write(modo)

# ===============================
# SALVAR FICHA
# ===============================
ficha_data = {
    "nome": nome,
    "titulo": titulo,
    "afiliacao": afiliacao,
    "raca": raca,
    "versao": versao,
    "origem": origem,
    "vida_maxima": vida_maxima,
    "vida_atual": vida_atual,
    "subatributos": subatributos,
    "proficiencias": proficiencias,
    "estilo_luta": estilo_luta,
    "historia": historia,
    "aparencia": aparencia,
    "armas": armas,
    "habilidades_passivas": habilidades_passivas,
    "ataques_nomeados": ataques_nomeados,
    "modo": modo,
    "haki_armamento": haki_armamento,
    "haki_observacao": haki_observacao,
    "haki_conquistador": haki_conquistador
}

st.markdown("---")
salvar_ficha(ficha_data)
st.caption("Versão 2.0 — Ficha Interativa de Personagem | OnePica RPG")
