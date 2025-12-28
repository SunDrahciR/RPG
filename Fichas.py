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
    "Humano": {
        "V1": "Ganha mais bônus ao upar sub-atributos (mestre decide o quanto).",
        "V2": "Os Hakis recebem +5.",
        "V3": "+5 nos Hakis e +10 em todos os Subatributos",
        "Fraqueza": "Quando a Raça do inimigo for maior que a sua, leva +10 de Dano"
    },

    "Tribo (Braço/Perna Longos)": {
        "V1": "Golpes com o membro respectivo recebem +7 em acerto.",
        "V2": "+13 de Dano com o membro, ataques com o membro são considerados Grandes",
        "V3": "+12 de Dano e +20 de Defesa com o membro. (Total: +25 de Dano, +7 de Acerto, Ataques Grandes)",
        "Fraqueza": "Golpes mirando nos membros longos tem +10 de Acerto"
    },

    "Tontata": {
        "V1": "+15 em Esquiva e Furtividade",
        "V2": "+23 em Esquiva e Furtividade (Total: +38)",
        "V3": "+2 em Esquiva e Furtividade e ignora a imunidade a Furtividade do Haki da Observação (Total: +40)",
        "Fraqueza": "-5 de Resistência, 19 também arranca membro"
    },

    "Homem-Peixe": {
        "V1": "Dentro da água, seus dados são dobrados.",
        "V2": "Dentro da água, seus dados são triplicados.",
        "V3": "Dentro da água, Força e Resistência são dobradas.",
        "Fraqueza": "Em ambientes secos, todos os resultados são cortados pela metade."
    },

    "Nativo do Céu": {
        "V1": "+15 em testes e ações aéreas.",
        "V2": "Em combate aéreo, o D20 é dobrado e recebe +10 de movimento no ar.",
        "V3": "Todos os resultados de movimento aéreo são dobrados.",
        "Fraqueza": "Enquanto estiver no ar, recebe +25 de dano elétrico."
    },

    "Oni": {
        "V1": "+15 de dano em ambientes de fogo.",
        "V2": "Em ambientes de fogo, o D20 é dobrado e causa +10 de dano.",
        "V3": "Em ambientes de fogo, o D20 é quadruplicado.",
        "Fraqueza": "Em ambientes de baixa temperatura, recebe -15 em Força e Resistência."
    },

    "Sereiano": {
        "V1": "Dentro da água, recebe +25 de movimento.",
        "V2": "Dentro da água, recebe 3D20 adicionais de movimento.",
        "V3": "Dentro da água, todos os dados de movimento e ataque são dobrados.",
        "Fraqueza": "Fora da água, não recebe bônus e fica incapacitado de se mover."
    },

    "Mink": {
        "V1": "+14 de movimentação e rastreamento. No Modo Sulong: +35 de dano e Velocidade.",
        "V2": "+16 de movimentação e rastreamento.",
        "V3": "+20 de movimentação e rastreamento. No Modo Sulong: +15 adicionais de dano e Velocidade.",
        "Fraqueza": "Ataques Sonoros ou Venenosos causam +30 de dano."
    },

    "Gigante": {
        "V1": "+15 em Força e Resistência. Todos os golpes são Grandes.",
        "V2": "+30 em Força e Resistência. Todos os golpes são Gigantes.",
        "V3": "Golpes físicos se tornam ataques em área. +10 de dano por alvo adicional.",
        "Fraqueza": "Todos os inimigos recebem +40 em testes de acerto contra Gigantes."
    },

    "Lunariano": {
        "V1": "Chamas acesas: +20 de Resistência. Chamas apagadas: +20 de Velocidade.",
        "V2": "Os bônus aumentam adicionalmente em +25.",
        "V3": "Os bônus aumentam adicionalmente em +5 e pode alternar o estado das chamas como Reação.",
        "Fraqueza": "Com as chamas apagadas, recebe dano proporcional ao bônus ativo."
    },

    "Bucaneiro": {
        "V1": "+22 de Resistência.",
        "V2": "Não é afetado por condições especiais de Grau 1.",
        "V3": "+28 de Resistência e não é afetado por condições especiais de Grau 2.",
        "Fraqueza": "Se um aliado perder membros, o Bucaneiro sofre Confusão Grau 3."
    },

    "Híbrido": {"V1": "O gene predominante define o status.", "V2": "A raça secundária começa a se desenvolver."},
}

def descricao_raca_progressiva(racas, raca, versao):
    textos = []

    if versao == "V1":
        textos.append(racas[raca]["V1"])

    elif versao == "V2":
        textos.append(racas[raca]["V1"])
        textos.append(racas[raca]["V2"])

    elif versao == "V3":
        textos.append(racas[raca]["V1"])
        textos.append(racas[raca]["V2"])
        textos.append(racas[raca]["V3"])

    return "\n".join(textos)
    
col1, col2 = st.columns(2)
with col1:
    raca = st.selectbox("4. Raça", list(racas.keys()), index=list(racas.keys()).index(st.session_state["raca"]) if st.session_state["raca"] else 0)
with col2:
    versao = st.selectbox(
    "Versão da Raça",
    ["V1", "V2", "V3"],
    index=["V1","V2","V3"].index(st.session_state["versao"]) if st.session_state["versao"] else 0)
        
if raca == "Híbrido":
    
    racas_base = [r for r in racas.keys() if r != "Híbrido"]
    col1, col2 = st.columns(2)
    with col1:
        raca1 = st.selectbox(
            "Raça Primária",
            racas_base,
            key= "hibrido_raca_primaria"
        )
        versao1 = st.selectbox(
            "Versão da Raça Primária",
            ["V1", "V2"],
             key = "hibrido_versao_primaria"
        )
    with col2:
        racas_secundarias = [r for r in racas_base if r != raca1]
        raca2 = st.selectbox(
            "Raça Secundária",
            racas_secundarias,
            key="hibrido_raca_secundaria"
        )
        versao2 = st.selectbox(
            "Versão da Raça Secundária",
            ["V1", "V2"],
            key="hibrido_versao_secundaria"
        )

    st.info(
        f"🔹 **Primária:** {raca1} ({versao1})\n\n"
        f"🔸 **Secundária:** {raca2} ({versao2})"
    )

if raca and raca != "Híbrido":
    st.markdown(f"**Descrição da Raça ({raca} - {versao})**")

    descricao = descricao_raca_progressiva(racas, raca, versao)

    st.info(
        f"{descricao}\n\n"
        f"**Fraqueza:** {racas[raca]['Fraqueza']}"
    )



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
    haki_armamento = st.selectbox(
        "Haki do Armamento",
        ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
        key="haki_armamento"
    )
with col2:
    haki_observacao = st.selectbox(
        "Haki da Observação",
        ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
        key="haki_observacao"
    )
with col3:
    haki_conquistador = st.selectbox(
        "Haki do Conquistador/Rei",
        ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
        key="haki_conquistador"
    )

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














