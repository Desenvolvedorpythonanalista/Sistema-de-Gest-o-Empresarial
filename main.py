import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import json
import string
import random

# Cria o diretório 'arquivos_recebidos' se não existir
os.makedirs("arquivos_recebidos", exist_ok=True)

# Cria o diretório 'arquivos_recebidos_1' se não existir
os.makedirs("arquivos_recebidos_1", exist_ok=True)

# Cria o diretório 'arquivos_recebidos_2' se não existir
os.makedirs("arquivos_recebidos_2", exist_ok=True)

# Cria o diretório 'arquivos_recebidos_3' se não existir
os.makedirs("arquivos_recebidos_3", exist_ok=True)

# Função para garantir que o diretório especificado exista
def ensure_directory_exists(directory):
    """
    Garante que o diretório especificado exista. Se não existir, cria-o.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

# Função para salvar os resultados em um arquivo CSV
def save_to_csv(data, filename):
    """
    Salva os dados fornecidos em um arquivo CSV com o nome especificado.
    
    Parameters:
    data (dict): Dados a serem salvos no CSV.
    filename (str): Nome do arquivo CSV.
    """
    # Função para salvar os resultados em um arquivo CSV na pasta que será compartilhada com o Dono da Tecnology Acacemy
    filepath = os.path.join("arquivos_recebidos", filename)
    df = pd.DataFrame([data])  # Converte os dados em um DataFrame
    df.to_csv(filepath, index=False)  # Salva o DataFrame como CSV
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos'")

    # Função para salvar os resultados em um arquivo CSV na pasta que será compartilhada com o Dono da Tecnology Acacemy
    filepath = os.path.join("arquivos_recebidos_1", filename)
    df = pd.DataFrame([data])  # Converte os dados em um DataFrame
    df.to_csv(filepath, index=False)  # Salva o DataFrame como CSV
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos_1'")
    
    # Função para salvar os resultados em um arquivo CSV na pasta que será compartilhada com o SEO da Tecnology Academy
    filepath = os.path.join("arquivos_recebidos_2", filename)
    df = pd.DataFrame([data])  # Converte os dados em um DataFrame
    df.to_csv(filepath, index=False)  # Salva o DataFrame como CSV
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos_2'")

    # Função para salvar os resultados em um arquivo CSV na pasta que será compartilhada com o Marketer da Tenology Academy
    filepath = os.path.join("arquivos_recebidos_3", filename)
    df = pd.DataFrame([data])  # Converte os dados em um DataFrame
    df.to_csv(filepath, index=False)  # Salva o DataFrame como CSV
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos_3'")

# Função para salvar e enviar a checklist do MKT para o SEO
def save_and_send_checklist_mkt(results, signature, score):
    """
    Salva os resultados da checklist em um arquivo CSV no diretório 'arquivos_recebidos_1' para MKT.
    
    Parameters:
    results (dict): Resultados da checklist.
    signature (str): Assinatura do revisor.
    score (float): Nota geral calculada.
    """
    unique_id = uuid.uuid4().hex  # Gera um identificador único
    filename = f"checklist_mkt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}.csv"  # Define o nome do arquivo
    data = {**results, "Assinatura do Revisor": signature, "Nota Geral": score}  # Inclui a assinatura e nota geral nos dados
    
    ensure_directory_exists("arquivos_recebidos_1")  # Verifica e cria a pasta se não existir
    filepath = os.path.join("arquivos_recebidos_1", filename)
    df = pd.DataFrame([data])  # Converte os dados em um DataFrame
    df.to_csv(filepath, index=False)  # Salva o DataFrame como CSV
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos_1'")
    st.session_state.filepath = filepath

# Função para salvar e enviar a checklist do SEO para o Dono
def save_and_send_checklist_seo(results, signature, score):
    """
    Salva os resultados da checklist em um arquivo CSV no diretório 'arquivos_recebidos_1' para SEO.
    
    Parameters:
    results (dict): Resultados da checklist.
    signature (str): Assinatura do revisor.
    score (float): Nota geral calculada.
    """
    unique_id = uuid.uuid4().hex  # Gera um identificador único
    filename = f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}.csv"  # Define o nome do arquivo
    data = {**results, "Assinatura do Revisor": signature, "Nota Geral": score}  # Inclui a assinatura e nota geral nos dados
    
    ensure_directory_exists("arquivos_recebidos_1")  # Verifica e cria a pasta se não existir
    filepath = os.path.join("arquivos_recebidos_1", filename)
    df = pd.DataFrame([data])  # Converte os dados em um DataFrame
    df.to_csv(filepath, index=False)  # Salva o DataFrame como CSV
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos_1'")
    st.session_state.filepath = filepath
  
def save_and_send_checklist_dono(results, signature, score):
    """
    Salva os resultados da checklist em um arquivo CSV no diretório 'arquivos_recebidos' para o Dono.
    
    Parameters:
    results (dict): Resultados da checklist.
    signature (str): Assinatura do revisor.
    score (float): Nota geral calculada.
    """
    # Gera um identificador único para o arquivo
    unique_id = uuid.uuid4().hex
    # Define o nome do arquivo com data e hora atual
    filename = f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}.csv"
    # Inclui a assinatura e a nota geral nos dados
    data = {**results, "Assinatura do Revisor": signature, "Nota Geral": score}

    # Verifica se o diretório existe e cria se necessário
    ensure_directory_exists("arquivos_recebidos")
    filepath = os.path.join("arquivos_recebidos", filename)

    # Converte os dados em um DataFrame e salva como CSV
    df = pd.DataFrame([data])
    df.to_csv(filepath, index=False)

    # Informa ao usuário e salva o caminho do arquivo na sessão
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos'")
    st.session_state.filepath = filepath

# Função para calcular a nota geral da checklist
def calculate_score_simple(checklist_items, results):
    """
    Calcula a nota geral com base na quantidade de itens marcados como concluídos.
    
    Parameters:
    checklist_items (list): Lista de itens da checklist.
    results (dict): Resultados da checklist.
    
    Returns:
    float: Nota geral calculada.
    """
    total_items = len(checklist_items)  # Total de itens na checklist
    checked_items = sum(results.get(item, False) for item in checklist_items)  # Contagem de itens marcados como concluídos
    score = (checked_items / total_items) * 10  # Calcula a nota geral
    return round(score, 1)  # Retorna a nota arredondada

# Função para calcular o progresso em percentual
def calculate_progress(checklist_items, results):
    """
    Calcula o progresso da checklist em percentual.
    
    Parameters:
    checklist_items (list): Lista de itens da checklist.
    results (dict): Resultados da checklist.
    
    Returns:
    float: Progresso da checklist em percentual.
    """
    total_items = len(checklist_items)  # Total de itens na checklist
    checked_items = sum(results.get(item, False) for item in checklist_items)  # Contagem de itens marcados como concluídos
    return round((checked_items / total_items) * 100, 1)  # Retorna o progresso em percentual

# Função para listar arquivos CSV recebidos para o Dono
def list_received_files():
    """
    Lista todos os arquivos CSV no diretório 'arquivos_recebidos'.
    
    Returns:
    list: Lista de nomes de arquivos CSV.
    """
    files = [f for f in os.listdir("arquivos_recebidos") if f.endswith(".csv")]
    return files

# Função para listar arquivos CSV recebidos para o Marketer
def list_received_files():
    """
    Lista todos os arquivos CSV no diretório 'arquivos_recebidos_2'.
    
    Returns:
    list: Lista de nomes de arquivos CSV.
    """
    files = [f for f in os.listdir("arquivos_recebidos_2") if f.endswith(".csv")]
    return files

# Função para listar arquivos CSV recebidos para o Marketer
def list_received_files():
    """
    Lista todos os arquivos CSV no diretório 'arquivos_recebidos_3'.
    
    Returns:
    list: Lista de nomes de arquivos CSV.
    """
    files = [f for f in os.listdir("arquivos_recebidos_3") if f.endswith(".csv")]
    return files

# Função para extrair a data do nome do arquivo
def extract_date_from_filename(filename):
    """
    Extrai a data do nome do arquivo, assumindo um formato específico.
    
    Parameters:
    filename (str): Nome do arquivo.
    
    Returns:
    date: Data extraída do nome do arquivo ou "Data inválida" se não puder ser extraída.
    """
    try:
        date_str = filename.split('_')[2]  # Assume que a data está na terceira posição do nome do arquivo
        date_obj = datetime.strptime(date_str, '%Y%m%d')  # Converte a string da data para um objeto datetime
        return date_obj.date()  # Retorna a data
    except (IndexError, ValueError) as e:
        st.error(f"Erro ao extrair a data do arquivo '{filename}': {e}")
        return "Data inválida"

# Função para exibir o conteúdo de um arquivo CSV (filtrando apenas as colunas desejadas)
def display_file_content(filepath):
    """
    Exibe o conteúdo de um arquivo CSV, filtrando apenas as colunas "Assinatura do Revisor" e "Nota Geral".
    
    Parameters:
    filepath (str): Caminho do arquivo CSV.
    """
    df = pd.read_csv(filepath)  # Lê o arquivo CSV em um DataFrame
    
    if "Assinatura do Revisor" in df.columns and "Nota Geral" in df.columns:
        df_filtered = df[["Assinatura do Revisor", "Nota Geral"]]  # Filtra apenas as colunas desejadas
        file_name = os.path.basename(filepath)
        date_of_file = extract_date_from_filename(file_name)  # Extrai a data do nome do arquivo
        df_filtered["Data"] = date_of_file  # Adiciona a data como uma nova coluna
        st.write(df_filtered)  # Exibe o DataFrame filtrado
    else:
        st.warning("O arquivo selecionado não contém as colunas esperadas.")

# Função para ordenar arquivos por nome ou por data
def sort_files(files, sort_by='name'):
    """
    Ordena os arquivos de acordo com o critério especificado (nome ou data).
    
    Parameters:
    files (list): Lista de nomes de arquivos.
    sort_by (str): Critério de ordenação ('name' para nome, 'month' para data).
    
    Returns:
    list: Lista de nomes de arquivos ordenados.
    """
    if sort_by == 'name':
        files.sort()  # Ordena os arquivos por nome
    elif sort_by == 'month':
        files.sort(key=lambda x: extract_date_from_filename(x) if extract_date_from_filename(x) != "Data inválida" else datetime(1900, 1, 1))
    return files

# Função para carregar os dados dos usuários
def load_user_data():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as file:
            json.dump([], file)
    with open("users.json", "r") as file:
        return json.load(file)

# Função para gerar um número de crachá único
def generate_badge_number(length=6):
    characters = string.ascii_uppercase + string.digits
    badge_number = ''.join(random.choice(characters) for _ in range(length))
    return badge_number     

# Função para salvar os dados dos usuários
def save_user_data(user_data):
    users = load_user_data()
    existing_user = next((user for user in users if user["email"] == user_data["email"]), None)
    if existing_user:
        users = [user if user["email"] != user_data["email"] else user_data for user in users]
    else:
        user_data["confirmation_code"] = generate_badge_number(length=5)  # Gerar um código de 5 dígitos
        users.append(user_data)
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Função para autenticar o usuário
def authenticate_user(email, password):
    users = load_user_data()
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user
    return None

# Função para verificar o código de confirmação
def verify_confirmation_code(email, code):
    users = load_user_data()
    for user in users:
        if user["email"] == email and user.get("confirmation_code") == code:
            return True
    return False

# Função de login e cadastro
def login():
    st.sidebar.title("Login")
    email = st.sidebar.text_input("E-mail")
    password = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Entrar"):
        user = authenticate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_data = user
            st.session_state.badge_number = generate_badge_number()
            if not user.get("confirmation_code"):
                st.session_state.confirmed = True
            else:
                st.session_state.confirmed = False
                confirm_access()
        else:
            st.error("E-mail ou senha inválidos")

    if st.sidebar.button("Cadastrar"):
        if email and password:
            if authenticate_user(email, None):
                st.error("E-mail já cadastrado.")
            else:
                user_data = {"email": email, "password": password, "badge_number": generate_badge_number()}
                save_user_data(user_data)  # Corrigido aqui
                st.success("Cadastro realizado com sucesso! Faça login para continuar.")
                st.experimental_rerun()
        else:
            st.error("Por favor, insira e-mail e senha.")

# Função para permitir que o usuário insira o código após o login
def confirm_access():
    st.title("Confirmação de Código de Acesso")
    code = st.text_input("Insira o código de confirmação enviado por e-mail:", type="password")

    if st.button("Confirmar"):
        if verify_confirmation_code(st.session_state.user_data["email"], code):
            st.session_state.confirmed = True
            st.success("Código de confirmação correto. Acesso concedido!")
            st.experimental_rerun()  # Recarrega a página para mostrar a interface principal
        else:
            st.error("Código de confirmação incorreto. Tente novamente.")                          

# Interface do Streamlit para o Dono
def dono_interface():
    st.title("Checklist Mensal do Dono com o CEO Diretor Executivo da Empresa")

    ideal_score = 8.0
    score = 0.0  # Inicializa a variável score
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 40px;">
                <h1 style="font-size: 4em; color: #ff6347;">{ideal_score}</h1>
                <h3>Nota Ideal</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        checklist_items = [
            "Liderança e Gestão Operacional",
            "Implementação de Estratégias Corporativas",
            "Supervisão das Áreas Funcionais",
            "Representação da Empresa",
            "Tomada de Decisões Estratégicas",
            "Gestão de Relações com Investidores e Partes Interessadas",
            "Decisões para Expansão da Marca",
            "Promoção de Inovações",
            "Manutenção das Diretrizes Corporativas",
            "Direção dos Departamentos e Reuniões",
            "Estabelecimento e Monitoramento de KPIs",
            "Desenvolvimento do Plano Estratégico",
            "Gerenciamento do Orçamento Corporativo",
            "Fomento à Cultura e Valores Organizacionais"
        ]

        results = {}

        st.header("Marque os itens concluídos")

        for idx, item in enumerate(checklist_items):
            results[item] = st.checkbox(item, value=False, key=f"dono_{idx}")

        st.header("Observações e Comentários Adicionais")
        observations = st.text_area("Comentários gerais sobre o desempenho do CEO e áreas para melhorias", key="dono_observacoes")
        results["Observações e Comentários Adicionais"] = observations

        st.header("Assinatura do Revisor")
        reviewer_signature = st.text_input("Assinatura do Revisor", key="dono_assinatura_revisor")

        if st.button("Calcular Nota Geral", key="dono_calcular"):
            if not reviewer_signature:
                st.error("A assinatura do revisor é obrigatória para calcular a nota geral.")
            else:
                score = calculate_score_simple(checklist_items, results)
                checklist_completion = calculate_progress(checklist_items, results)
                st.write(f"Nota Geral: {score}/10")
                st.write(f"Nota Ideal: {ideal_score}/10")
                st.write(f"Checklists Concluídas: {checklist_completion}%")

        if st.button("Salvar e Enviar", key="dono_salvar_enviar"):
            if reviewer_signature:
                save_and_send_checklist_dono(results, reviewer_signature, score)
                st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o Dono.")
            else:
                st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

        if st.button("Enviar", key="dono_enviar"):
            if "filepath" in st.session_state:
                st.success(f"Checklist enviado para o Dono! Caminho do arquivo: {st.session_state.filepath}")
            else:
                st.error("Primeiro, salve a checklist antes de enviar.")

    st.title("Arquivos Recebidos")

sort_by = st.selectbox("Ordenar por", ["Nome do arquivo", "Ordem de Mês"], key="dono_sort_by")

# Listar os arquivos recebidos da pasta 'arquivos_recebidos_1' (onde o MKT salva os arquivos)
files = list_received_files(directory="arquivos_recebidos_1")  
files = sort_files(files, sort_by='name' if sort_by == 'Nome do arquivo' else 'month')

if files:
    selected_file = st.selectbox("Escolha um arquivo para visualizar", files, key="dono_selecionar_arquivo")
    if selected_file:
        filepath = os.path.join("arquivos_recebidos_1", selected_file)
        display_file_content(filepath)
else:
    st.info("Nenhum arquivo recebido ainda.")


# Interface do Streamlit para o MKT
def mkt_interface():
    st.title("Business Book do Gerente de SEO Marketing da Tecnology Academy")

    ideal_score = 8.0
    score = 0.0  # Inicializa a variável score
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 40px;">
                <h1 style="font-size: 4em; color: #ff6347;">{ideal_score}</h1>
                <h3>Nota Ideal</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        checklist_items = {
            "Checklist Semanal do Consultor/Assessor de Negócios": {
                "Análise de Propostas": [
                    "Revisar todas as propostas em aberto e sua evolução.",
                    "Garantir que todas as propostas estejam completas e atualizadas."
                ],
                "Reuniões com Clientes": [
                    "Realizar reuniões de acompanhamento com clientes para discutir o progresso.",
                    "Documentar todos os pontos discutidos e acordos feitos."
                ],
                "Avaliação de Resultados": [
                    "Revisar os resultados obtidos em comparação com os objetivos estabelecidos.",
                    "Identificar áreas para melhoria e ajuste de estratégias."
                ],
                "Planejamento Estratégico": [
                    "Participar do planejamento estratégico para alinhar as propostas com os objetivos da empresa.",
                    "Definir metas e estratégias para a prospecção de novos clientes e desenvolvimento de propostas."
                ],
                "Preparação para Reuniões": [
                    "Revisar e preparar todos os materiais necessários antes das reuniões com clientes.",
                    "Garantir que todas as informações e documentos estejam atualizados e prontos."
                ],
                "Gerenciamento de Tempo": [
                    "Gerenciar o tempo de forma eficiente para equilibrar tarefas e compromissos.",
                    "Priorizar atividades baseadas em importância e prazos."
                ],
                "Preparar Relatórios de Progresso": [
                    "Preparar e enviar relatórios de progresso para clientes e a equipe.",
                    "Garantir que todos os relatórios estejam completos e entregues pontualmente."
                ],
                "Atualização de Banco de Dados de Clientes": [
                    "Atualizar o banco de dados com informações recentes sobre clientes e interações.",
                    "Manter registros precisos e atualizados para futuras referências."
                ]
            },
            "Checklist Semanal do Editor de Vídeos": {
                "Revisar Filmagens": [
                    "Assistir a todo o material bruto para selecionar os melhores takes."
                ],
                "Edição Inicial": [
                    "Realizar a edição inicial para criar um primeiro rascunho do vídeo."
                ],
                "Adição de Efeitos Visuais": [
                    "Adicionar efeitos visuais necessários para melhorar a qualidade do vídeo."
                ],
                "Inclusão de Áudio": [
                    "Adicionar trilha sonora e efeitos sonoros ao vídeo."
                ],
                "Revisão de Áudio": [
                    "Garantir que o áudio esteja claro e bem balanceado."
                ],
                "Ajuste de Cor": [
                    "Ajustar as cores do vídeo para garantir consistência e qualidade."
                ],
                "Incluir Títulos e Legendas": [
                    "Adicionar títulos, legendas e outros elementos gráficos."
                ],
                "Exportação do Vídeo": [
                    "Exportar o vídeo no formato e qualidade requisitados."
                ],
                "Revisão Final": [
                    "Assistir ao vídeo finalizado para garantir que tudo esteja conforme o esperado."
                ],
                "Entrega do Vídeo": [
                    "Entregar o vídeo finalizado aos clientes ou para publicação."
                ],
                "Backup do Material": [
                    "Realizar backup de todo o material bruto e editado."
                ],
                "Documentação do Projeto": [
                    "Atualizar a documentação do projeto com detalhes da edição e observações."
                ]
            },
            "Checklist Semanal do Especialista em Produto": {
                "Avaliação de Produto": [
                    "Revisar o desempenho do produto no mercado.",
                    "Coletar feedback de clientes e stakeholders."
                ],
                "Análise de Concorrência": [
                    "Analisar as estratégias dos concorrentes e suas ofertas."
                ],
                "Planejamento de Novos Recursos": [
                    "Planejar novos recursos ou melhorias para o produto."
                ],
                "Atualização de Documentação": [
                    "Atualizar a documentação do produto conforme novas alterações."
                ],
                "Testes de Produto": [
                    "Conduzir testes de qualidade e usabilidade do produto."
                ],
                "Coordenação com Equipes": [
                    "Coordinar com equipes de desenvolvimento e marketing para alinhar estratégias."
                ],
                "Preparação de Relatórios": [
                    "Preparar relatórios sobre o progresso e desempenho do produto."
                ],
                "Reuniões de Feedback": [
                    "Realizar reuniões de feedback com clientes e equipes."
                ],
                "Ações Corretivas": [
                    "Definir e implementar ações corretivas com base no feedback e análise."
                ]
            },
            "Checklist Semanal do Gestor de Projetos": {
                "Revisão do Planejamento do Projeto": [
                    "Revisar o cronograma e as metas do projeto.",
                    "Verificar se o projeto está seguindo o plano."
                ],
                "Análise de Recursos": [
                    "Avaliar a alocação de recursos e ajustar conforme necessário."
                ],
                "Reuniões de Equipe": [
                    "Realizar reuniões de acompanhamento com a equipe de projeto.",
                    "Documentar todos os pontos discutidos e decisões tomadas."
                ],
                "Gestão de Riscos": [
                    "Identificar novos riscos e atualizar o plano de gerenciamento de riscos."
                ],
                "Revisão de Orçamento": [
                    "Verificar o status do orçamento e ajustar conforme necessário."
                ],
                "Comunicação com Stakeholders": [
                    "Manter comunicação contínua com todos os stakeholders do projeto."
                ],
                "Controle de Qualidade": [
                    "Garantir que todas as entregas atendam aos padrões de qualidade estabelecidos."
                ],
                "Preparação de Relatórios de Status": [
                    "Preparar relatórios de status e progresso para os stakeholders."
                ],
                "Planejamento de Próximos Passos": [
                    "Planejar os próximos passos e atividades para a semana seguinte."
                ]
            }
        }

        selected_checklist = st.selectbox("Escolha o checklist:", checklist_items.keys(), key="mkt_checklist_selecionar")
        checklist_items = checklist_items[selected_checklist]

        results = {}

        st.header("Marque os itens concluídos")

        for category, items in checklist_items.items():
            st.subheader(category)
            for idx, item in enumerate(items):
                results[item] = st.checkbox(item, value=False, key=f"mkt_{category}_{idx}")

        st.header("Observações e Comentários Adicionais")
        observations = st.text_area("Comentários gerais sobre o desempenho e áreas para melhorias", key="mkt_observacoes")
        results["Observações e Comentários Adicionais"] = observations

        st.header("Assinatura do Revisor")
        reviewer_signature = st.text_input("Assinatura do Revisor", key="mkt_assinatura_revisor")

        if st.button("Calcular Nota Geral", key="mkt_calcular"):
            if not reviewer_signature:
                st.error("A assinatura do revisor é obrigatória para calcular a nota geral.")
            else:
                score = calculate_score_simple([item for sublist in checklist_items.values() for item in sublist], results)
                checklist_completion = calculate_progress([item for sublist in checklist_items.values() for item in sublist], results)
                st.write(f"Nota Geral: {score}/10")
                st.write(f"Nota Ideal: {ideal_score}/10")
                st.write(f"Checklists Concluídas: {checklist_completion}%")

        if st.button("Salvar e Enviar", key="mkt_salvar_enviar"):
            if reviewer_signature:
                save_and_send_checklist_mkt(results, reviewer_signature, score)
                st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o MKT.")
            else:
                st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

        if st.button("Enviar", key="mkt_enviar"):
            if "filepath" in st.session_state:
                st.success(f"Checklist enviado para o MKT! Caminho do arquivo: {st.session_state.filepath}")
            else:
                st.error("Primeiro, salve a checklist antes de enviar.")

    st.title("Arquivos Recebidos")

    sort_by = st.selectbox("Ordenar por", ["Nome do arquivo", "Ordem de Mês"], key="mkt_sort_by")

    files = list_received_files()
    files = sort_files(files, sort_by='name' if sort_by == 'Nome do arquivo' else 'month')

    if files:
        selected_file = st.selectbox("Escolha um arquivo para visualizar", files, key="mkt_selecionar_arquivo")
        if selected_file:
            filepath = os.path.join("arquivos_recebidos_3", selected_file)
            display_file_content(filepath)
    else:
        st.info("Nenhum arquivo recebido ainda.")

# Interface do Streamlit para o SEO
def seo_interface():
    st.title("Business Book do Diretor | & CEO Executivo da Tecnology Academy")

    ideal_score = 8.0
    score = 0.0  # Inicializa a variável score
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 40px;">
                <h1 style="font-size: 4em; color: #ff6347;">{ideal_score}</h1>
                <h3>Nota Ideal</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        checklist_items = {
            "Checklist Semanal do SEO com o MKT Gestor/Gerente de Marketing": [
                "Revisar o desempenho de SEO das últimas campanhas.",
                "Analisar métricas de tráfego e engajamento.",
                "Verificar a implementação de estratégias de palavras-chave.",
                "Atualizar e otimizar o conteúdo existente.",
                "Identificar e corrigir problemas técnicos no site.",
                "Fazer análises de concorrência e tendências de mercado.",
                "Gerar relatórios de desempenho e apresentar resultados.",
                "Ajustar estratégias com base nos dados coletados."
            ],
            
            "Checklist Semanal para Revisão com o Cientista de Dados": [
                "Revisar os dados de SEO e suas análises.",
                "Garantir a integridade e precisão dos dados.",
                "Analisar padrões e tendências de tráfego.",
                "Preparar relatórios detalhados e insights para a equipe.",
                "Discutir estratégias de otimização com base nos dados.",
                "Revisar e ajustar modelos preditivos e análises avançadas.",
                "Garantir que os dados estejam alinhados com os objetivos de SEO.",
                "Coletar feedback da equipe sobre as análises realizadas."
            ]
        }
        
        selected_checklist = st.selectbox("Escolha o checklist:", checklist_items.keys(), key="seo_checklist_selecionar")
        checklist_items = checklist_items[selected_checklist]

        results = {}

        st.header("Marque os itens concluídos")

        for idx, item in enumerate(checklist_items):
            results[item] = st.checkbox(item, value=False, key=f"seo_{idx}")

        st.header("Observações e Comentários Adicionais")
        observations = st.text_area("Comentários gerais sobre o desempenho e áreas para melhorias", key="seo_observacoes")
        results["Observações e Comentários Adicionais"] = observations

        st.header("Assinatura do Revisor")
        reviewer_signature = st.text_input("Assinatura do Revisor", key="seo_assinatura_revisor")

        if st.button("Calcular Nota Geral", key="seo_calcular"):
            if not reviewer_signature:
                st.error("A assinatura do revisor é obrigatória para calcular a nota geral.")
            else:
                score = calculate_score_simple(checklist_items, results)
                checklist_completion = calculate_progress(checklist_items, results)
                st.write(f"Nota Geral: {score}/10")
                st.write(f"Nota Ideal: {ideal_score}/10")
                st.write(f"Checklists Concluídas: {checklist_completion}%")

        if st.button("Salvar e Enviar", key="seo_salvar_enviar"):
            if reviewer_signature:
                save_and_send_checklist_seo(results, reviewer_signature, score)
                st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o SEO.")
            else:
                st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

        if st.button("Enviar", key="seo_enviar"):
            if "filepath" in st.session_state:
                st.success(f"Checklist enviado para o SEO! Caminho do arquivo: {st.session_state.filepath}")
            else:
                st.error("Primeiro, salve a checklist antes de enviar.")

    st.title("Arquivos Recebidos")

    sort_by = st.selectbox("Ordenar por", ["Nome do arquivo", "Ordem de Mês"], key="seo_sort_by")

    files = list_received_files()
    files = sort_files(files, sort_by='name' if sort_by == 'Nome do arquivo' else 'month')
    
    if files:
        selected_file = st.selectbox("Escolha um arquivo para visualizar", files, key="seo_selecionar_arquivo")
        if selected_file:
            filepath = os.path.join("arquivos_recebidos_2", selected_file)
            display_file_content(filepath)
    else:
        st.info("Nenhum arquivo recebido ainda.")

# Interface de Login e Cadastro
def login_cadastro():
    st.title("Login e Cadastro")

    # Inicialize o estado da sessão se não estiver definido
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'registration_complete' not in st.session_state:
        st.session_state.registration_complete = False
    
    if st.session_state.logged_in:
        st.success(f"Bem-vindo, {st.session_state.username}!")
        return

    # Escolha entre Login ou Cadastro
    option = st.selectbox("Escolha uma opção", ["Login", "Cadastro"])

    if option == "Login":
        st.header("Faça o Login")
        username = st.text_input("Nome de Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            # Aqui você pode implementar a lógica para verificar o login
            # Exemplo: Verificação fictícia
            if username and password:  # Suponha que qualquer combinação funcione para fins de exemplo
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login realizado com sucesso!")
            else:
                st.error("Nome de usuário ou senha incorretos. Tente novamente.")
    
    elif option == "Cadastro":
        st.header("Faça o Cadastro")
        username = st.text_input("Nome de Usuário")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirme a Senha", type="password")

        if st.button("Cadastrar"):
            if password == confirm_password:
                # Aqui você pode implementar a lógica para salvar o novo usuário
                st.session_state.username = username
                st.session_state.registration_complete = True
                st.success("Cadastro realizado com sucesso! Agora faça login para acessar a plataforma.")
                st.session_state.logged_in = False  # Assegure que o usuário será solicitado a fazer login
            else:
                st.error("As senhas não coincidem. Tente novamente.")

    # Título estilizado abaixo da seção de login e cadastro
    st.markdown("<h2 style='text-align: center; color: #007bff;'> Sistema de gestão comercial |                _DevLucas</h2>", unsafe_allow_html=True)                


    # Seção de Redes Sociais
    st.markdown("""
    <h1 align="center"></h1>
    <div style="text-align: center;">
        <a href="mailto:lachimolalala61@gmail.com">
            <img width="30" src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png" alt="gmail">
        </a>
        <a href="https://www.linkedin.com/in/miguel-lucas-60091119b/">
            <img width="25" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linkedin/linkedin-original.svg" alt="linkedin">
        </a>
        <a href="https://www.youtube.com/channel/UCd5Ivcm28R1C3fCQKbOx2cg">
            <img width="35" src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="youtube">
        </a>
        <a href="https://www.instagram.com/devparadev/">
            <img width="25" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="instagram">
        </a>
    </div>
    <br>
    <div style="text-align: center;">
    </div>
    """, unsafe_allow_html=True)

# Função principal para a interface de boas-vindas e navegação
def main():
    # Verificar se o usuário está logado
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_cadastro()
    else:
        st.title(f"Bem-vindo, {st.session_state.username}!")
        st.success("Seu cadastro foi realizado com sucesso!")        
        st.sidebar.title("Menu")
        role = st.sidebar.selectbox("Escolha o papel:", ["Dono", "MKT", "SEO"])

        if role == "Dono":
            dono_interface()
        elif role == "MKT":
            mkt_interface()
        elif role == "SEO":
            seo_interface()

if __name__ == "__main__":
    main()
