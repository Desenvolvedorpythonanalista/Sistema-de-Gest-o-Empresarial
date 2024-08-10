import os

def search_term_in_files(directory, term):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if term in content:
                        print(f"Termo '{term}' encontrado no arquivo: {file_path}")
            except (IOError, UnicodeDecodeError) as e:
                print(f"Erro ao ler o arquivo {file_path}: {e}")

# Substitua 'seu_diretorio' pelo diretório onde está o código
search_term_in_files('seu_diretorio', 'arquivos_recebidos')
