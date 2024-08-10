import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

# Diretório para salvar arquivos recebidos
os.makedirs("arquivos_recebidos", exist_ok=True)

# Função para salvar os resultados em um arquivo CSV
def save_to_csv(data, filename):
    filepath = os.path.join("arquivos_recebidos", filename)
    df = pd.DataFrame([data])
    df.to_csv(filepath, index=False)
    st.success(f"Arquivo salvo como {filename} em 'arquivos_recebidos'")

# Função para salvar e enviar a checklist
def save_and_send_checklist(results, signature, score):
    unique_id = uuid.uuid4().hex
    filename = f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}.csv"
    data = {**results, "Assinatura do Revisor": signature, "Nota Geral": score}
    save_to_csv(data, filename)
    st.session_state.filepath = os.path.join("arquivos_recebidos", filename)

# Função para calcular a nota final para checklist com itens simples
def calculate_score_simple(checklist_items, results):
    total_items = len(checklist_items)
    checked_items = sum(results.get(item, False) for item in checklist_items)
    score = (checked_items / total_items) * 10
    return round(score, 1)

# Função para calcular o progresso do checklist (porcentagem concluída)
def calculate_progress(checklist_items, results):
    total_items = len(checklist_items)
    checked_items = sum(results.get(item, False) for item in checklist_items)
    return round((checked_items / total_items) * 100, 1)

# Função para listar arquivos recebidos
def list_received_files():
    files = [f for f in os.listdir("arquivos_recebidos") if f.endswith(".csv")]
    return files

# Função para extrair a data do nome do arquivo
def extract_date_from_filename(filename):
    try:
        # Parte do nome do arquivo para extrair a data
        date_str = filename.split('_')[2]  # Assume que a data está na terceira posição
        # Converte a string de data para um objeto datetime
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        return date_obj.date()
    except (IndexError, ValueError) as e:
        st.error(f"Erro ao extrair a data do arquivo '{filename}': {e}")
        return "Data inválida"

# Função para exibir o conteúdo de um arquivo CSV (filtrando apenas as colunas desejadas)
def display_file_content(filepath):
    df = pd.read_csv(filepath)
    
    # Verificar se as colunas esperadas existem no DataFrame
    if "Assinatura do Revisor" in df.columns and "Nota Geral" in df.columns:
        # Selecionar apenas as colunas desejadas
        df_filtered = df[["Assinatura do Revisor", "Nota Geral"]]
        # Adicionar a coluna de data
        file_name = os.path.basename(filepath)
        date_of_file = extract_date_from_filename(file_name)
        df_filtered["Data"] = date_of_file
        st.write(df_filtered)
    else:
        st.warning("O arquivo selecionado não contém as colunas esperadas.")

# Função para ordenar arquivos por nome ou mês
def sort_files(files, sort_by='name'):
    if sort_by == 'name':
        files.sort()
    elif sort_by == 'month':
        files.sort(key=lambda x: extract_date_from_filename(x) if extract_date_from_filename(x) != "Data inválida" else datetime(1900, 1, 1))
    return files

# Interface do Streamlit para o Dono
def dono_interface():
    st.title("Checklist Mensal do Dono com o CEO Diretor Executivo da Empresa")

    # Nota Ideal
    ideal_score = 8.0

    # Layout com coluna para a Nota Ideal
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 40px;">
                <h1 style="font-size: 4em; color: #ff6347;">{ideal_score}</h1>
                <h3>Nota Ideal</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Definir o checklist
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

        # Inicializar o dicionário para armazenar os resultados
        results = {}

        # Mostrar checklist com caixas de seleção
        st.header("Marque os itens concluídos")

        for item in checklist_items:
            results[item] = st.checkbox(item, value=False)

        st.header("Observações e Comentários Adicionais")
        observations = st.text_area("Comentários gerais sobre o desempenho do CEO e áreas para melhorias")
        results["Observações e Comentários Adicionais"] = observations

        st.header("Assinatura do Revisor")
        reviewer_signature = st.text_input("Assinatura do Revisor", key="ceo_assinatura_revisor")

        if st.button("Calcular Nota Geral"):
            if not reviewer_signature:
                st.error("A assinatura do revisor é obrigatória para calcular a nota geral.")
            else:
                score = calculate_score_simple(checklist_items, results)
                checklist_completion = calculate_progress(checklist_items, results)
                st.write(f"Nota Geral: {score}/10")
                st.write(f"Nota Ideal: {ideal_score}/10")
                st.write(f"Checklists Concluídas: {checklist_completion}%")

        if st.button("Salvar e Enviar"):
            if reviewer_signature:
                save_and_send_checklist(results, reviewer_signature, score)
                st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o Dono.")
            else:
                st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

        if st.button("Enviar"):
            if "filepath" in st.session_state:
                st.success(f"Checklist enviado para o Dono! Caminho do arquivo: {st.session_state.filepath}")
            else:
                st.error("Primeiro, salve a checklist antes de enviar.")

    st.title("Arquivos Recebidos")

    # Filtros de ordenação
    sort_by = st.selectbox("Ordenar por", ["Nome do arquivo", "Ordem de Mês"])

    # Listar e ordenar arquivos recebidos
    files = list_received_files()
    files = sort_files(files, sort_by='name' if sort_by == 'Nome do arquivo' else 'month')

    if files:
        selected_file = st.selectbox("Escolha um arquivo para visualizar", files)
        if selected_file:
            filepath = os.path.join("arquivos_recebidos", selected_file)
            display_file_content(filepath)
    else:
        st.info("Nenhum arquivo recebido ainda.")

# Interface do Streamlit para o MKT
def mkt_interface():
    st.title("Checklist de Marketing")

    # Nota Ideal
    ideal_score = 9.0

    # Layout com coluna para a Nota Ideal
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 40px;">
                <h1 style="font-size: 4em; color: #ff6347;">{ideal_score}</h1>
                <h3>Nota Ideal</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Definir o checklist
        checklist_items = [
            "Análise de Mercado",
            "Planejamento Estratégico de Marketing",
            "Execução de Campanhas Publicitárias",
            "Gestão de Redes Sociais",
            "Criação de Conteúdo",
            "Pesquisa de Concorrência",
            "Avaliação de Desempenho de Campanhas",
            "Otimização de SEO",
            "Gestão de Orçamento de Marketing"
        ]

        # Inicializar o dicionário para armazenar os resultados
        results = {}

        # Mostrar checklist com caixas de seleção
        st.header("Marque os itens concluídos")

        for item in checklist_items:
            results[item] = st.checkbox(item, value=False)

        st.header("Observações e Comentários Adicionais")
        observations = st.text_area("Comentários gerais sobre o desempenho de Marketing e áreas para melhorias")
        results["Observações e Comentários Adicionais"] = observations

        st.header("Assinatura do Revisor")
        reviewer_signature = st.text_input("Assinatura do Revisor", key="mkt_assinatura_revisor")

        if st.button("Calcular Nota Geral"):
            if not reviewer_signature:
                st.error("A assinatura do revisor é obrigatória para calcular a nota geral.")
            else:
                score = calculate_score_simple(checklist_items, results)
                checklist_completion = calculate_progress(checklist_items, results)
                st.write(f"Nota Geral: {score}/10")
                st.write(f"Nota Ideal: {ideal_score}/10")
                st.write(f"Checklists Concluídas: {checklist_completion}%")

        if st.button("Salvar e Enviar"):
            if reviewer_signature:
                save_and_send_checklist(results, reviewer_signature, score)
                st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o MKT.")
            else:
                st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

        if st.button("Enviar"):
            if "filepath" in st.session_state:
                st.success(f"Checklist enviado para o MKT! Caminho do arquivo: {st.session_state.filepath}")
            else:
                st.error("Primeiro, salve a checklist antes de enviar.")

    st.title("Arquivos Recebidos")

    # Filtros de ordenação
    sort_by = st.selectbox("Ordenar por", ["Nome do arquivo", "Ordem de Mês"])

    # Listar e ordenar arquivos recebidos
    files = list_received_files()
    files = sort_files(files, sort_by='name' if sort_by == 'Nome do arquivo' else 'month')

    if files:
        selected_file = st.selectbox("Escolha um arquivo para visualizar", files)
        if selected_file:
            filepath = os.path.join("arquivos_recebidos", selected_file)
            display_file_content(filepath)
    else:
        st.info("Nenhum arquivo recebido ainda.")

# Interface do Streamlit para SEO
def seo_interface():
    st.title("Checklist de SEO")

    # Nota Ideal
    ideal_score = 7.5

    # Layout com coluna para a Nota Ideal
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 40px;">
                <h1 style="font-size: 4em; color: #ff6347;">{ideal_score}</h1>
                <h3>Nota Ideal</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Definir o checklist
        checklist_items = [
            "Análise de Palavras-Chave",
            "Otimização On-Page",
            "Link Building",
            "Análise de Concorrência",
            "Monitoramento de Rankings",
            "Estratégia de Conteúdo",
            "SEO Técnico",
            "Avaliação de Backlinks"
        ]

        # Inicializar o dicionário para armazenar os resultados
        results = {}

        # Mostrar checklist com caixas de seleção
        st.header("Marque os itens concluídos")

        for item in checklist_items:
            results[item] = st.checkbox(item, value=False)

        st.header("Observações e Comentários Adicionais")
        observations = st.text_area("Comentários gerais sobre o desempenho de SEO e áreas para melhorias")
        results["Observações e Comentários Adicionais"] = observations

        st.header("Assinatura do Revisor")
        reviewer_signature = st.text_input("Assinatura do Revisor", key="seo_assinatura_revisor")

        if st.button("Calcular Nota Geral"):
            if not reviewer_signature:
                st.error("A assinatura do revisor é obrigatória para calcular a nota geral.")
            else:
                score = calculate_score_simple(checklist_items, results)
                checklist_completion = calculate_progress(checklist_items, results)
                st.write(f"Nota Geral: {score}/10")
                st.write(f"Nota Ideal: {ideal_score}/10")
                st.write(f"Checklists Concluídas: {checklist_completion}%")

        if st.button("Salvar e Enviar"):
            if reviewer_signature:
                save_and_send_checklist(results, reviewer_signature, score)
                st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o SEO.")
            else:
                st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

        if st.button("Enviar"):
            if "filepath" in st.session_state:
                st.success(f"Checklist enviado para o SEO! Caminho do arquivo: {st.session_state.filepath}")
            else:
                st.error("Primeiro, salve a checklist antes de enviar.")

    st.title("Arquivos Recebidos")

    # Filtros de ordenação
    sort_by = st.selectbox("Ordenar por", ["Nome do arquivo", "Ordem de Mês"])

    # Listar e ordenar arquivos recebidos
    files = list_received_files()
    files = sort_files(files, sort_by='name' if sort_by == 'Nome do arquivo' else 'month')

    if files:
        selected_file = st.selectbox("Escolha um arquivo para visualizar", files)
        if selected_file:
            filepath = os.path.join("arquivos_recebidos", selected_file)
            display_file_content(filepath)
    else:
        st.info("Nenhum arquivo recebido ainda.")

# Interface de Login e Cadastro
def login_cadastro():
    st.title("Login e Cadastro")

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
                st.experimental_rerun()
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
                st.experimental_rerun()
            else:
                st.error("As senhas não coincidem. Tente novamente.")

# Função principal para a interface de boas-vindas e navegação
def main():
    # Verificar se o usuário está logado
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_cadastro()
    else:
        st.title(f"Bem-vindo, {st.session_state.username}!")
        st.success("Seu cadastro foi realizado com sucesso!")

        # Captura do cargo do usuário
        cargo = st.selectbox("Escolha o cargo", ["Dono", "Marketing", "SEO"])

        if cargo == "Dono":
            dono_interface()
        elif cargo == "Marketing":
            mkt_interface()
        elif cargo == "SEO":
            seo_interface()

if __name__ == "__main__":
    main()
