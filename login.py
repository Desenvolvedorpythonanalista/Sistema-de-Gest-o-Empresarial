import streamlit as st
import json
import os

# Função para salvar os dados do usuário em um arquivo JSON
def save_user_data(user_data):
    """
    Salva ou atualiza os dados do usuário em um arquivo JSON.
    
    Parâmetros:
    - user_data (dict): Um dicionário contendo os dados do usuário (nome completo, e-mail, senha, etc.).
    
    Descrição:
    - Verifica se o arquivo 'users.json' existe. Se não existir, cria um novo arquivo com uma lista vazia.
    - Lê os dados existentes e adiciona ou atualiza os dados do usuário.
    - Salva a lista atualizada de usuários no arquivo JSON.
    """
    # Verifica se o arquivo 'users.json' não existe
    if not os.path.exists("users.json"):
        # Cria um novo arquivo 'users.json' com uma lista vazia
        with open("users.json", "w") as file:
            json.dump([], file)
    
    # Abre o arquivo 'users.json' em modo leitura e carrega os dados existentes
    with open("users.json", "r") as file:
        users = json.load(file)
    
    # Adiciona ou atualiza os dados do usuário
    users.append(user_data)
    
    # Salva a lista atualizada no arquivo JSON
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Função para autenticar um usuário com base em e-mail, senha e número de crachá (opcional)
def authenticate_user(email, password, badge_number=None):
    """
    Autentica um usuário com base no e-mail, senha e, opcionalmente, no número de crachá.
    
    Parâmetros:
    - email (str): O e-mail do usuário.
    - password (str): A senha do usuário.
    - badge_number (str, opcional): O número de crachá do usuário (se aplicável).
    
    Retorna:
    - dict: Dados do usuário se a autenticação for bem-sucedida, caso contrário, retorna None.
    
    Descrição:
    - Lê os dados dos usuários do arquivo 'users.json' e verifica se os detalhes fornecidos correspondem a um usuário registrado.
    - Se o número de crachá for fornecido, ele será verificado também.
    """
    # Abre o arquivo 'users.json' em modo leitura e carrega os dados dos usuários
    with open("users.json", "r") as file:
        users = json.load(file)
    
    # Verifica se o e-mail e a senha correspondem ao admin padrão
    if email == "admin" and password == "":
        return {"email": email, "badge_number": "admin", "full_name": "Administrador", "job_title": "Admin"}
    
    # Percorre a lista de usuários para encontrar um usuário que corresponda ao e-mail e senha fornecidos
    for user in users:
        if user["email"] == email and user["password"] == password:
            # Se o número de crachá for fornecido, verifica se ele corresponde ao número do usuário
            if badge_number and user.get("badge_number") != badge_number:
                return None
            return user
    return None

# Função para obter os títulos de cargos disponíveis que ainda não foram usados
def get_available_job_titles():
    """
    Obtém uma lista de títulos de cargos disponíveis que ainda não foram utilizados.
    
    Retorna:
    - list: Uma lista de títulos de cargos disponíveis.
    
    Descrição:
    - Lê os dados dos usuários do arquivo 'users.json' se ele existir.
    - Cria um conjunto de títulos de cargos já utilizados e calcula os disponíveis.
    """
    # Verifica se o arquivo 'users.json' existe e carrega os dados se existir
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
            # Cria um conjunto de títulos de cargos usados pelos usuários
            used_job_titles = set(user["job_title"] for user in users)
    else:
        used_job_titles = set()
    
    # Define todos os títulos de cargos possíveis
    all_job_titles = {"Dono", "SEO (Diretor Executivo)", "Gerente de Marketing", "Outro"}
    # Calcula os títulos de cargos disponíveis subtraindo os usados dos possíveis
    available_job_titles = list(all_job_titles - used_job_titles)
    return available_job_titles

# Função principal que controla a interface do usuário e navegação
def main():
    """
    Controla a navegação e exibição da interface do usuário com base no estado atual da sessão.
    
    Descrição:
    - Gerencia o fluxo de login, registro e interfaces específicas de cargo.
    - Redireciona o usuário para a interface apropriada com base no estado da sessão.
    """
    # Verifica se a chave 'registration_step' não está no estado da sessão e define seu valor inicial como "login"
    if "registration_step" not in st.session_state:
        st.session_state.registration_step = "login"

    # Etapa de login
    if st.session_state.registration_step == "login":
        st.title("Login")

        # Cria um formulário para o login do usuário
        with st.form(key="login_form"):
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            badge_number = st.text_input("Número de Crachá de Funcionário")
            login_button = st.form_submit_button("Fazer Login")

        # Botões de navegação para alternar entre login e cadastro
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cadastrar"):
                st.session_state.registration_step = "register"
                st.experimental_rerun()

        with col2:
            if st.button("Já tenho uma conta. Faça Login"):
                st.session_state.registration_step = "login"
                st.experimental_rerun()

        # Se o botão de login for pressionado, tenta autenticar o usuário
        if login_button:
            user = authenticate_user(email, password, badge_number)
            if user:
                # Define informações do usuário no estado da sessão
                st.session_state.logged_in = True
                st.session_state.username = email
                st.session_state.badge_number = user.get("badge_number", "")
                st.session_state.full_name = user.get("full_name", "")
                st.session_state.job_title = user.get("job_title", "")
                
                # Redireciona o usuário para a interface apropriada com base no cargo ou crachá
                if st.session_state.job_title == "SEO (Diretor Executivo)":
                    st.session_state.registration_step = "checklist_SEO"
                elif st.session_state.job_title == "Dono":
                    st.session_state.registration_step = "checklist_Dono"
                elif st.session_state.job_title == "Gerente de Marketing":
                    st.session_state.registration_step = "checklist_MKT"
                elif st.session_state.job_title == "Outro":
                    st.session_state.registration_step = "checklist_outro"
                elif st.session_state.badge_number == "admin":
                    st.session_state.registration_step = "admin_interface"
                else:
                    st.session_state.registration_step = "default_interface"
                st.experimental_rerun()
            else:
                st.error("E-mail, senha ou número de crachá incorretos.")

    # Etapa de cadastro de novo usuário
    elif st.session_state.registration_step == "register":
        st.title("Cadastro e Autenticação")
        st.subheader("Cadastro de Novo Usuário")

        # Cria um formulário para o cadastro de um novo usuário
        with st.form(key="registration_form"):
            full_name = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            phone_number = st.text_input("Número de Telefone")
            job_title = st.selectbox("Cargo", get_available_job_titles())
            badge_number = st.text_input("Número de Crachá de Funcionário")
            password = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button("Enviar Cadastro")

        # Botões de navegação para alternar entre login e cadastro
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Já tenho uma conta. Faça Login"):
                st.session_state.registration_step = "login"
                st.experimental_rerun()

        with col2:
            if st.button("Cadastrar"):
                st.session_state.registration_step = "register"
                st.experimental_rerun()

        # Se o botão de envio do formulário for pressionado, valida e salva os dados do usuário
        if submit_button:
            # Verifica se todos os campos obrigatórios foram preenchidos
            if not full_name or not email or not password:
                st.error("Nome completo, e-mail e senha são obrigatórios.")
            else:
                # Armazena as informações do usuário no estado da sessão
                st.session_state.user_info = {
                    "full_name": full_name,
                    "email": email,
                    "phone_number": phone_number,
                    "job_title": job_title,
                    "badge_number": badge_number,
                    "password": password
                }
                
                # Salva os dados do usuário no arquivo JSON
                save_user_data(st.session_state.user_info)

                # Redireciona para a página de login e exibe uma mensagem de sucesso
                st.session_state.registration_step = "login"
                st.success("Cadastro concluído com sucesso! Você pode agora fazer login.")
                st.experimental_rerun()

    # Interface para o checklist SEO
    elif st.session_state.registration_step == "checklist_SEO":
        import checklist_SEO  # Importa o módulo do checklist SEO
        checklist_SEO.main()  # Chama a função principal do checklist SEO

    # Interface para o checklist Dono
    elif st.session_state.registration_step == "checklist_Dono":
        import checklist_Dono  # Importa o módulo do checklist Dono
        checklist_Dono.main()  # Chama a função principal do checklist Dono

    # Interface para o checklist Gerente de Marketing
    elif st.session_state.registration_step == "checklist_MKT":
        import checklist_MKT  # Importa o módulo do checklist Gerente de Marketing
        checklist_MKT.main()  # Chama a função principal do checklist Gerente de Marketing

    # Interface para outros cargos
    elif st.session_state.registration_step == "checklist_outro":
        st.write("Interface para outro cargo")

    # Interface padrão para usuários que não se encaixam em outras categorias
    elif st.session_state.registration_step == "default_interface":
        st.empty() 
        
        # Exibe uma mensagem de boas-vindas com estilo personalizado
        st.markdown(f"""
            <style>
                .centered-container {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    text-align: center;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: transparent;
                    border: 2px solid black;
                    color: black;
                    text-decoration: none;
                }}
                .button:hover {{
                    background-color: black;
                    color: white;
                }}
            </style>
            <div class="centered-container">
                <h1>Bem-vindo, {st.session_state.full_name}!</h1>
                <p>Estamos felizes em ter você na equipe.</p>
                <a class="button" href="#">Prosseguir</a>
            </div>
        """, unsafe_allow_html=True)

    # Interface para o admin
    elif st.session_state.registration_step == "admin_interface":
        st.title("Interface Admin")
        st.write("Bem-vindo à interface admin!")

# Verifica se o script está sendo executado diretamente e chama a função principal
if __name__ == "__main__":
    main()
