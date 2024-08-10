import pandas as pd
import matplotlib.pyplot as plt

# Defina o caminho para o seu arquivo CSV
file_path = r'C:\Users\NIL\Desktop\CHECKLIST\arquivos_recebidos_2\checklist_20240809_182209_cc2e128472fb4b1d849a0859b18a0e79.csv'

# Leia o arquivo CSV usando pandas
try:
    data = pd.read_csv(file_path)
    print("Arquivo carregado com sucesso.")
except FileNotFoundError:
    print(f"Erro: O arquivo {file_path} não foi encontrado.")
    exit()
except pd.errors.EmptyDataError:
    print("Erro: O arquivo está vazio.")
    exit()
except pd.errors.ParserError:
    print("Erro: O arquivo não pôde ser analisado.")
    exit()

# Exiba as primeiras linhas do DataFrame para entender a estrutura dos dados
print(data.head())

# Vamos supor que você queira plotar um histograma da coluna 'Nota Geral'
# Primeiro, verifique se a coluna 'Nota Geral' existe
if 'Nota Geral' in data.columns:
    # Extraia a coluna 'Nota Geral'
    nota_geral = data['Nota Geral'].dropna()  # Remove valores NaN para evitar erros no histograma
    
    # Crie o histograma
    plt.figure(figsize=(10, 6))
    plt.hist(nota_geral, bins=10, edgecolor='black', alpha=0.7)
    plt.title('Distribuição da Nota Geral')
    plt.xlabel('Nota Geral')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.show()
else:
    print("A coluna 'Nota Geral' não foi encontrada no arquivo CSV.")
