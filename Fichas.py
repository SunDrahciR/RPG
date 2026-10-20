import streamlit as st
import json
import hashlib
from io import StringIO
from io import BytesIO

# ===============================
# DEFINIÇÕES DAS VIRTUDES
# ===============================

TEXTOS_VIRTUDES = {
    "Ardiloso": {
        "descricao": "Um caminho de golpes sujos, batalhas travadas na mente.",
        "efeito": (
            "Dano e Resistência reduzidos pela metade. Possui +50% de Acerto. "
            "Críticos são reduzidos em 1 (Crítico só arranca membro caso seja 20 Natural)."
        ),
    },
    "Protetor": {
        "descricao": (
            "A proteção de quem você se importa sempre vem a ser sua prioridade, "
            "sempre querendo os acompanhar em situações de risco e tomando a frente do perigo."
        ),
        "efeito": (
            "35% de sua Defesa entra como Vida Temporária. Ela não se recupera por curas "
            "normais; ao fim da batalha, recupera-se ao máximo. Tem 25% de Velocidade a menos "
            "e 20% de Defesa a mais."
        ),
    },
    "Brutalidade": {
        "descricao": (
            "Você não se importa com mais nada durante a batalha, pois seu único objetivo "
            "é matar e destruir seus inimigos. Não para de bater até seus inimigos morrerem "
            "e, se tentarem fugir, fará de tudo para ir atrás."
        ),
        "efeito": "+25% de Dano e +10% de Acerto. Não possui ação de bloqueio.",
    },
    "Sagacidade": {
        "descricao": (
            "Aquele que pensa antes de agir, tomando decisões rápidas e certeiras, com alta "
            "desconfiança de todos, e incapaz de tomar atitudes que coloquem sua vida em risco rapidamente."
        ),
        "efeito": "+25% de Velocidade. 30% da Velocidade vai para Acerto. -20% de Dano.",
    },
    "Honra": {
        "descricao": (
            "Você não é capaz de quebrar seus ideais do que é o certo. Não pode atacar alguém "
            "que esteja com enfermidade causada por outra pessoa."
        ),
        "efeito": (
            "25% de sua Vontade atual vai para Dano e Acerto. Em testes de Vontade para fazer "
            "algo contra sua honra, o teste se torna 30% maior."
        ),
    },
    "Duelista": {
        "descricao": (
            "Você se enxerga como o único capaz de carregar o peso da batalha, evitando que "
            "seus aliados entrem em combate o máximo possível."
        ),
        "efeito": (
            "Ao escolher um alvo, ambos entram em um estado de Duelo Justo, recebendo +15% "
            "em Acerto e Dano um contra o outro. Se um dos duelistas atacar ou for atacado "
            "por um terceiro, ambos sofrem -25% em Acerto e Dano."
        ),
    },
    "Determinação": {
        "descricao": (
            "Uma mentalidade baseada em persistência, resistência e força. Quanto mais difícil "
            "fica a batalha, mais o personagem se recusa a desistir."
        ),
        "efeito": (
            "Ganha +10% de Defesa e Dano a cada 20% de Vida perdida. Ao escolher um inimigo "
            "como alvo, deve continuar tentando enfrentá-lo enquanto ele estiver consciente "
            "e em combate. Caso abandone voluntariamente esse confronto para atacar outro alvo, "
            "sofre -25% em todas as rolagens por 2 turnos."
        ),
    },
    "Ego": {
        "descricao": (
            "Você se enxerga como poderoso em batalha, não obedecendo ou dando importância para quem é mais fraco."
        ),
        "efeito": (
            "Na primeira metade da Vida, tem -25% de Dano. Na segunda metade, ganha +30% de Dano. "
            "Quando tem mais atributo que o oponente, ganha um D4 a mais no resultado do dado, "
            "em rolagens desse atributo."
        ),
    },
    "Pacifismo": {
        "descricao": (
            "Não é capaz de matar e tenta impedir que assim o façam, pois toda a vida é sagrada."
        ),
        "efeito": (
            "Só consegue contra-atacar. Contra-ataques são uma ação garantida com +50% no Dano. "
            "O oponente fica com, no mínimo, 1 ponto de Vida, e não são arrancados membros."
        ),
    },
    "Coletivista": {
        "descricao": (
            "Lutar é um fardo grande demais para se fazer sozinho. Sempre tenta apoiar seus aliados "
            "em qualquer decisão."
        ),
        "efeito": (
            "Quando está com outras pessoas, você e seus aliados recebem +10% de Vontade e +20% "
            "de Acerto, e não há penalidade ao fazer Ação em Conjunto com você. Caso esteja sozinho, "
            "recebe -10% de Vontade e -20% de Acerto."
        ),
    },
    "Impulsividade": {
        "descricao": "Sempre age antes de pensar, pois pensar muito é pra nerds.",
        "efeito": "25% da Velocidade vai para Dano. Sofre -20% em Acerto em todos os ataques.",
    },
}


def criar_virtudes_padrao():
    return {
        nome: {
            "descricao": dados["descricao"],
            "efeito": dados["efeito"],
            "habilidades": [],
        }
        for nome, dados in TEXTOS_VIRTUDES.items()
    }



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
    
    #Hibrido
    st.session_state["hibrido_raca_primaria"] = data.get(
    "hibrido_raca_primaria",
    ""
)

    st.session_state["hibrido_versao_primaria"] = data.get(
    "hibrido_versao_primaria",
    "V1"
)

    st.session_state["hibrido_raca_secundaria"] = data.get(
    "hibrido_raca_secundaria",
    ""
)

    st.session_state["hibrido_versao_secundaria"] = data.get(
    "hibrido_versao_secundaria",
    "V1"
)

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
    
    # Virtudes: mantém compatibilidade com fichas antigas
    virtudes_carregadas = data.get("virtudes", {})
    virtudes_padrao = criar_virtudes_padrao()
    virtudes_final = {}

    for nome, padrao in virtudes_padrao.items():
        carregada = virtudes_carregadas.get(nome, {})
        virtudes_final[nome] = {
            "descricao": carregada.get("descricao", padrao["descricao"]),
            "efeito": carregada.get("efeito", padrao["efeito"]),
            "habilidades": carregada.get("habilidades", []).copy(),
        }

    # Preserva também eventuais virtudes extras presentes no JSON
    for nome, dados_virtude in virtudes_carregadas.items():
        if nome not in virtudes_final:
            virtudes_final[nome] = {
                "descricao": dados_virtude.get("descricao", ""),
                "efeito": dados_virtude.get("efeito", ""),
                "habilidades": dados_virtude.get("habilidades", []).copy(),
            }

    st.session_state["virtudes"] = virtudes_final
    virtude_salva = data.get("virtude_selecionada", "Ardiloso")
    st.session_state["virtude_selecionada"] = (
        virtude_salva if virtude_salva in virtudes_final else "Ardiloso"
    )

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

if "virtudes" not in st.session_state:
    st.session_state["virtudes"] = criar_virtudes_padrao()

if "virtude_selecionada" not in st.session_state:
    st.session_state["virtude_selecionada"] = "Ardiloso"

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
    # O Streamlit reexecuta o script a cada interação. Este hash impede
    # que a mesma ficha seja recarregada e sobrescreva as edições a cada rerun.
    hash_upload = hashlib.sha256(upload.getvalue()).hexdigest()

    if st.session_state.get("_ultima_ficha_carregada_hash") != hash_upload:
        try:
            carregar_ficha(upload)
            st.session_state["_ultima_ficha_carregada_hash"] = hash_upload
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
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Tribo (Braço/Perna Longos)": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Tontata": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Homem-Peixe": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Nativo do Céu": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Oni": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Sereiano": {
        "V1": "",
        "V2": "",
        "V3": "",
        "Fraqueza": ""
    },

    "Mink": {
        "V1": "",
        "V2": "",
        "V3": "+",
    },

    "Gigante": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Lunariano": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Bucaneiro": {
        "V1": "",
        "V2": "",
        "V3": "",
    },

    "Híbrido": {
        "V1": "",
        "V2": "",
        "V3": ""
    }
}

    
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
                index=racas_base.index(
                    st.session_state.get(
                        "hibrido_raca_primaria",
                        racas_base[0]
                    )
                ) if st.session_state.get(
                    "hibrido_raca_primaria"
                ) in racas_base else 0,
                key="hibrido_raca_primaria"
            )
    
            versao1 = st.selectbox(
                "Versão da Raça Primária",
                ["V1", "V2"],
                index=["V1", "V2"].index(
                    st.session_state.get(
                        "hibrido_versao_primaria",
                        "V1"
                    )
                ),
                key="hibrido_versao_primaria"
            )
    
        with colH2:
            racas_secundarias = [
                r for r in racas_base if r != raca1
            ]
    
            raca2 = st.selectbox(
                "Raça Secundária",
                racas_secundarias,
                index=racas_secundarias.index(
                    st.session_state.get(
                        "hibrido_raca_secundaria",
                        racas_secundarias[0]
                    )
                ) if st.session_state.get(
                    "hibrido_raca_secundaria"
                ) in racas_secundarias else 0,
                key="hibrido_raca_secundaria"
            )
    
            versao2 = st.selectbox(
                "Versão da Raça Secundária",
                ["V1", "V2"],
                index=["V1", "V2"].index(
                    st.session_state.get(
                        "hibrido_versao_secundaria",
                        "V1"
                    )
                ),
                key="hibrido_versao_secundaria"
            )
    
        st.info(
            f"**Primária:** {raca1} ({versao1})\n\n"
            f"**Secundária:** {raca2} ({versao2})"
        )

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

tab_passivas, tab_habilidades, tab_ataques, tab_modos, tab_virtude = st.tabs(
    ["Passivas", "Habilidades", "Ataques", "Modos", "Virtude"]
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

# ===============================
# VIRTUDE
# ===============================

def adicionar_habilidade_virtude():
    nome_virtude = st.session_state["virtude_selecionada"]
    nome = st.session_state["nova_virtude_hab_nome"]
    descricao = st.session_state["nova_virtude_hab_desc"]

    if nome.strip():
        st.session_state["virtudes"][nome_virtude]["habilidades"].append({
            "nome": nome.strip(),
            "descricao": descricao,
        })
        st.session_state["nova_virtude_hab_nome"] = ""
        st.session_state["nova_virtude_hab_desc"] = ""


with tab_virtude:
    st.subheader("Virtude")

    nomes_virtudes = list(TEXTOS_VIRTUDES.keys())

    # Se a ficha carregada tiver uma virtude selecionada válida, preserva-a.
    if st.session_state.get("virtude_selecionada") not in nomes_virtudes:
        st.session_state["virtude_selecionada"] = nomes_virtudes[0]

    st.selectbox(
        "Escolher Virtude",
        options=nomes_virtudes,
        key="virtude_selecionada",
    )

    virtude_atual = st.session_state["virtude_selecionada"]
    dados_virtude = st.session_state["virtudes"].setdefault(
        virtude_atual,
        {
            "descricao": TEXTOS_VIRTUDES[virtude_atual]["descricao"],
            "efeito": TEXTOS_VIRTUDES[virtude_atual]["efeito"],
            "habilidades": [],
        },
    )

    st.markdown(f"### {virtude_atual}")
    st.write(dados_virtude.get("descricao", ""))
    st.markdown("**Efeito da Virtude**")
    st.info(dados_virtude.get("efeito", ""))

    st.divider()

    with st.expander("➕ Adicionar Habilidade de Virtude"):
        st.text_input(
            "Nome da Habilidade",
            key="nova_virtude_hab_nome",
        )
        st.text_area(
            "Descrição",
            key="nova_virtude_hab_desc",
            height=120,
        )
        st.button(
            "Adicionar Habilidade",
            key="btn_add_virtude_hab",
            on_click=adicionar_habilidade_virtude,
        )

    habilidades_virtude = dados_virtude.setdefault("habilidades", [])

    if not habilidades_virtude:
        st.caption("Nenhuma habilidade adicionada a esta Virtude ainda.")

    for i, habilidade in enumerate(habilidades_virtude):
        key_nome = f"edit_virtude_{virtude_atual}_{i}_nome"
        key_desc = f"edit_virtude_{virtude_atual}_{i}_desc"

        if key_nome not in st.session_state:
            st.session_state[key_nome] = habilidade.get("nome", "")

        if key_desc not in st.session_state:
            st.session_state[key_desc] = habilidade.get("descricao", "")

        with st.expander(habilidade.get("nome", "Habilidade sem nome")):
            st.text_input("Nome", key=key_nome)
            st.text_area("Descrição", key=key_desc, height=120)

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "💾 Salvar",
                    key=f"save_virtude_{virtude_atual}_{i}",
                ):
                    habilidades_virtude[i] = {
                        "nome": st.session_state[key_nome],
                        "descricao": st.session_state[key_desc],
                    }
                    st.rerun()

            with col2:
                if st.button(
                    "🗑 Remover",
                    key=f"del_virtude_{virtude_atual}_{i}",
                ):
                    habilidades_virtude.pop(i)
                    # Limpa os campos de edição dessa virtude para evitar
                    # que valores antigos sejam associados a outra habilidade.
                    for j in range(len(habilidades_virtude) + 1):
                        st.session_state.pop(
                            f"edit_virtude_{virtude_atual}_{j}_nome", None
                        )
                        st.session_state.pop(
                            f"edit_virtude_{virtude_atual}_{j}_desc", None
                        )
                    st.rerun()


GRAUS_ARSENAL = {
    4: {"bonus": 12, "ma": 10},
    3: {"bonus": 25, "ma": 30},
    2: {"bonus": 50, "ma": 50},
    1: {"bonus": 75, "ma": 100},
    "Especial": {"bonus": 100, "ma": 150},
}

BONUS_AMALDICOADA = 1.5

def calcular_arsenal(grau, amaldicoada):
    bonus = GRAUS_ARSENAL[grau]["bonus"]
    ma = GRAUS_ARSENAL[grau]["ma"]

    if amaldicoada:
        bonus = int(bonus * BONUS_AMALDICOADA)
        ma = int(ma * BONUS_AMALDICOADA)

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
            [4, 3, 2, 1, "Especial"],
            format_func=lambda g: f"Grau {g}",
            key="novo_arsenal_grau"
        )

        st.checkbox(
            "Arsenal Amaldiçoado (+50% bônus, +50% M.A.)",
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
                [4, 3, 2, 1, "Especial"],
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
    
    "hibrido_raca_primaria": st.session_state.get(
        "hibrido_raca_primaria",
        ""
    ),

    "hibrido_versao_primaria": st.session_state.get(
        "hibrido_versao_primaria",
        "V1"
    ),

"hibrido_raca_secundaria": st.session_state.get(
    "hibrido_raca_secundaria",
    ""
),

"hibrido_versao_secundaria": st.session_state.get(
    "hibrido_versao_secundaria",
    "V1"
),
    
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
    "virtude_selecionada": st.session_state["virtude_selecionada"],
    "virtudes": st.session_state["virtudes"],

    "arsenal": st.session_state["arsenal"]
}

if st.session_state.get("imagem_personagem"):
    ficha_data["imagem"] = st.session_state["imagem_personagem"].getvalue().decode("latin1")


st.markdown("---")
salvar_ficha(ficha_data)
st.caption("Versão 5.0 — Ficha Interativa de Personagem | OnePica RPG")
