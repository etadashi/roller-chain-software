import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from backend_chain_selector import calcular_resultados

# Configuração da classe App, com descrição dos frames
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software de Seleção de Correntes")
        self.geometry("900x400")
        self.dados = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (TelaInicial, EscolhaEntrada, EntradaObrigatoria1, EntradaObrigatoria2, EntradaOpcional1, EntradaOpcional2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(TelaInicial)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Configuração da Tela inicial  
class TelaInicial(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Bem-vindo ao Software de Seleção de Correntes", font=("Helvetica", 16)).pack(pady=20)
        explicacao = (
        "Este programa visa facilitar a seleção de correntes com base em dados de entrada.\n\n"
        "Ao clicar em \"Iniciar\", você será direcionado para a seleção de Dados Obrigatórios.\n"
        "Depois de adicionar seus dados de entrada obrigatórios, você será direcionado para uma aba de\n"
        "Dados Opcionais, onde é possível configurar um fator de sobrecarga específico com base na sua\n"
        "aplicação, uma distância estimada entre os centros das rodas dentadas e um tipo de corrente\n"
        "caso deseje.\n\n"
        "O programa realizará os cálculos com base nas variáveis de entrada e retornará os resultados\n"
        "para a corrente recomendada, além de outras correntes ANSI superiores. Também pode ser comparado\n"
        "o Coeficiente de Segurança para o projeto para diferentes combinações de correntes (simples, dupla, tripla)."
        )
        
        tk.Label(self,text=explicacao,wraplength=700,justify="center",font=("Helvetica", 11)).pack(pady=(0, 30))
        tk.Button(self, text="Iniciar", command=lambda: controller.show_frame(EscolhaEntrada)).pack()

# Configuração da Tela de escolha das variáveis 
class EscolhaEntrada(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Escolha o tipo de entrada de dados obrigatórios:", font=("Helvetica", 14)).pack(pady=20)
        tk.Button(self, text="1 - Rotações n1 e n2, Potência nominal", width=50, command=lambda: controller.show_frame(EntradaObrigatoria1)).pack(pady=10)
        tk.Button(self, text="2 - Rotação n1, Nº de dentes z1 e z2, Potência nominal", width=50, command=lambda: controller.show_frame(EntradaObrigatoria2)).pack()
        tk.Button(self, text="Voltar", command=lambda: controller.show_frame(TelaInicial)).pack(pady=30)

# Configuração da Tela de entradas obrigatórias 1 Rotações n1 e n2, Potência nominal
class EntradaObrigatoria1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame_esquerda = tk.Frame(self)
        frame_esquerda.pack(side="left", padx=20, pady=20, anchor="n")

        labels = ["n1 (rpm):", "n2 (rpm):", "Potência nominal (N0):", "Unidade de potência:"]
        self.entries = []

        # Configuração dos campos de coleta de variáveis
        for i, texto in enumerate(labels):
            tk.Label(frame_esquerda, text=texto).grid(row=i, column=0, sticky="w", pady=5)
            if "Unidade" in texto:
                self.unidade_var = tk.StringVar()
                unidade_box = ttk.Combobox(frame_esquerda, textvariable=self.unidade_var, values=("CV", "hp", "kW"))
                unidade_box.grid(row=i, column=1, pady=5, padx=5)
                self.entries.append(unidade_box)
            else:
                entry = tk.Entry(frame_esquerda)
                entry.grid(row=i, column=1, pady=5, padx=5)
                self.entries.append(entry)

        # Coleta das variáveis carregadas 
        self.n1_entry, self.n2_entry, self.n0_entry, _ = self.entries

        tk.Button(frame_esquerda, text="Continuar para variáveis opcionais", command=self.validar_campos).grid(row=len(labels), columnspan=2, pady=15)
        tk.Button(frame_esquerda, text="Voltar", command=lambda: controller.show_frame(EscolhaEntrada)).grid(row=len(labels)+1, columnspan=2)

        # Configuração imagem suporte
        frame_direita = tk.Frame(self)
        frame_direita.pack(side="left", padx=10, pady=20, anchor="n")
        try:
            imagem = Image.open("Imagem_Dados_Entrada.png")
            imagem = imagem.resize((400, 200))
            self.imagem_tk = ImageTk.PhotoImage(imagem)
            tk.Label(frame_direita, image=self.imagem_tk).pack()
        except Exception:
            tk.Label(frame_direita, text="(Imagem não carregada)").pack()

    # Verificação da coleta das variáveis obrigatórias
    def validar_campos(self):
        try:
            n1 = float(self.n1_entry.get())
            n2 = float(self.n2_entry.get())
            n0 = float(self.n0_entry.get())
            unidade = self.unidade_var.get()

            if not unidade:
                raise ValueError("Unidade de potência não selecionada.")

            self.controller.dados = {"n1": n1, "n2": n2, "N0": n0, "unidade": unidade}
            self.controller.show_frame(EntradaOpcional1)
        except Exception as e:
            messagebox.showerror("Erro de entrada", "Entre com todas as variáveis obrigatórias e revise se não foram adicionados valores decimais com ','. Os decimais devem ser representados com '.'.")

# Configuração da Tela de escolha das variáveis opcionais
class EntradaOpcional1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Entradas Opcionais", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Seleção do Tipo de choque
        tk.Label(self, text="Tipo de choque do sistema: Fator de serviço").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.tipo_choque = ttk.Combobox(self, width=60, justify='right')
        self.tipo_choque['values'] = [
            "",
            "Constante para motor elétrico/turbina: 1.0",
            "Constante para acionamento hidráulico: 1.0",
            "Constante para acionamento mecânico: 1.2",
            "Moderado ou meio impulsivo para motor elétrico/turbina: 1.3",
            "Moderado ou meio impulsivo para acionamento hidráulico: 1.4",
            "Moderado ou meio impulsivo para acionamento mecânico: 1.4",
            "Pesado ou bastante abrasivo para motor elétrico/turbina: 1.5",
            "Pesado ou bastante abrasivo para acionamento hidráulico: 1.4",
            "Pesado ou bastante abrasivo para acionamento mecânico: 1.7"
        ]
        self.tipo_choque.grid(row=1, column=1, padx=5, pady=5)

        # Entrada manual do número de dentes da roda dentada motora (z1)
        tk.Label(self, text="z1 (nº de dentes da roda motora)").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.z1_entry = tk.Entry(self, width=15)
        self.z1_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Entrada manual da distância entre centros das rodas dentadas (a)
        tk.Label(self, text="a (distância entre centros) em mm").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.a_entry = tk.Entry(self, width=15)
        self.a_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Entrada manual do Tipo de corrente
        tk.Label(self, text="Tipo de Corrente ANSI").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.tipo_corrente = ttk.Combobox(self, width=15)
        self.tipo_corrente['values'] = ["", "25", "35", "40", "50", "60", "80", "100", "120", "140", "160", "180", "200", "240"]
        self.tipo_corrente.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=20)

        tk.Button(frame_botoes, text="Calcular", command=self.pegar_dados).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Voltar", command=lambda: controller.show_frame(EntradaObrigatoria1)).pack(side="left", padx=10)

    # Conexão com o código Backend
    def pegar_dados(self):
        try:
            dados = self.controller.dados.copy()
            if self.tipo_choque.get():
                dados["Tipo_choque"] = self.tipo_choque.get()
            if self.z1_entry.get():
                dados["z1"] = int(self.z1_entry.get())
            if self.a_entry.get():
                dados["a"] = float(self.a_entry.get())
            if self.tipo_corrente.get():
                dados["Tipo_corrente"] = self.tipo_corrente.get()
            print(dados)
            resultados = calcular_resultados(dados)
            self.exibir_resultados(resultados)
        except Exception as e:
            messagebox.showerror("Erro ao calcular", "Ops, algo deu errado nos cálculos, revisar se não foi adicionado um valor com ','. Os decimais devem ser representados com '.'")

    # Retorna os cálculos do Backend e cria uma janela de exibição dos resultados
    def exibir_resultados(self, resultados):
        janela_resultados = tk.Toplevel(self)
        janela_resultados.title("Resultados Comparativos")
        janela_resultados.geometry("1700x500")

        num_correntes = len(resultados)
        titulo = f"Comparação entre {num_correntes} corrente(s)" if num_correntes > 1 else "Resultados"

        tk.Label(janela_resultados, text=titulo, font=("Arial", 16, "bold")).pack(pady=10)

        frame_container = tk.Frame(janela_resultados)
        frame_container.pack(fill="both", expand=True, padx=10, pady=10)

        for nome_corrente, dados in resultados.items():
            frame = tk.Frame(frame_container, bd=2, relief="groove")
            frame.pack(side="left", expand=True, fill="both", padx=10)

            tk.Label(frame, text=nome_corrente, font=("Arial", 14, "bold")).pack(pady=5)

            for k, v in dados.items():
                valor = round(v, 3) if isinstance(v, float) else v
                tk.Label(frame, text=f"{k}: {valor}", anchor="w", justify="left").pack(fill="x")

# Configuração da Tela de entradas obrigatórias 2 Rotação n1, números de dentes das rodas z1 e z2, Potência nominal
class EntradaObrigatoria2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame_esquerda = tk.Frame(self)
        frame_esquerda.pack(side="left", padx=20, pady=20, anchor="n")

        labels = ["n1 (rpm):", "z1 (nº de dentes roda motora):", "z2 (nº de dentes roda movida):", "Potência nominal (N0):", "Unidade de potência:"]
        self.entries = []

        # Configuração dos campos de coleta de variáveis
        for i, texto in enumerate(labels):
            tk.Label(frame_esquerda, text=texto).grid(row=i, column=0, sticky="w", pady=5)
            if "Unidade" in texto:
                self.unidade_var = tk.StringVar()
                unidade_box = ttk.Combobox(frame_esquerda, textvariable=self.unidade_var, values=("CV", "hp", "kW"))
                unidade_box.grid(row=i, column=1, pady=5, padx=5)
                self.entries.append(unidade_box)
            else:
                entry = tk.Entry(frame_esquerda)
                entry.grid(row=i, column=1, pady=5, padx=5)
                self.entries.append(entry)

        # Coleta das variáveis carregadas
        self.n1_entry, self.z1_entry, self.z2_entry, self.n0_entry, _ = self.entries

        tk.Button(frame_esquerda, text="Continuar para variáveis opcionais", command=self.validar_campos).grid(row=len(labels), columnspan=2, pady=15)
        tk.Button(frame_esquerda, text="Voltar", command=lambda: controller.show_frame(EscolhaEntrada)).grid(row=len(labels)+1, columnspan=2)

        frame_direita = tk.Frame(self)
        frame_direita.pack(side="left", padx=10, pady=20, anchor="n")
        try:
            imagem = Image.open("Imagem_Dados_Entrada_2.png")
            imagem = imagem.resize((400, 200))
            self.imagem_tk = ImageTk.PhotoImage(imagem)
            tk.Label(frame_direita, image=self.imagem_tk).pack()
        except Exception:
            tk.Label(frame_direita, text="(Imagem não carregada)").pack()

    # Verificação da coleta das variáveis obrigatórias
    def validar_campos(self):
        try:
            n1 = float(self.n1_entry.get())
            z1 = int(self.z1_entry.get())
            z2 = int(self.z2_entry.get())
            n0 = float(self.n0_entry.get())
            unidade = self.unidade_var.get()

            if not unidade:
                raise ValueError("Unidade de potência não selecionada.")

            n2 = n1 * z1 / z2
            self.controller.dados = {"n1": n1, "z1": z1, "z2": z2, "n2": n2, "N0": n0, "unidade": unidade}
            self.controller.show_frame(EntradaOpcional2)
        except Exception as e:
            messagebox.showerror("Erro de entrada", "Entre com todas as variáveis obrigatórias e revise se não foram adicionados valores decimais com ','. Os decimais devem ser representados com '.'.")

# Configuração da Tela de escolha das variáveis opcionais
class EntradaOpcional2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Entradas Opcionais", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Seleção do Tipo de choque
        tk.Label(self, text="Tipo de choque do sistema: Fator de serviço").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.tipo_choque = ttk.Combobox(self, width=60, justify='right')
        self.tipo_choque['values'] = [
            "",
            "Constante para motor elétrico/turbina: 1.0",
            "Constante para acionamento hidráulico: 1.0",
            "Constante para acionamento mecânico: 1.2",
            "Moderado ou meio impulsivo para motor elétrico/turbina: 1.3",
            "Moderado ou meio impulsivo para acionamento hidráulico: 1.4",
            "Moderado ou meio impulsivo para acionamento mecânico: 1.4",
            "Pesado ou bastante abrasivo para motor elétrico/turbina: 1.5",
            "Pesado ou bastante abrasivo para acionamento hidráulico: 1.4",
            "Pesado ou bastante abrasivo para acionamento mecânico: 1.7"
        ]
        self.tipo_choque.grid(row=1, column=1, padx=5, pady=5)

        # Entrada manual da distância entre centros das rodas dentadas (a)
        tk.Label(self, text="a (distância entre centros) em mm").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.a_entry = tk.Entry(self, width=15)
        self.a_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Entrada manual do Tipo de corrente
        tk.Label(self, text="Tipo de Corrente ANSI").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.tipo_corrente = ttk.Combobox(self, width=15)
        self.tipo_corrente['values'] = ["", "25", "35", "40", "50", "60", "80", "100", "120", "140", "160", "180", "200", "240"]
        self.tipo_corrente.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=20)

        tk.Button(frame_botoes, text="Calcular", command=self.pegar_dados).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Voltar", command=lambda: controller.show_frame(EntradaObrigatoria2)).pack(side="left", padx=10)

    # Conexão com o código Backend
    def pegar_dados(self):
        try:
            # Copia os dados obrigatórios e adiciona os opcionais
            dados = self.controller.dados.copy()
            if self.tipo_choque.get():
                dados["Tipo_choque"] = self.tipo_choque.get()
            if self.a_entry.get():
                dados["a"] = float(self.a_entry.get())
            if self.tipo_corrente.get():
                dados["Tipo_corrente"] = self.tipo_corrente.get()
            print(dados)
            resultados = calcular_resultados(dados)
            self.exibir_resultados(resultados)

        except Exception as e:
            messagebox.showerror("Erro ao calcular", "Ops, algo deu errado nos cálculos, revisar se não foi adicionado um valor com ','. Os decimais devem ser representados com '.'")

    # Retorna os cálculos do Backend e cria uma janela de exibição dos resultados
    def exibir_resultados(self, resultados):

        janela_resultados = tk.Toplevel(self)
        janela_resultados.title("Resultados Comparativos")
        janela_resultados.geometry("1700x500")

        num_correntes = len(resultados)
        titulo = "Resultados"
        if num_correntes == 2:
            titulo = "Comparação entre duas correntes"
        elif num_correntes == 3:
            titulo = "Comparação entre três correntes"
        elif num_correntes == 4:
            titulo = "Comparação entre quatro correntes"
        elif num_correntes == 5:
            titulo = "Comparação entre cinco correntes"

        tk.Label(janela_resultados, text=titulo, font=("Arial", 16, "bold")).pack(pady=10)

        frame_container = tk.Frame(janela_resultados)
        frame_container.pack(fill="both", expand=True, padx=10, pady=10)

        for nome_corrente, dados in resultados.items():
            frame = tk.Frame(frame_container, bd=2, relief="groove")
            frame.pack(side="left", expand=True, fill="both", padx=10)

            tk.Label(frame, text=nome_corrente, font=("Arial", 14, "bold")).pack(pady=5)

            for k, v in dados.items():
                valor = round(v, 3) if isinstance(v, float) else v
                tk.Label(frame, text=f"{k}: {valor}", anchor="w", justify="left").pack(fill="x")

if __name__ == "__main__":
    app = App()
    app.mainloop()
