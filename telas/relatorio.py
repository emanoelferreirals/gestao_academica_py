import os
import tkinter as tk
from tkinter import messagebox, filedialog
from groq import Groq
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap

# Definir chave da API
os.environ["GROQ_API_KEY"] = "chave"  # Substitua pela sua chave correta

# Configuração do cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def exibir_tela(element_pai):
    # Função para gerar relatóriox
    def gerar_relatorio(notas):
        prompt = f"""
        Baseado nas seguintes notas do aluno, gere um relatório de desempenho e sugira um plano de estudos:
        
        {notas}
        
        O relatório deve incluir:
        - Um resumo do desempenho do aluno.
        - Pontos fortes e fracos.
        - Sugestões de estudo para melhorar as notas mais baixas.
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content  # Retorna o texto gerado
        except Exception as e:
            return f"Erro ao gerar relatório: {e}"

    # Função para mostrar relatório
    def mostrar_relatorio():
        global relatorio_texto  

        notas = [
            {"Matéria": "Matemática", "Período": "1", "n1": "10", "n2": "20", "n3": "12", "n4": "100"},
            {"Matéria": "Portugues", "Período": "6", "n1": "90", "n2": "89", "n3": "30", "n4": "100"},
        ]
        
        relatorio_texto = gerar_relatorio(notas)
        
        # Atualizar área de exibição no Tkinter
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, markdown_to_text(relatorio_texto))  # Converte Markdown para texto puro
        text_widget.config(state=tk.DISABLED)

    # Função para converter Markdown para texto limpo
    def markdown_to_text(md_content):
        """Remove tags do Markdown e retorna um texto mais limpo"""
        md_content = md_content.replace("**", "").replace("__", "")  # Remove negrito
        md_content = md_content.replace("* ", "- ").replace("•", "-")  # Converte listas
        md_content = md_content.replace("# ", "").replace("## ", "").replace("### ", "")  # Remove cabeçalhos
        return md_content.strip()

    # Função para exportar para PDF com formatação melhorada
    def exportar_para_pdf():
        if not relatorio_texto:
            messagebox.showerror("Erro", "Nenhum relatório gerado!")
            return

        caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not caminho_arquivo:
            return

        try:
            c = canvas.Canvas(caminho_arquivo, pagesize=letter)
            largura_pagina, altura_pagina = letter
            margem_esquerda = 50
            margem_topo = altura_pagina - 50

            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(largura_pagina / 2, margem_topo, "Relatório de Desempenho")

            c.setFont("Helvetica", 12)
            texto_y = margem_topo - 30  # Ajuste do espaçamento inicial
            
            for linha in markdown_to_text(relatorio_texto).split("\n"):
                linhas_formatadas = wrap(linha, width=80)  # Quebra de linha automática
                for l in linhas_formatadas:
                    c.drawString(margem_esquerda, texto_y, l)
                    texto_y -= 15  # Espaçamento entre as linhas

                    if texto_y < 50:  # Verifica se precisa de nova página
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        texto_y = margem_topo

            c.save()
            messagebox.showinfo("Sucesso", f"PDF salvo em: {caminho_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar PDF: {e}")

    # Botão para gerar relatório
    botao_gerar = tk.Button(element_pai, text="Gerar Relatório", command=mostrar_relatorio)
    botao_gerar.pack(pady=10)

    # Área de exibição do relatório (sem tags HTML)
    text_widget = tk.Text(element_pai, wrap="word", height=15, width=70)
    text_widget.pack(pady=10)
    text_widget.config(state=tk.DISABLED)

    # Botão para exportar PDF
    botao_pdf = tk.Button(element_pai, text="Exportar para PDF", command=exportar_para_pdf)
    botao_pdf.pack(pady=10)

    element_pai.mainloop()
