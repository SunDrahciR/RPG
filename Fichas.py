import streamlit as st
import json
from io import StringIO
from io import BytesIO

# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(page_title="Ficha de Personagem - OnePica RPG", layout="wide")

st.title("Ficha de Personagem - One Pica RPG")

st.markdown("""
<style>
img {
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.avatar-img div img {
    transition: 0.25s ease;
    cursor: pointer;
}

.avatar-img div img:hover {
    transform: scale(2.2);
    position: relative;
    z-index: 999;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.avatar-img {
    overflow: visible !important;
}
</style>
""", unsafe_allow_html=True)



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
    data = json.load(stringio)

    # Campos simples
    for campo in [
        "nome", "titulo", "afiliacao", "origem",
        "vida_maxima", "vida_atual",
        "proficiencias", "estilo_luta",
        "historia", "aparencia", "anotacoes"
    ]:
        if campo in data:
            st.session_state[campo] = data[campo]

    if "imagem" in data and data["imagem"]:
        st.session_state["imagem_personagem"] = BytesIO(data["imagem"].encode("latin1"))

    # Raça
    st.session_state["raca"] = data.get("raca", "")
    st.session_state["versao"] = data.get("versao", "V1")
    st.session_state["raca_select"] = st.session_state["raca"]
    st.session_state["versao_raca_select"] = st.session_state["versao"]

    # Subatributos
    st.session_state["subatributos"] = data.get("subatributos", {
        "forca": 0,
        "intelecto": 0,
        "resistencia": 0,
        "velocidade": 0,
        "elemental": 0,
        "ma": 0,
        "vontade": 0
    })

    for k, v in st.session_state["subatributos"].items():
        st.session_state[f"sub_{k}"] = v

    # Haki
    st.session_state["haki_armamento"] = data.get("haki_armamento", "Nenhum")
    st.session_state["haki_observacao"] = data.get("haki_observacao", "Nenhum")
    st.session_state["haki_conquistador"] = data.get("haki_conquistador", "Nenhum")

    # Listas
    if "passivas" in data:
        st.session_state["passivas"] = data["passivas"].copy()

    if "habilidades" in data:
        st.session_state["habilidades"] = data["habilidades"].copy()
    
    if "ataques" in data:
        st.session_state["ataques"] = data["ataques"].copy()
    
    if "modos" in data:
        st.session_state["modos"] = data["modos"].copy()
    
    if "arsenal" in data:
        st.session_state["arsenal"] = data["arsenal"].copy()
    return data


# ===============================
# INICIALIZAÇÃO DO SESSION STATE
# ===============================
chaves = [
    "nome", "titulo", "afiliacao", "origem",
    "raca", "versao",
    "vida_maxima", "vida_atual",
    "proficiencias", "estilo_luta",
    "historia", "aparencia", "anotacoes"
]

if "imagem_personagem" not in st.session_state:
    st.session_state["imagem_personagem"] = None

if "anotacoes" not in st.session_state:
    st.session_state["anotacoes"] = ""

if "raca" not in st.session_state:
    st.session_state["raca"] = ""

if "versao" not in st.session_state:
    st.session_state["versao"] = "V1"

if "subatributos" not in st.session_state:
    st.session_state["subatributos"] = {
        "forca": 0,
        "intelecto": 0,
        "resistencia": 0,
        "velocidade": 0,
        "elemental": 0,
        "ma": 0,
        "vontade": 0
    }

for key, default in {
    "passivas": [],
    "habilidades": [],
    "ataques": [],
    "modos": [],
    "arsenal": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default.copy()

for haki in ["haki_armamento", "haki_observacao", "haki_conquistador"]:
    if haki not in st.session_state:
        st.session_state[haki] = "Nenhum"

if "vida_maxima" not in st.session_state or not isinstance(st.session_state["vida_maxima"], int):
    st.session_state["vida_maxima"] = 100

if "vida_atual" not in st.session_state or not isinstance(st.session_state["vida_atual"], int):
    st.session_state["vida_atual"] = 100


# ===============================
# SIDEBAR — GERENCIAR FICHA
# ===============================
st.sidebar.header("Gerenciar Ficha")
upload = st.sidebar.file_uploader("Carregar Ficha (.json)", type="json")

if upload is not None:
    try:
        dados_carregados = carregar_ficha(upload)
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
        col_img, col_info = st.columns([1, 2])

        #Imagem
        with col_img:
            if st.session_state.get("imagem_personagem"):
                st.markdown('<div class="avatar-img">', unsafe_allow_html=True)
                st.image(st.session_state["imagem_personagem"], width=120)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("### 👤")
        
            if st.button("Imagem"):
                st.session_state["mostrar_upload"] = True
        
            if st.session_state.get("mostrar_upload"):
                imagem = st.file_uploader(
                    "",
                    type=["png", "jpg", "jpeg", "webp"],
                    key="upload_imagem"
                )
        
                if imagem:
                    st.session_state["imagem_personagem"] = imagem
                    st.session_state["mostrar_upload"] = False

        #Info
        with col_info:
            st.text_input("Nome", key="nome")
            st.text_input("Título", key="titulo")
            st.text_input("Afiliação", key="afiliacao")
            st.text_input("Origem", key="origem")

# ===============================
# RAÇAS
# ===============================
st.header("Raça")

racas = {
    "Humano": {
        "V1": "Ganha 50% a mais de Atributo em relação ao Arco",
        "V2": "Os Hakis recebem +10.",
        "V3": " +10 nos Hakis e ganham 50% a mais em todos os Subatributos",
        "Fraqueza": " Leva 25% de dano a mais caso o atacante tenha uma raça de nível superior"
    },

    "Tribo (Braço/Perna Longos)": {
        "V1": "Golpes com o membro respectivo recebem +14 em acerto.",
        "V2": "Ganha 1d20 a mais em ações com o membro, ataques com o membro são considerados Grandes",
        "V3": " Ganha +1d20 com o membro e +30 de Defesa com o membro",
        "Fraqueza": "Golpes mirando nos membros longos tem um bônus equivalente a Grande no Acerto"
    },

    "Tontata": {
        "V1": "+15 em Esquiva e Furtividade",
        "V2": "+23 em Esquiva e Furtividade e ignora a imunidade a Furtividade do Haki da Observação, desde que o nivel de Haki do Tontata seja superior ou equivalente",
        "V3": "+22 em Esquiva e Furtividade",
        "Fraqueza": " Ataques direcionados a um Tontata recebem um bônus equivalente a Grande em Dano e Acerto"
    },

    "Homem-Peixe": {
        "V1": "Dentro da água, seus dados são dobrados.",
        "V2": "Dentro da água, seus dados são triplicados.",
        "V3": "Dentro da água, Força e Resistência são dobradas.",
        "Fraqueza": "Em ambientes secos, todos os resultados são cortados pela metade."
    },

    "Nativo do Céu": {
        "V1": "+25 em Aéreo",
        "V2": "D20 é triplicado no ar e recebe +20 em Movimentação Aérea",
        "V3": "Todos os resultados de movimento aéreo são triplicados.",
        "Fraqueza": "Leva o dobro de dano elétrico estando no ar."
    },

    "Oni": {
        "V1": "+25 de dano em ambientes de fogo.",
        "V2": "Em ambientes de fogo, o D20 é triplicado e causa +25 de dano.",
        "V3": "Em ambientes de fogo, o D20 é quadruplicado.",
        "Fraqueza": "Em ambientes de baixa temperatura, todos os resultados são cortados pela metade."
    },

    "Sereiano": {
        "V1": "Dentro da água, d20 de movimento é dobrado.",
        "V2": "Dentro da água, recebe +50 em Força, Elemento e Velocidade",
        "V3": "Dentro da água, todos os dados de movimento e ataque são dobrados.",
        "Fraqueza": "Fora da água, não recebe bônus"
    },

    "Mink": {
        "V1": "+20 de movimentação e rastreamento. No Modo Sulong: +35 em atributos físicos e elemental e os atributos base são dobrados",
        "V2": "+20 de movimentação e rastreamento.",
        "V3": "+30 de movimentação e rastreamento. No Modo Sulong: +15 adicionais de dano e Velocidade.",
        "Fraqueza": "Ataques Sonoros ou Venenosos causam +30 de dano."
    },

    "Gigante": {
        "V1": "+25 em Força e Resistência. Todos os golpes são Grandes.",
        "V2": "+45 em Força e Resistência. Todos os golpes são Gigantes.",
        "V3": "Todos os golpes físicos são em área, e pra cada pessoa na área é +25 de dano.",
        "Fraqueza": "Todos tem +20 a cada nivel da raça para acertar um Gigante "
    },

    "Lunariano": {
        "V1": "Chamas acesas: +30 de Resistência. Chamas apagadas: +30 de Velocidade.",
        "V2": "Os bônus aumentam adicionalmente em +20.",
        "V3": "Os bônus aumentam em +20 e pode alternar o estado das chamas como Reação.",
        "Fraqueza": "Com as chamas apagadas, leva o dobro de dano."
    },

    "Bucaneiro": {
        "V1": "+40 de Resistência.",
        "V2": "+30 de Resistência e não é afetado por condições especiais de Grau 1.",
        "V3": "+30 de Resistência e não é afetado por condições especiais de Grau 2.",
        "Fraqueza": "Se um aliado perder membros, o Bucaneiro sofre Confusão Grau 3 e Paralisia Grau 3."
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
    st.subheader("Raça")

    col1, col2 = st.columns(2)

    with col1:
        raca_keys = list(racas.keys())

        raca = st.selectbox(
            "Raça",
            raca_keys,
            index=raca_keys.index(st.session_state["raca"])
            if st.session_state.get("raca") in raca_keys
            else 0,
            key="raca_select"
        )

    with col2:
        versoes = ["V1", "V2", "V3"]

        versao = st.selectbox(
            "Versão da Raça",
            versoes,
            index=versoes.index(st.session_state["versao"])
            if st.session_state.get("versao") in versoes
            else 0,
            key="versao_raca_select"
        )

    
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
        with st.expander("Descrição da Raça"):
            descricao = descricao_raca_progressiva(racas, raca, versao)
            st.markdown(descricao)
            st.markdown(f"**Fraqueza:** {racas[raca]['Fraqueza']}")



#VIDA + SUBATRIBUTOS
with colB:
    with st.container(border=True):
        st.subheader("Vida")

        vida_maxima = st.number_input(
            "Vida Máxima",
            min_value=1,
            step=10,
            value=st.session_state.get("vida_maxima", 100),
            key="vida_maxima"
        )

        vida_atual = st.number_input(
            "Vida Atual",
            min_value=0,
            max_value=st.session_state["vida_maxima"],
            value=min(
                st.session_state.get("vida_atual", vida_maxima),
                st.session_state["vida_maxima"]
            ),
            key="vida_atual"
        )

    for k, v in st.session_state["subatributos"].items():
        if f"sub_{k}" not in st.session_state:
            st.session_state[f"sub_{k}"] = v
      
    with st.container(border=True):
        st.subheader("Subatributos")

        sa = st.session_state["subatributos"]
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

if "sub_forca" in st.session_state:
    st.session_state["subatributos"]["forca"] = st.session_state["sub_forca"]

if "sub_intelecto" in st.session_state:
    st.session_state["subatributos"]["intelecto"] = st.session_state["sub_intelecto"]

if "sub_resistencia" in st.session_state:
    st.session_state["subatributos"]["resistencia"] = st.session_state["sub_resistencia"]

if "sub_velocidade" in st.session_state:
    st.session_state["subatributos"]["velocidade"] = st.session_state["sub_velocidade"]

if "sub_elemental" in st.session_state:
    st.session_state["subatributos"]["elemental"] = st.session_state["sub_elemental"]

if "sub_ma" in st.session_state:
    st.session_state["subatributos"]["ma"] = st.session_state["sub_ma"]

if "sub_vontade" in st.session_state:
    st.session_state["subatributos"]["vontade"] = st.session_state["sub_vontade"]

# HAKI
with colC:
    with st.container(border=True):
        st.subheader("Haki")
    
        st.selectbox(
            "Haki do Armamento",
            ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
            key="haki_armamento"
        )
    
        st.selectbox(
            "Haki da Observação",
            ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
            key="haki_observacao"
        )
    
        st.selectbox(
            "Haki do Conquistador/Rei",
            ["Nenhum", "V1", "V2", "V3", "V4", "V5"],
            key="haki_conquistador"
        )
        with st.container(border=True):
            st.subheader("Anotações")
    
            st.text_area(
                "Anotações de Combate / Observações",
                key="anotacoes",
                height=180
            )

#APTIDÕES
st.markdown("---")
st.header("Habilidades do Personagem")

tab_passivas, tab_habilidades, tab_ataques, tab_modos = st.tabs(
    ["Passivas", "Habilidades", "Ataques", "Modos"]
)

# ===============================
# PASSIVAS
# ===============================

def adicionar_passiva():
    nome = st.session_state["nova_passiva_nome"]
    desc = st.session_state["nova_passiva_desc"]

    if nome.strip():
        st.session_state["passivas"].append({
            "nome": nome,
            "descricao": desc
        })
        st.session_state["nova_passiva_nome"] = ""
        st.session_state["nova_passiva_desc"] = ""

with tab_passivas:
    st.subheader("Passivas")

    with st.expander("➕ Nova Passiva"):
        st.text_input("Nome", key="nova_passiva_nome")
        st.text_area("Descrição", key="nova_passiva_desc", height=120)

        st.button("Adicionar Passiva", on_click=adicionar_passiva)

    for i, p in enumerate(st.session_state["passivas"]):
        with st.expander(p["nome"]):

            key_nome = f"edit_passiva_nome_{i}"
            key_desc = f"edit_passiva_desc_{i}"

            if key_nome not in st.session_state:
                st.session_state[key_nome] = p["nome"]

            if key_desc not in st.session_state:
                st.session_state[key_desc] = p["descricao"]

            st.text_input("Nome", key=key_nome)
            st.text_area("Descrição", key=key_desc, height=120)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Salvar", key=f"save_passiva_{i}"):
                    st.session_state["passivas"][i] = {
                        "nome": st.session_state[key_nome],
                        "descricao": st.session_state[key_desc]
                    }
                    st.rerun()

            with col2:
                if st.button("🗑 Remover", key=f"del_passiva_{i}"):
                    st.session_state["passivas"].pop(i)
                    st.rerun()

# ===============================
# HABILIDADES
# ===============================

def adicionar_habilidade():
    nome = st.session_state["nova_hab_nome"]
    desc = st.session_state["nova_hab_desc"]

    if nome.strip():
        st.session_state["habilidades"].append({
            "nome": nome,
            "descricao": desc
        })
        st.session_state["nova_hab_nome"] = ""
        st.session_state["nova_hab_desc"] = ""

with tab_habilidades:
    st.subheader("Habilidades")

    with st.expander("➕ Nova Habilidade"):
        st.text_input("Nome", key="nova_hab_nome")
        st.text_area("Descrição", key="nova_hab_desc", height=120)

        st.button("Adicionar Habilidade", on_click=adicionar_habilidade)

    for i, h in enumerate(st.session_state["habilidades"]):
        with st.expander(h["nome"]):

            key_nome = f"edit_hab_nome_{i}"
            key_desc = f"edit_hab_desc_{i}"

            if key_nome not in st.session_state:
                st.session_state[key_nome] = h["nome"]

            if key_desc not in st.session_state:
                st.session_state[key_desc] = h["descricao"]

            st.text_input("Nome", key=key_nome)
            st.text_area("Descrição", key=key_desc, height=120)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Salvar", key=f"save_hab_{i}"):
                    st.session_state["habilidades"][i] = {
                        "nome": st.session_state[key_nome],
                        "descricao": st.session_state[key_desc]
                    }
                    st.rerun()

            with col2:
                if st.button("🗑 Remover", key=f"del_hab_{i}"):
                    st.session_state["habilidades"].pop(i)
                    st.rerun()
# ===============================
# ATAQUES
# ===============================

def adicionar_ataque():
    nome = st.session_state["novo_atk_nome"]
    bonus = st.session_state["novo_atk_bonus"]
    tipo = st.session_state["novo_atk_tipo"]
    desc = st.session_state["novo_atk_desc"]

    if nome.strip():
        st.session_state["ataques"].append({
            "nome": nome,
            "bonus": bonus,
            "tipo": tipo,
            "descricao": desc
        })

        st.session_state["novo_atk_nome"] = ""
        st.session_state["novo_atk_bonus"] = ""
        st.session_state["novo_atk_tipo"] = ""
        st.session_state["novo_atk_desc"] = ""

with tab_ataques:
    st.subheader("Ataques")

    with st.expander("➕ Novo Ataque"):
        st.text_input("Nome", key="novo_atk_nome")
        st.text_input("Bônus", key="novo_atk_bonus")
        st.text_input("Tipo", key="novo_atk_tipo")
        st.text_area("Descrição", key="novo_atk_desc", height=120)

        st.button("Adicionar Ataque", on_click=adicionar_ataque)

    for i, a in enumerate(st.session_state["ataques"]):
        header = f"{a['nome']} | {a['bonus']} | {a['tipo']}"

        with st.expander(header):

            key_nome = f"edit_atk_nome_{i}"
            key_bonus = f"edit_atk_bonus_{i}"
            key_tipo = f"edit_atk_tipo_{i}"
            key_desc = f"edit_atk_desc_{i}"

            if key_nome not in st.session_state:
                st.session_state[key_nome] = a["nome"]

            if key_bonus not in st.session_state:
                st.session_state[key_bonus] = a["bonus"]

            if key_tipo not in st.session_state:
                st.session_state[key_tipo] = a["tipo"]

            if key_desc not in st.session_state:
                st.session_state[key_desc] = a["descricao"]

            st.text_input("Nome", key=key_nome)
            st.text_input("Bônus", key=key_bonus)
            st.text_input("Tipo", key=key_tipo)
            st.text_area("Descrição", key=key_desc, height=120)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Salvar", key=f"save_atk_{i}"):
                    st.session_state["ataques"][i] = {
                        "nome": st.session_state[key_nome],
                        "bonus": st.session_state[key_bonus],
                        "tipo": st.session_state[key_tipo],
                        "descricao": st.session_state[key_desc]
                    }
                    st.rerun()

            with col2:
                if st.button("🗑 Remover", key=f"del_atk_{i}"):
                    st.session_state["ataques"].pop(i)
                    st.rerun()

# ===============================
# MODOS
# ===============================

def adicionar_modo():
    nome = st.session_state["novo_modo_nome"]
    cond = st.session_state["novo_modo_condicao"]
    efeito = st.session_state["novo_modo_efeito"]
    desc = st.session_state["novo_modo_desc"]

    if nome.strip():
        st.session_state["modos"].append({
            "nome": nome,
            "condicao": cond,
            "efeito": efeito,
            "descricao": desc
        })

        st.session_state["novo_modo_nome"] = ""
        st.session_state["novo_modo_condicao"] = ""
        st.session_state["novo_modo_efeito"] = ""
        st.session_state["novo_modo_desc"] = ""
        
with tab_modos:
    st.subheader("Modos")

    with st.expander("➕ Novo Modo"):
        st.text_input("Nome", key="novo_modo_nome")
        st.text_input("Condição", key="novo_modo_condicao")
        st.text_input("Efeito / Bônus", key="novo_modo_efeito")
        st.text_area("Descrição", key="novo_modo_desc", height=120)

        st.button(
            "Adicionar Modo",
            key="btn_add_modo",
            on_click=adicionar_modo
        )

    for i, m in enumerate(st.session_state["modos"]):
        with st.expander(m["nome"]):

            key_nome = f"edit_modo_nome_{i}"
            key_cond = f"edit_modo_cond_{i}"
            key_efeito = f"edit_modo_efeito_{i}"
            key_desc = f"edit_modo_desc_{i}"
        
            if key_nome not in st.session_state:
                st.session_state[key_nome] = m["nome"]
        
            if key_cond not in st.session_state:
                st.session_state[key_cond] = m["condicao"]
        
            if key_efeito not in st.session_state:
                st.session_state[key_efeito] = m["efeito"]
        
            if key_desc not in st.session_state:
                st.session_state[key_desc] = m["descricao"]
        
            st.text_input("Nome", key=key_nome)
            st.text_input("Condição", key=key_cond)
            st.text_input("Efeito", key=key_efeito)
            st.text_area("Descrição", key=key_desc, height=120)
        
            col1, col2 = st.columns(2)
        
            with col1:
                if st.button("💾 Salvar", key=f"save_modo_{i}"):
                    st.session_state["modos"][i] = {
                        "nome": st.session_state[key_nome],
                        "condicao": st.session_state[key_cond],
                        "efeito": st.session_state[key_efeito],
                        "descricao": st.session_state[key_desc]
                    }
                    st.rerun()
        
            with col2:
                if st.button("🗑 Remover", key=f"del_modo_{i}"):
                    st.session_state["modos"].pop(i)
                    st.rerun()

    # ===============================
    # ARSENAL
    # ===============================

GRAUS_ARSENAL = {
    4: {"bonus": 8, "ma": 0},
    3: {"bonus": 15, "ma": 10},
    2: {"bonus": 23, "ma": 20},
    1: {"bonus": 35, "ma": 35},
}

def calcular_arsenal(grau, amaldicoada):
    bonus = GRAUS_ARSENAL[grau]["bonus"]
    ma = GRAUS_ARSENAL[grau]["ma"]

    if amaldicoada:
        bonus += 15
        ma += 10

    return bonus, ma

def add_arsenal():
    nome = st.session_state.get("novo_arsenal_nome", "").strip()
    tipo = st.session_state.get("novo_arsenal_tipo", "").strip()
    grau = st.session_state.get("novo_arsenal_grau", 4)
    amaldicoada = st.session_state.get("novo_arsenal_amaldicoada", False)
    despertada = st.session_state.get("novo_arsenal_despertada", False)
    habilidade = st.session_state.get("novo_arsenal_habilidade", "")
    descricao = st.session_state.get("novo_arsenal_desc", "")

    if not nome:
        return

    bonus, ma = calcular_arsenal(grau, amaldicoada)

    st.session_state["arsenal"].append({
        "nome": nome,
        "tipo": tipo,
        "grau": grau,
        "bonus": bonus,
        "ma_requerido": ma,
        "amaldicoada": amaldicoada,
        "despertada": despertada if grau == 1 else False,
        "habilidade_despertada": habilidade if despertada else "",
        "descricao": descricao
    })

    st.session_state["novo_arsenal_nome"] = ""
    st.session_state["novo_arsenal_tipo"] = ""
    st.session_state["novo_arsenal_desc"] = ""
    st.session_state["novo_arsenal_amaldicoada"] = False
    st.session_state["novo_arsenal_despertada"] = False
    st.session_state["novo_arsenal_habilidade"] = ""

    st.rerun()

st.markdown("---")
st.header("Arsenal")

with st.container(border=True):
    st.subheader("Equipamentos de Combate")

    with st.expander("➕ Novo Arsenal", expanded=True):

        st.text_input(
            "Nome do Arsenal",
            key="novo_arsenal_nome"
        )

        st.text_input(
            "Tipo (Espada, Arma de Fogo, etc)",
            key="novo_arsenal_tipo"
        )

        st.selectbox(
            "Grau do Arsenal",
            [4, 3, 2, 1],
            format_func=lambda g: f"Grau {g}",
            key="novo_arsenal_grau"
        )

        st.checkbox(
            "Arsenal Amaldiçoado (+15 bônus, +10 M.A.)",
            key="novo_arsenal_amaldicoada"
        )

        if st.session_state.get("novo_arsenal_grau") == 1:
            st.checkbox(
                "Grau 1 Despertado",
                key="novo_arsenal_despertada"
            )

            if st.session_state.get("novo_arsenal_despertada"):
                st.text_area(
                    "Habilidade Despertada do Arsenal",
                    height=100,
                    key="novo_arsenal_habilidade"
                )

        bonus, ma = calcular_arsenal(
            st.session_state.get("novo_arsenal_grau", 4),
            st.session_state.get("novo_arsenal_amaldicoada", False)
        )

        st.markdown(
            f"""
            **Bônus Total:** +{bonus}  
            **M.A. Requerido:** {ma}
            """
        )

        st.text_area(
            "Descrição Geral",
            height=120,
            key="novo_arsenal_desc"
        )

        st.button(
            "Adicionar Arsenal",
            on_click=add_arsenal
        )

if st.session_state["arsenal"]:
    st.subheader("Arsenais Equipados")

    for i, a in enumerate(st.session_state["arsenal"]):

        key_nome = f"edit_arsenal_nome_{i}"
        key_tipo = f"edit_arsenal_tipo_{i}"
        key_grau = f"edit_arsenal_grau_{i}"
        key_despertada = f"edit_arsenal_despertada_{i}"
        key_hab_despertada = f"edit_arsenal_hab_{i}"
        key_amald = f"edit_arsenal_amald_{i}"
        key_desc = f"edit_arsenal_desc_{i}"
    
        if key_nome not in st.session_state:
            st.session_state[key_nome] = a["nome"]
    
        if key_tipo not in st.session_state:
            st.session_state[key_tipo] = a["tipo"]
    
        if key_grau not in st.session_state:
            st.session_state[key_grau] = a["grau"]
    
        if key_amald not in st.session_state:
            st.session_state[key_amald] = a["amaldicoada"]

        if key_despertada not in st.session_state:
            st.session_state[key_despertada] = a.get("despertada", False)

        if key_hab_despertada not in st.session_state:
            st.session_state[key_hab_despertada] = a.get("habilidade_despertada", "")
    
        if key_desc not in st.session_state:
            st.session_state[key_desc] = a["descricao"]
    
        titulo = f"{st.session_state[key_nome]} | Grau {st.session_state[key_grau]}"

        with st.expander(titulo):
    
            st.text_input("Nome", key=key_nome)
            st.text_input("Tipo", key=key_tipo)
    
            st.selectbox(
                "Grau",
                [4, 3, 2, 1],
                key=key_grau
            )

            if st.session_state[key_grau] == 1:
                st.checkbox("Despertado", key=key_despertada)

            if st.session_state[key_despertada]:
                st.text_area(
                    "Habilidade Despertada",
                    key=key_hab_despertada,
                    height=100
                )
    
            st.checkbox("Amaldiçoado", key=key_amald)
    
            bonus, ma = calcular_arsenal(
                st.session_state[key_grau],
                st.session_state[key_amald]
            )
    
            st.markdown(f"**Bônus:** +{bonus} | **M.A.:** {ma}")
    
            st.text_area("Descrição", key=key_desc, height=120)
    
            col1, col2 = st.columns(2)
    
            with col1:
                if st.button("💾 Salvar", key=f"save_arsenal_{i}"):
                    st.session_state["arsenal"][i] = {
                        "nome": st.session_state[key_nome],
                        "tipo": st.session_state[key_tipo],
                        "grau": st.session_state[key_grau],
                        "bonus": bonus,
                        "ma_requerido": ma,
                        "amaldicoada": st.session_state[key_amald],
                        "despertada": st.session_state[key_despertada] if st.session_state[key_grau] == 1 else False,
                        "habilidade_despertada": st.session_state[key_hab_despertada] if st.session_state[key_despertada] else "",
                        "descricao": st.session_state[key_desc]
                    }
                    st.rerun()
    
            with col2:
                if st.button("🗑 Remover", key=f"del_arsenal_{i}"):
                    st.session_state["arsenal"].pop(i)
                    st.rerun()

# ===============================
# PROFICIÊNCIAS, ESTILO
# ===============================


st.header("Proficiências")
st.text_input(
    "Proficiências",
    key="proficiencias",
    placeholder="Ex: Atirador, Corpo-a-Corpo, Armas Brancas..."
)

st.header("Estilo de Luta")
st.text_area(
    "Estilo de Luta",
    key="estilo_luta",
    placeholder="Descreva o estilo de luta do personagem..."
)

# ===============================
# HISTÓRIA E APARÊNCIA
# ===============================

st.header("História e Aparência")

with st.container(border=True):
    st.text_area(
    "História",
    key="historia",
    height=220
)
    
    st.text_area(
    "Aparência",
    key="aparencia",
    height=150
)

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
    "nome": st.session_state["nome"],
    "titulo": st.session_state["titulo"],
    "afiliacao": st.session_state["afiliacao"],
    "origem": st.session_state["origem"],
    "imagem": None,
    
    "raca": st.session_state["raca"],
    "versao": st.session_state["versao"],
    
    "vida_maxima": st.session_state["vida_maxima"],
    "vida_atual": st.session_state["vida_atual"],
    "subatributos": st.session_state["subatributos"],
    
    "haki_armamento": st.session_state["haki_armamento"],
    "haki_observacao": st.session_state["haki_observacao"],
    "haki_conquistador": st.session_state["haki_conquistador"],
    "anotacoes": st.session_state["anotacoes"],

    "proficiencias": st.session_state["proficiencias"],
    "estilo_luta": st.session_state["estilo_luta"],

    "historia": st.session_state["historia"],
    "aparencia": st.session_state["aparencia"],

    "passivas": st.session_state["passivas"],
    "habilidades": st.session_state["habilidades"],
    "ataques": st.session_state["ataques"],
    "modos": st.session_state["modos"],

    "arsenal": st.session_state["arsenal"]
}

if st.session_state.get("imagem_personagem"):
    ficha_data["imagem"] = st.session_state["imagem_personagem"].getvalue().decode("latin1")


st.markdown("---")
salvar_ficha(ficha_data)
st.caption("Versão 5.0 — Ficha Interativa de Personagem | OnePica RPG")
