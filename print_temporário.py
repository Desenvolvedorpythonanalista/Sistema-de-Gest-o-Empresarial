import streamlit as st
from Auth import authenticate_user, get_available_job_titles, save_user_data, assign_badge_number, generate_badge_number

def get_first_name(full_name):
    return full_name.split()[0]

def initialize_session_state():
    if "registration_step" not in st.session_state:
        st.session_state.registration_step = "login"
    if "job_title" not in st.session_state:
        st.session_state.job_title = ""

def navigate_to_checklist():
    initialize_session_state()
    # Mapeamento dos cargos para os módulos de checklist
    checklists = {
        "SEO (Diretor Executivo)": "checklist_SEO",
        "Dono": "checklist_Dono",
        "Gerente de Marketing": "checklist_MKT",
        "Outro": "checklist_Outro"  # Corrigido para "checklist_Outro"
    }

    # Verificar o valor do cargo
    st.write(f"Valor do cargo no session_state: {st.session_state.job_title}")

    # Nome do módulo a ser importado com base no cargo do usuário
    checklist_module = checklists.get(st.session_state.job_title, None)

    if checklist_module:
        try:
            # Importar o módulo dinamicamente
            checklist = __import__(checklist_module)
            checklist.main()  # Chamar a função principal do módulo
        except ImportError:
            st.error(f"Não foi possível importar o módulo {checklist_module}.")
    else:
        st.error(f"Cargo não reconhecido: {st.session_state.job_title}. Verifique o mapeamento dos cargos.")

# Cadastro de Novo Usuário
if st.session_state.registration_step == "register":
    st.title("Cadastro e Autenticação")
    st.subheader("Cadastro de Novo Usuário")

    with st.form(key="registration_form"):
        full_name = st.text_input("Nome Completo")
        email = st.text_input("E-mail")
        phone_number = st.text_input("Número de Telefone")
        job_title = st.selectbox("Cargo", get_available_job_titles())  # Verifique se o título está correto
        password = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Enviar Cadastro")
        login_button = st.form_submit_button("Já tenho uma conta. Faça Login")

        if submit_button:
            if not full_name or not email or not password:
                st.error("Nome completo, e-mail e senha são obrigatórios.")
            else:
                badge_number = generate_badge_number()  # Gerar automaticamente o número de crachá

                st.session_state.user_info = {
                    "full_name": full_name,
                    "email": email,
                    "phone_number": phone_number,
                    "job_title": job_title,  # Verifique se está sendo salvo corretamente
                    "badge_number": badge_number,
                    "password": password
                }
                
                save_user_data(st.session_state.user_info)
                assign_badge_number(email, badge_number)

                st.session_state.registration_step = "welcome"
                st.success("Cadastro concluído com sucesso!")
                st.experimental_rerun()

        if login_button:
            st.session_state.registration_step = "login"
            st.experimental_rerun()

# Login do Usuário
elif st.session_state.registration_step == "login":
    st.title("Login")

    with st.form(key="login_form"):
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")
        register_button = st.form_submit_button("Cadastrar")

        if login_button:
            if not email or not password:
                st.error("E-mail e senha são obrigatórios.")
            else:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = email
                    st.session_state.badge_number = user.get("badge_number", "")
                    st.session_state.full_name = user.get("full_name", "")
                    st.session_state.job_title = user.get("job_title", "")  # Verifique se o cargo está sendo recuperado corretamente
                    st.success("Login bem-sucedido.")
                    
                    # Redireciona com base no cargo do usuário
                    if st.session_state.job_title == "SEO (Diretor Executivo)":
                        st.session_state.registration_step = "checklist_seo"
                    elif st.session_state.job_title == "Dono":
                        st.session_state.registration_step = "checklist_dono"
                    elif st.session_state.job_title == "Gerente de Marketing":
                        st.session_state.registration_step = "checklist_mkt"
                    elif st.session_state.job_title == "Outro":
                        st.session_state.registration_step = "checklist_outro"
                    elif st.session_state.badge_number == "admin":
                        st.session_state.registration_step = "admin_interface"
                    else:
                        st.session_state.registration_step = "default_interface"
                    st.experimental_rerun()
                else:
                    st.error("E-mail ou senha incorretos.")

        if register_button:
            st.session_state.registration_step = "register"
            st.experimental_rerun()
