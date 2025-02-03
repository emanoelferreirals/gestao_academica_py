import markdown
import webbrowser
import tempfile

# Caminho do arquivo Markdown
file_path = 'database/explicacao_detalhada.md'

# Função para abrir e ler o conteúdo do arquivo Markdown com codificação UTF-8
def abrir_arquivo():
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Convertendo o conteúdo do Markdown para HTML
def converter_markdown_para_html(md_content):
    return markdown.markdown(md_content)

# Função para salvar o HTML temporário e abrir no navegador
def abrir_no_navegador(html_content):
    # Criando um arquivo temporário para armazenar o HTML
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as temp_file:
        temp_file.write(html_content)
        temp_file.close()  # Fechar o arquivo antes de abrir
        # Abrir o arquivo no navegador padrão
        webbrowser.open(f"file://{temp_file.name}")

# Lendo o conteúdo do arquivo Markdown
conteudo_md = abrir_arquivo()

# Convertendo o conteúdo para HTML
conteudo_html = converter_markdown_para_html(conteudo_md)

# Abrindo o HTML no navegador
abrir_no_navegador(conteudo_html)
