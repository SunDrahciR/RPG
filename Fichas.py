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
