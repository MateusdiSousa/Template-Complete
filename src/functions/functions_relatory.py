import json
import os

def get_jsons_dir(dir: str):
    """Obtém todos os arquivos JSON de um diretório"""
    jsons = []
    for nome_arquivo in os.listdir(dir):
        path_arquivo = os.path.join(dir, nome_arquivo)
        json_data = get_jsons_by_file(path=path_arquivo)
        if json_data is not None:  # Só adiciona se for um JSON válido
            jsons.append(json_data)
    return jsons

def get_jsons_by_file(path: str):
    """Carrega um único arquivo JSON"""
    if os.path.isfile(path=path) and path.endswith('.json'):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Erro ao ler arquivo {path}: {str(e)}")
            return None
    return None

def get_template_text(path_template: str):
    """Obtém o conteúdo do template"""
    if os.path.isfile(path=path_template):
        with open(path_template, 'r', encoding='utf-8') as file:
            return file.read()
    raise FileNotFoundError(f"Template não encontrado: {path_template}")

def write_relatory(path_output: str, text: str):
    """Escreve o relatório final"""
    os.makedirs(os.path.dirname(path_output), exist_ok=True)
    with open(path_output, 'w', encoding='utf-8') as file:
        file.write(text)

def substituir_texto_com_json(texto, dados_json):
    """Substitui placeholders no template pelos valores do JSON"""
    if not isinstance(dados_json, dict):
        raise ValueError("Dados JSON devem ser um dicionário")
    
    for key, value in dados_json.items():
        placeholder = "{{" + key + "}}"
        texto = texto.replace(placeholder, str(value))
    return texto

def generate_relatory_by_many_dir(path_template: str, path_tests: list, path_output: str):
    """Gera relatório a partir de múltiplos diretórios"""
    testes = []
    for path in path_tests:
        if os.path.isdir(path):
            testes.extend(get_jsons_dir(path))
        else:
            print(f"Aviso: {path} não é um diretório válido")

    template_text = get_template_text(path_template=path_template)
    
    new_text = ""
    for teste in testes:
        if teste:  # Verifica se não é None
            new_text += substituir_texto_com_json(template_text, teste) + "\n\n"
        
    write_relatory(path_output=path_output, text=new_text)

def generate_relatory_by_many_json(path_template: str, path_tests: list, path_output: str):
    """Gera relatório a partir de múltiplos arquivos JSON específicos"""
    testes = []
    for path in path_tests:
        if os.path.isfile(path):
            json_data = get_jsons_by_file(path)
            if json_data:
                testes.append(json_data)
        else:
            print(f"Aviso: {path} não é um arquivo válido")

    template_text = get_template_text(path_template=path_template)
    new_text = ""
    for teste in testes:
        new_text += substituir_texto_com_json(template_text, teste) + "\n\n"
        
    write_relatory(path_output=path_output, text=new_text)
