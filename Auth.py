import json
import os
import random
import string

# Função para salvar dados do usuário
def save_user_data(user_data):
    """
    Salva ou atualiza os dados do usuário em um arquivo JSON.
    
    Parâmetros:
    - user_data (dict): Um dicionário contendo os dados do usuário (nome, e-mail, senha, etc.).
    
    Descrição:
    - Verifica se o arquivo 'users.json' existe. Se não existir, cria um novo arquivo com uma lista vazia.
    - Lê os dados existentes do arquivo e adiciona ou atualiza os dados do usuário.
    - Salva a lista atualizada de usuários no arquivo JSON.
    """
    # Verifica se o arquivo 'users.json' não existe
    if not os.path.exists("users.json"):
        # Cria um novo arquivo 'users.json' com uma lista vazia
        with open("users.json", "w") as file:
            json.dump([], file)
    
    # Abre o arquivo 'users.json' e carrega os dados existentes
    with open("users.json", "r") as file:
        users = json.load(file)
    
    # Verifica se já existe um usuário com o mesmo e-mail
    existing_user = next((user for user in users if user["email"] == user_data["email"]), None)
    if existing_user:
        # Atualiza os dados do usuário existente
        users = [user if user["email"] != user_data["email"] else user_data for user in users]
    else:
        # Adiciona um novo usuário à lista
        users.append(user_data)
    
    # Salva a lista atualizada de usuários no arquivo 'users.json'
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Função para autenticar o usuário
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
    - Se um número de crachá for fornecido, ele será verificado também.
    """
    # Abre o arquivo 'users.json' e carrega os dados dos usuários
    with open("users.json", "r") as file:
        users = json.load(file)
    
    # Verifica se o número de crachá foi fornecido
    if badge_number:
        # Autentica o usuário com base no e-mail, senha e número de crachá
        for user in users:
            if user["email"] == email and user["password"] == password and user["badge_number"] == badge_number:
                return user
    else:
        # Autentica o usuário com base apenas no e-mail e senha
        for user in users:
            if user["email"] == email and user["password"] == password:
                return user

    return None

# Função para atribuir um número de crachá a um usuário
def assign_badge_number(email, badge_number):
    """
    Atribui um número de crachá a um usuário existente.
    
    Parâmetros:
    - email (str): O e-mail do usuário.
    - badge_number (str): O número de crachá a ser atribuído.
    
    Retorna:
    - bool: Retorna True se a atribuição for bem-sucedida, caso contrário, retorna False.
    
    Descrição:
    - Lê os dados dos usuários do arquivo 'users.json'.
    - Atualiza o número de crachá do usuário com o e-mail fornecido.
    - Salva as alterações no arquivo 'users.json'.
    """
    # Verifica se o arquivo 'users.json' existe
    if not os.path.exists("users.json"):
        return False
    
    # Abre o arquivo 'users.json' e carrega os dados dos usuários
    with open("users.json", "r") as file:
        users = json.load(file)
    
    # Encontra o usuário com o e-mail fornecido e atualiza o número de crachá
    for user in users:
        if user["email"] == email:
            user["badge_number"] = badge_number
            # Salva as alterações no arquivo 'users.json'
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
            return True
    return False

# Função para gerar um número de crachá único (mockup para demonstração)
def generate_badge_number(length=6):
    """
    Gera um número de crachá único com um comprimento específico.
    
    Parâmetros:
    - length (int): O comprimento do número de crachá gerado (padrão é 6).
    
    Retorna:
    - str: O número de crachá gerado.
    
    Descrição:
    - Usa caracteres alfanuméricos (letras maiúsculas e dígitos) para gerar um número de crachá aleatório.
    """
    characters = string.ascii_uppercase + string.digits
    badge_number = ''.join(random.choice(characters) for _ in range(length))
    return badge_number

# Função para obter cargos disponíveis
def get_available_job_titles():
    """
    Obtém uma lista de cargos disponíveis.
    
    Retorna:
    - list: Uma lista de títulos de cargos disponíveis.
    
    Descrição:
    - Retorna uma lista fixa de títulos de cargos. Pode ser expandida ou modificada conforme necessário.
    """
    return ["SEO (Diretor Executivo)", "Dono", "Gerente de Marketing", "Outro"]
