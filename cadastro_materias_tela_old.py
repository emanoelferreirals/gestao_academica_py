import tkinter as tk
from tkinter import ttk
from funcs_old import salvar_materia
from PIL import Image, ImageTk  # Para exibir imagens

class CadastroMaterias:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Matérias")
        self.root.geometry("600x400")
        
        # Configurando a imagem de fundo
        self.bg_image = Image.open("resources/img/fundo.png")
        self.bg_image = self.bg_image.resize((600, 400))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(relwidth=1, relheight=1)
        
        # Frame principal
        frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=250)
        
        # Campos do formulário
        tk.Label(frame, text="Nome da Matéria:", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nome = tk.Entry(frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(frame, text="Descrição:", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_descricao = tk.Entry(frame, width=30)
        self.entry_descricao.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(frame, text="Conteúdos:", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_conteudos = tk.Entry(frame, width=30)
        self.entry_conteudos.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(frame, text="Períodos:", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_periodos = tk.Entry(frame, width=5)
        self.entry_periodos.grid(row=3, column=1, padx=10, pady=5)
        
        # Botão de salvar
        btn_salvar = ttk.Button(frame, text="Salvar", command=self.salvar)
        btn_salvar.grid(row=4, columnspan=2, pady=10)
    
    def salvar(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        conteudos = self.entry_conteudos.get().split(",")  # Lista separada por vírgula
        periodos = self.entry_periodos.get()
        
        if nome and descricao and conteudos and periodos:
            salvar_materia(nome, descricao, conteudos, periodos)
            tk.messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
        else:
            tk.messagebox.showerror("Erro", "Preencha todos os campos!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroMaterias(root)
    root.mainloop()
