from tkinter import Tk, Label
from PIL import Image, ImageTk

# Criar janela
root = Tk()

# Carregar imagem PNG com transparência
imagem = Image.open("resources/img/fundo_transp.png")  # Sua imagem PNG com transparência
fundo = (255, 255, 255)  # Cor de fundo desejada (branco)

# Criar um novo fundo branco e mesclar com a imagem original
imagem = imagem.convert("RGBA")  
nova_imagem = Image.new("RGBA", imagem.size, fundo + (255,))  # Fundo branco
nova_imagem.paste(imagem, (0, 0), imagem)  # Mesclar transparência

# Converter para formato suportado pelo Tkinter
imagem_tk = ImageTk.PhotoImage(nova_imagem)

# Exibir imagem
label = Label(root, image=imagem_tk)
label.pack()

root.mainloop()
