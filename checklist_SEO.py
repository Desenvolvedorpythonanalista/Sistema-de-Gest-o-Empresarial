import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

# Função para criar diretório se não existir
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Função para salvar os resultados em um arquivo CSV
def save_to_csv(data, filename):
    ensure_directory_exists("arquivos_recebidos")
    filepath = os.path.join("arquivos_recebidos", filename)
    df = pd.DataFrame([data])
    df.to_csv(filepath, index=False)
    st.success(f"Arquivo salvo como {filename} em arquivos_recebidos")

# Função para salvar e enviar a checklist
def save_and_send_checklist(results, signature, score):
    unique_id = uuid.uuid4().hex
    filename = f"checklist_marketing_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}.csv"
    data = {**results, "Assinatura do Revisor": signature, "Nota Geral": score}
    save_to_csv(data, filename)
    st.session_state.filepath = os.path.join("arquivos_recebidos", filename)

# Função para calcular a nota final para checklist com itens simples
def calculate_score_simple(checklist_items, results):
    total_items = len(checklist_items)
    checked_items = sum(results.get(item, False) for item in checklist_items)
    score = (checked_items / total_items) * 10
    return round(score, 1)

# Função para calcular a nota final para checklist com sub-itens
def calculate_score_with_subitems(checklist_items, results):
    total_items = sum(len(sub_items) for sub_items in checklist_items.values())
    checked_items = sum(sum(results.get(item, []).count(True)) for item in checklist_items)
    score = (checked_items / total_items) * 10
    return round(score, 1)

# Função para calcular o progresso do checklist (porcentagem concluída)
def calculate_progress(checklist_items, results):
    total_items = len(checklist_items)
    checked_items = sum(results.get(item, False) for item in checklist_items)
    return round((checked_items / total_items) * 100, 1)

# Função para salvar arquivos recebidos
def save_uploaded_file(uploaded_file):
    ensure_directory_exists("arquivos_recebidos_2")
    file_path = os.path.join("arquivos_recebidos_2", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

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

# Função para listar arquivos recebidos na pasta correta
def list_received_files():
    ensure_directory_exists("arquivos_recebidos_2")
    files = [f for f in os.listdir("arquivos_recebidos_2") if f.endswith(".csv")]
    return files

# Função para ordenar arquivos por nome ou mês
def sort_files(files, sort_by='name'):
    if sort_by == 'name':
        files.sort()
    elif sort_by == 'month':
        files.sort(key=lambda x: extract_date_from_filename(x) if extract_date_from_filename(x) != "Data inválida" else datetime(1900, 1, 1))
    return files

# Função para listar arquivos de um diretório específico
def list_files_in_directory(directory):
    ensure_directory_exists(directory)
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    return files

# Função para exibir o conteúdo de um arquivo CSV a partir de um diretório específico
def display_file_content_from_directory(directory, filename):
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        # Exibir apenas as colunas "Data", "Assinatura do Revisor" e "Nota Geral"
        columns_to_show = ["Data", "Assinatura do Revisor", "Nota Geral"]
        df_filtered = df[columns_to_show] if all(col in df.columns for col in columns_to_show) else pd.DataFrame()
        st.write("Conteúdo do arquivo:")
        st.write(df_filtered)
    else:
        st.error(f"Arquivo não encontrado: {filepath}")

# Interface do Streamlit
def main():
    st.title("Checklist Marketing")

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
        # Seleção do tipo de checklist
        checklist_type = st.radio("Escolha o Checklist", 
                                  ["Checklist Semanal do SEO com o MKT Gestor/Gerente de Marketing",
                                   "Checklist Semanal para Revisão com o Cientista de Dados"])

        # Inicializar as variáveis score e resultados no session_state
        if "score" not in st.session_state:
            st.session_state.score = None
        if "results" not in st.session_state:
            st.session_state.results = {}
        if "reviewer_signature" not in st.session_state:
            st.session_state.reviewer_signature = ""

        if checklist_type == "Checklist Semanal do SEO com o MKT Gestor/Gerente de Marketing":
            st.header("Checklist Semanal do SEO com o MKT Gestor/Gerente de Marketing")
            data = st.date_input("Data", value=datetime.today())
            st.session_state.results["Data"] = data

            checklist_items = {
                "Implementar Estratégias Comerciais de Marketing": [
                    "Atualizou estratégias comerciais e ajustou campanhas com base em dados recentes."
                ],
                "Fechar Propostas Comerciais": [
                    "Revisou e enviou propostas comerciais; garantiu clareza nas metas de vendas."
                ],
                "Gerenciar Vendas e Marketing": [
                    "Realizou reuniões para revisar progresso e ajustou a autonomia dos departamentos."
                ],
                "Identificar Oportunidades": [
                    "Atualizou dashboards e ajustou planos com base em novas oportunidades e previsões."
                ],
                "Monitorar Resultados de Contratos e E-mail Marketing": [
                    "Avaliou resultados de contratos e campanhas de e-mail marketing, ajustando estratégias conforme necessário."
                ],
                "Coordenar Atividades Promocionais": [
                    "Planejou e revisou eventos promocionais e logísticas associadas."
                ],
                "Testar Desempenho dos Canais de Vendas e Redes Sociais": [
                    "Monitorou e ajustou o desempenho dos canais de vendas e redes sociais."
                ],
                "Revisar Métricas de Dados": [
                    "Conferiu métricas de desempenho e ajustou estratégias baseadas nos dados."
                ],
                "Liderar Criadores de Conteúdo e Social Media": [
                    "Revisou e ajustou planos de conteúdo e campanhas de social media."
                ],
                "Explorar Potencial dos Anúncios": [
                    "Avaliou e ajustou estratégias de anúncios conforme o desempenho observado."
                ]
            }

            st.header("Marque os itens concluídos")

            for item in checklist_items:
                st.session_state.results[item] = st.checkbox(item, value=False, key=f"mkt_{item}")

            st.header("Observações e Comentários Adicionais")
            observations = st.text_area("Comentários gerais sobre o desempenho do Gestor/Gerente de Marketing e áreas para melhorias")
            st.session_state.results["Observações e Comentários Adicionais"] = observations

            st.header("Próximos Passos e Ações")
            actions = st.text_area("Defina ações a serem tomadas antes da próxima reunião")
            st.session_state.results["Próximos Passos e Ações"] = actions

            st.header("Assinatura do Revisor")
            st.session_state.reviewer_signature = st.text_input("Assinatura do Revisor", key="mkt_assinatura_revisor")
            
            # Botão de calcular a nota geral
            if st.button("Calcular Nota Geral", key="calcular_nota_geral_mkt_gerente"):
                if not st.session_state.reviewer_signature:
                    st.error("A assinatura do revisor é obrigatória para calcular a nota geral.")
                else:
                    st.session_state.score = calculate_score_simple(checklist_items.keys(), st.session_state.results)
                    checklist_completion = calculate_progress(checklist_items, st.session_state.results)
                    st.write(f"Nota Geral: {st.session_state.score}/10")
                    st.write(f"Nota Ideal: {ideal_score}/10")
                    st.write(f"Checklists Concluídas: {checklist_completion}%")
            
            # Botão de salvar e enviar
            if st.button("Salvar e Enviar", key="salvar_enviar_mkt_gerente"):
                if st.session_state.reviewer_signature:
                    if st.session_state.score is not None:  # Verificar se a nota foi calculada
                        save_and_send_checklist(st.session_state.results, st.session_state.reviewer_signature, st.session_state.score)
                        st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o Dono.")
                    else:
                        st.error("Primeiro, calcule a nota geral antes de salvar e enviar.")
                else:
                    st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

            # Botão de enviar
            if st.button("Enviar", key="enviar_mkt_gerente"):
                if "filepath" in st.session_state:
                    st.success(f"Checklist enviado para o Dono! Caminho do arquivo: {st.session_state.filepath}")
                else:
                    st.error("Primeiro, salve a checklist antes de enviar.")

        elif checklist_type == "Checklist Semanal para Revisão com o Cientista de Dados":
            st.header("Checklist Semanal para Revisão com o Cientista de Dados")
            data = st.date_input("Data da Reunião", value=datetime.today())
            st.session_state.results["Data da Reunião"] = data

            checklist_items = {
                "Análise de Dados": [
                    "Revisão dos grandes volumes de dados analisados e insights gerados.",
                    "Avaliação dos modelos estatísticos e algoritmos de machine learning desenvolvidos."
                ],
                "Desenvolvimento e Manutenção de Dashboards": [
                    "Verificação dos dashboards atualizados em tempo real e adequação às necessidades dos setores.",
                    "Revisão dos relatórios gerados e sua precisão."
                ],
                "Colaboração e Implementação": [
                    "Avaliação da colaboração com diferentes departamentos para implementar soluções baseadas em dados.",
                    "Verificação do desenvolvimento e integração de soluções em Django."
                ],
                "Gerenciamento de Dados": [
                    "Revisão das atividades de gerenciamento, desenvolvimento e manutenção de bancos de dados relacionais.",
                    "Avaliação da integridade e otimização dos bancos de dados."
                ],
                "Identificação de Oportunidades": [
                    "Análise das oportunidades de destaque identificadas e ações tomadas para aproveitá-las."
                ]
            }

            st.header("Marque os itens concluídos")

            for item, sub_items in checklist_items.items():
                st.session_state.results[item] = [st.checkbox(sub_item, value=False, key=f"cientista_{item}_{i}") for i, sub_item in enumerate(sub_items)]

            st.header("Observações e Comentários Adicionais")
            observations = st.text_area("Comentários gerais sobre o desempenho do Cientista de Dados e áreas para melhorias")
            st.session_state.results["Observações e Comentários Adicionais"] = observations

            st.header("Próximos Passos e Ações")
            actions = st.text_area("Defina ações a serem tomadas antes da próxima reunião")
            st.session_state.results["Próximos Passos e Ações"] = actions

            st.header("Assinatura do Revisor")
            st.session_state.reviewer_signature = st.text_input("Digite o nome do revisor", key="cientista_assinatura_revisor")
            
            # Botão de calcular a nota geral
            if st.button("Calcular Nota Geral", key="calcular_nota_geral_cientista_dados"):
                if not st.session_state.reviewer_signature:
                    st.error("O campo 'Assinatura do Revisor' é obrigatório para calcular a nota geral.")
                else:
                    st.session_state.score = calculate_score_with_subitems(checklist_items, st.session_state.results)
                    checklist_completion = calculate_progress(checklist_items, st.session_state.results)
                    st.write(f"Nota Geral: {st.session_state.score}/10")
                    st.write(f"Nota Ideal: {ideal_score}/10")
                    st.write(f"Checklists Concluídas: {checklist_completion}%")
            
            # Botão de salvar e enviar
            if st.button("Salvar e Enviar", key="salvar_enviar_cientista_dados"):
                if st.session_state.reviewer_signature:
                    if st.session_state.score is not None:  # Verificar se a nota foi calculada
                        save_and_send_checklist(st.session_state.results, st.session_state.reviewer_signature, st.session_state.score)
                        st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o Dono.")
                    else:
                        st.error("Primeiro, calcule a nota geral antes de salvar e enviar.")
                else:
                    st.error("A assinatura do revisor é obrigatória para salvar e enviar os resultados.")

            # Botão de enviar
            if st.button("Enviar", key="enviar_cientista_dados"):
                if "filepath" in st.session_state:
                    st.success(f"Checklist enviado para o Dono! Caminho do arquivo: {st.session_state.filepath}")
                else:
                    st.error("Primeiro, salve a checklist antes de enviar.")

    st.title("Arquivos Recebidos")

    # Filtro de ordenação
    sort_by = st.selectbox("Ordenar por", ["Nome do arquivo", "Ordem de Mês"])

    # Listar e ordenar arquivos recebidos
    files = list_files_in_directory("arquivos_recebidos_2")
    files = sort_files(files, sort_by='name' if sort_by == 'Nome do arquivo' else 'month')

    if files:
        selected_file = st.selectbox("Escolha um arquivo para visualizar", files)
        if selected_file:
            filepath = os.path.join("arquivos_recebidos_2", selected_file)
            display_file_content_from_directory("arquivos_recebidos_2", selected_file)
    else:
        st.info("Nenhum arquivo recebido ainda.")

if __name__ == "__main__":
    main()
