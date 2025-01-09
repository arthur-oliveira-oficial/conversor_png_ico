import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ConversorPNGICO:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor PNG para ICO")
        self.root.geometry("400x200")
        
        # Criando os elementos da interface
        self.label = tk.Label(root, text="Selecione uma imagem PNG para converter:", pady=10)
        self.label.pack()
        
        self.btn_selecionar = tk.Button(root, text="Selecionar PNG", command=self.selecionar_arquivo)
        self.btn_selecionar.pack(pady=10)
        
        self.arquivo_selecionado = tk.StringVar()
        self.label_arquivo = tk.Label(root, textvariable=self.arquivo_selecionado)
        self.label_arquivo.pack(pady=10)
        
        self.btn_converter = tk.Button(root, text="Converter para ICO", command=self.converter)
        self.btn_converter.pack(pady=10)
        
        self.arquivo_png = None

    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png")]
        )
        if arquivo:
            self.arquivo_png = arquivo
            self.arquivo_selecionado.set(os.path.basename(arquivo))

    def converter(self):
        if not self.arquivo_png:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo PNG primeiro!")
            return
            
        try:
            # Abre a imagem PNG
            imagem = Image.open(self.arquivo_png)
            
            # Converte para RGBA para manter transparência
            if imagem.mode != 'RGBA':
                imagem = imagem.convert('RGBA')
            
            # Calcula as dimensões mantendo a proporção
            largura, altura = imagem.size
            nova_largura = 128
            nova_altura = int((altura * nova_largura) / largura)
            
            if nova_altura > 128:
                nova_altura = 128
                nova_largura = int((largura * nova_altura) / altura)
            
            # Cria nova imagem com fundo transparente
            nova_imagem = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
            
            # Redimensiona a imagem original
            imagem_redimensionada = imagem.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
            
            # Calcula posição central
            x = (128 - nova_largura) // 2
            y = (128 - nova_altura) // 2
            
            # Cola a imagem redimensionada no centro
            nova_imagem.paste(imagem_redimensionada, (x, y), imagem_redimensionada)
            
            # Define o caminho de saída
            saida = os.path.splitext(self.arquivo_png)[0] + '.ico'
            
            # Salva como ICO
            nova_imagem.save(saida, format='ICO', sizes=[(128, 128)])
            
            messagebox.showinfo("Sucesso", "Arquivo convertido com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter arquivo: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorPNGICO(root)
    root.mainloop()