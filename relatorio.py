import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import os
from groq import Groq

os.environ["GROQ_API_KEY"] = "sua_chave_aqui" #chave da api

GROQ_API_URL = "https://api.groq.com/v1/chat/completions"  # Verifique se esse é o endpoint correto

# Configuração do cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Função para gerar relatório com base nas notas
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
            model="llama-3.3-70b-versatile",  # Use o modelo correto
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content  # Retorna o texto gerado
    except Exception as e:
        return f"Erro ao gerar relatório: {e}"


def mostrar_relatorio():
    notas = [
        {"Matéria": "Matemática", "Período": "1", "n1": "10", "n2": "20", "n3": "12", "n4": "100"},
        {"Matéria": "Portugues", "Período": "6", "n1": "90", "n2": "89", "n3": "30", "n4": "100"}
    ]
    
    resultado = gerar_relatorio(notas)
    
    texto_relatorio.delete("1.0", tk.END)
    texto_relatorio.insert(tk.END, resultado)

# Criando a janela
janela = tk.Tk()
janela.title("Relatório de Desempenho")

# Criando o botão para gerar relatório
botao_gerar = tk.Button(janela, text="Gerar Relatório", command=mostrar_relatorio)
botao_gerar.pack(pady=10)

# Criando um campo de texto para exibir o relatório
texto_relatorio = scrolledtext.ScrolledText(janela, width=80, height=20)
texto_relatorio.pack(padx=10, pady=10)

janela.mainloop()
