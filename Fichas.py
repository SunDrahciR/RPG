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

    "Híbrido": {
        "V1": "O gene predominante define o status.",
        "V2": "A raça secundária começa a se desenvolver."
    }
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
    # DESCRIÇÃO
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

st.session_state["subatributos"]["forca"] = st.session_state.get("sub_forca", 0)
st.session_state["subatributos"]["intelecto"] = st.session_state.get("sub_intelecto", 0)
st.session_state["subatributos"]["resistencia"] = st.session_state.get("sub_resistencia", 0)
st.session_state["subatributos"]["velocidade"] = st.session_state.get("sub_velocidade", 0)
st.session_state["subatributos"]["elemental"] = st.session_state.get("sub_elemental", 0)
st.session_state["subatributos"]["ma"] = st.session_state.get("sub_ma", 0)
st.session_state["subatributos"]["vontade"] = st.session_state.get("sub_vontade", 0)

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
# SALVAR FICHA
# ===============================
sa = st.session_state["subatributos"]

sa["forca"] = st.session_state.get("sub_forca", sa["forca"])
sa["intelecto"] = st.session_state.get("sub_intelecto", sa["intelecto"])
sa["resistencia"] = st.session_state.get("sub_resistencia", sa["resistencia"])
sa["velocidade"] = st.session_state.get("sub_velocidade", sa["velocidade"])
sa["elemental"] = st.session_state.get("sub_elemental", sa["elemental"])
sa["ma"] = st.session_state.get("sub_ma", sa["ma"])
sa["vontade"] = st.session_state.get("sub_vontade", sa["vontade"])

ficha_data = {
    "nome": nome,
    "titulo": titulo,
    "afiliacao": afiliacao,
    "raca": st.session_state["raca"],
    "versao": st.session_state["versao"],
    "origem": origem,
    "vida_maxima": vida_maxima,
    "vida_atual": vida_atual,
    "subatributos": st.session_state["subatributos"],
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


































