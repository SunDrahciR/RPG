import streamlit as st
import json
from io import StringIO

# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(page_title="Ficha de Personagem - OnePica RPG", layout="wide")

st.title("Ficha de Personagem - One Pica RPG")

modo_visual = st.toggle("Modo Leitura", value=False)

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
            "forca": 0,
            "intelecto": 0,
            "resistencia": 0,
            "velocidade": 0,
            "elemental": 0,
            "ma": 0,
            "vontade": 0
        }

# ===============================
# SIDEBAR — GERENCIAR FICHA
# ===============================
st.sidebar.header("Gerenciar Ficha")
upload = st.sidebar.file_uploader("Carregar Ficha (.json)", type="json")

if upload is not None:
    try:
        dados_carregados = carregar_ficha(upload)
        for key, value in dados_carregados.items():
            st.session_state[key] = value
        st.sidebar.success("Ficha carregada com sucesso! Os campos foram atualizados.")
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar ficha: {e}")

# ===============================
# PAINEL PRINCIPAL DA FICHA
# ===============================

colA, colB, colC = st.columns([1.2, 1.4, 1.4])

# IDENTIDADE
with colA:
    with st.container(border=True):
        st.subheader("Identidade")

        if modo_visual:
            st.markdown(f"## {st.session_state['nome'] or 'Sem Nome'}")
            st.caption(st.session_state['titulo'] or "—")
            st.write(f"**Afiliação:** {st.session_state['afiliacao'] or '—'}")
            st.write(f"**Origem:** {st.session_state['origem'] or '—'}")
        else:
            nome = st.text_input("Nome", value=st.session_state["nome"])
            titulo = st.text_input("Título", value=st.session_state["titulo"])
            afiliacao = st.text_input("Afiliação", value=st.session_state["afiliacao"])
            origem = st.text_input("Origem", value=st.session_state["origem"])

# ===============================
# RAÇAS
# ===============================
st.markdown("---")

with st.container(border=True):
    st.subheader("🧬 Raça")

    # Seleção principal (ESSA é a fonte da verdade)
    col1, col2 = st.columns(2)

    with col1:
        raca = st.selectbox(
            "Raça",
            list(racas.keys()),
            index=list(racas.keys()).index(st.session_state["raca"])
            if st.session_state["raca"] else 0,
            key="raca_select"
        )

    with col2:
        versao = st.selectbox(
            "Versão da Raça",
            ["V1", "V2", "V3"],
            index=["V1", "V2", "V3"].index(st.session_state["versao"])
            if st.session_state["versao"] else 0,
            key="versao_raca_select"
        )

    # Salva no session_state (importante)
    st.session_state["raca"] = raca
    st.session_state["versao"] = versao

    # ===============================
    # HÍBRIDO
    # ===============================
    if raca == "Híbrido":
        racas_base = [r for r in racas.keys() if r != "Híbrido"]
        colH1, colH2 = st.columns(2)

        with colH1:
            raca1 = st.selectbox(
                "Raça Primária",
                racas_base,
                key="hibrido_raca_primaria"
            )
            versao1 = st.selectbox(
                "Versão da Raça Primária",
                ["V1", "V2"],
                key="hibrido_versao_primaria"
            )

        with colH2:
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

    # ===============================
    # DESCRIÇÃO (NÃO SOME!)
    # ===============================
    if raca and raca != "Híbrido":
        with st.expander("📜 Descrição da Raça"):
            descricao = descricao_raca_progressiva(racas, raca, versao)
            st.markdown(descricao)
            st.markdown(f"**Fraqueza:** {racas[raca]['Fraqueza']}")



#VIDA + SUBATRIBUTOS
with colB:
    with st.container(border=True):
        st.subheader("Vida")

        vida_maxima = int(st.session_state["vida_maxima"] or 100)
        vida_atual = int(st.session_state["vida_atual"] or vida_maxima)

        if modo_visual:
            st.metric("Vida", f"{vida_atual} / {vida_maxima}")
        else:
            vida_maxima = st.number_input("Vida Máxima", min_value=1, value=vida_maxima, step=10)
            vida_atual = st.number_input("Vida Atual", min_value=0, max_value=vida_maxima, value=vida_atual)

    with st.container(border=True):
        st.subheader("🌀 Subatributos")

        sa = st.session_state["subatributos"]

        if modo_visual:
            c1, c2, c3 = st.columns(3)
            c1.metric("FOR", sa["forca"])
            c1.metric("INT", sa["intelecto"])
            c2.metric("RES", sa["resistencia"])
            c2.metric("VEL", sa["velocidade"])
            c3.metric("ELE", sa["elemental"])
            c3.metric("M.A", sa["ma"])
            c3.metric("VON", sa["vontade"])
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.number_input("Força", min_value=0, step=1, key="sub_forca")
                st.number_input("Intelecto", min_value=0, step=1, key="sub_intelecto")
            with c2:
                st.number_input("Resistência", min_value=0, step=1, key="sub_resistencia")
                st.number_input("Velocidade", min_value=0, step=1, key="sub_velocidade")
            with c3:
                st.number_input("Elemento", min_value=0, step=1, key="sub_elemental")
                st.number_input("M.A", min_value=0, step=1, key="sub_ma")
                st.number_input("Vontade", min_value=0, step=1, key="sub_vontade")

# HAKI
with colC:
    with st.container(border=True):
        st.subheader("Haki")

        if modo_visual:
            st.write(f" **Armamento:** {haki_armamento}")
            st.write(f" **Observação:** {haki_observacao}")
            st.write(f" **Conquistador:** {haki_conquistador}")
        else:
            haki_armamento = st.selectbox(
                "Haki do Armamento",
                ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
                key="haki_armamento"
            )
            haki_observacao = st.selectbox(
                "Haki da Observação",
                ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
                key="haki_observacao"
            )
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

    st.markdown("###  Vida")
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





























