import streamlit as st
from datetime import datetime
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import uuid
import pandas as pd

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Função para calcular a nota geral
def calculate_score(checklist_items, results):
    total_items = len(checklist_items)
    completed_items = sum([results.get(item, False) for item in checklist_items])
    score = (completed_items / total_items) * 10
    return round(score, 1)

# Função para calcular o progresso em percentual
def calculate_progress(checklist_items, results):
    total_items = len(checklist_items)
    completed_items = sum([results.get(item, False) for item in checklist_items])
    progress = (completed_items / total_items) * 100
    return round(progress, 1)

# Função para garantir que o diretório existe
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Função para salvar os resultados em um arquivo CSV
def save_to_csv(data, filename):
    ensure_directory_exists("arquivos_recebidos_2")  # Verifica e cria a pasta se não existir
    filepath = os.path.join("arquivos_recebidos_2", filename)
    df = pd.DataFrame([data])
    df.to_csv(filepath, index=False)
    st.success(f"Arquivo salvo como {filename} em arquivos_recebidos_2")
    
# Função para salvar e enviar a checklist
def save_and_send_checklist(results, signature, score):
    unique_id = uuid.uuid4().hex
    filename = f"checklist_marketing_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{unique_id}.csv"
    data = {**results, "Assinatura do Revisor": signature, "Nota Geral": score}
    save_to_csv(data, filename)
    st.session_state.filepath = os.path.join("arquivos_recebidos_2", filename)

# Função para listar arquivos recebidos na pasta correta
def list_received_files():
    ensure_directory_exists("arquivos_recebidos_2")
    files = [f for f in os.listdir("arquivos_recebidos_2") if f.endswith(".csv")]
    return files

# Função principal para exibir o aplicativo
def main():
    if 'file_to_send' not in st.session_state:
        st.session_state.file_to_send = None

    st.title("Sistema de Checklist Semanal")

    ideal_scores = {
        "Checklist Semanal do Consultor/Assessor de Negócios": 10,
        "Checklist Semanal do Editor de Vídeos": 8,
        "Checklist Semanal do Especialista em Produto": 9,
        "Checklist Semanal do Gestor de Projetos": 8
    }

    checklist_type = st.selectbox(
        "Selecione o tipo de checklist:",
        list(ideal_scores.keys())
    )

    ideal_score = ideal_scores[checklist_type]
    st.write(f"Nota Ideal para este checklist: {ideal_score}/10")

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

    items = checklist_items.get(checklist_type, {})
    data = st.date_input("Data", value=datetime.today())
    results = {"Data": data}

    st.header(f"Checklist Semanal do {checklist_type}")

    st.header("Marque os itens concluídos")
    for item in items.keys():
        results[item] = st.checkbox(item, value=False)

    st.header("Observações e Comentários Adicionais")
    observations = st.text_area(f"Comentários gerais sobre o desempenho do {checklist_type} e áreas para melhorias")
    results["Observações e Comentários Adicionais"] = observations

    st.header("Próximos Passos e Ações")
    actions = st.text_area("Defina ações a serem tomadas antes do próximo dia")
    results["Próximos Passos e Ações"] = actions

    st.header("Assinatura do Revisor")
    signature = st.text_input("Assinatura do Revisor")
    results["Assinatura do Revisor"] = signature

    if st.button("Calcular Nota Geral"):
        if not signature:
            st.error("O campo 'Assinatura do Revisor' é obrigatório para calcular a nota geral.")
        else:
            score = calculate_score(items, results)
            checklist_completion = calculate_progress(items, results)
            st.write(f"Nota Geral: {score}/10")
            st.write(f"Nota Ideal: {ideal_score}/10")
            st.write(f"Checklists Concluídas: {checklist_completion}%")

    if st.button("Salvar e Enviar"):
        if not signature:
            st.error("O campo 'Assinatura do Revisor' é obrigatório para salvar e enviar.")
        else:
            score = calculate_score(items, results)
            save_and_send_checklist(results, signature, score)
            st.info("Agora você pode clicar em 'Enviar' para enviar a checklist para o Dono.")

    if st.button("Enviar"):
        if st.session_state.filepath and os.path.isfile(st.session_state.filepath):
            st.success(f"Checklist enviada com sucesso! Arquivo: {st.session_state.filepath}")
        else:
            st.error("Primeiro, salve a checklist antes de enviar.")

if __name__ == "__main__":
    main()
