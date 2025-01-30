#importa tkinter e facilita a chamada de seus elementos
import tkinter as tk

#Importa os widgets estilizados do Tkinter
import tkinter.ttk as ttk

#Importa o ttkbootstrap
import ttkbootstrap as tb

#importando pillow
from PIL import Image,ImageTk

#Importa o ttkbootstrap para melhorar o design do app
# import ttkbootstrap as tb

#criando janela principal
root = tk.Tk()
root.title("Login SODGA")
root.geometry("500x300")
root.resizable(False,False) # Impede redimensionamento

#Imagem para plano de fundo
fundo = Image.open("resources/img/wallpaper.png")
fundo = fundo.resize((500,300)) #Ajusta o tamanho da imagem para a janela.
fundo = ImageTk.PhotoImage(fundo) #Converte a imagem para um formato compatível com o Tkinter.

lbl_fundo = tk.Label(root,image=fundo) #Cria um rótulo exibindo a imagem
lbl_fundo.place(x=0,y=0,relwidth=1,relheight=1) #Faz com que a imagem ocupe toda a tela

#Criando frame para organizar os elementos
frame = ttk.Frame(root,padding=30)
frame.pack(expand=True)

#Entrada do usuário
lbl_user = ttk.Label(frame,text="Usuário: ")
lbl_user.grid(row=0,column=0,sticky="w",pady=5)
entry_user = ttk.Entry(frame,width=25)
entry_user.grid(row=0,column=1)

lbl_pass = ttk.Label(frame,text="Senha: ")
lbl_pass.grid(row=1,column=0,sticky="w",pady=5)
entry_pass = ttk.Entry(frame,width=25,show="*")
entry_pass.grid(row=1,column=1)

#criando os botões
btn_login = ttk.Button(frame,text="Login").grid(row=3,column=0,columnspan=2,pady=10)
btn_cadastro = ttk.Button(frame,text="Criar Conta").grid(row=4,column=0,columnspan=2,pady=10)

root.mainloop() # Impede o fechamento da janela 
