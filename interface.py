import tkinter as tk
from tkinter import ttk, messagebox
from database import Database


class Interface:

    def __init__(self, janela):
        self.janela = janela
        self.db = Database()
        self.id_cliente = None

        self.janela.title("Sistema de Cadastro de Clientes")
        largura = 900
        altura = 650
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

        self.criar_componentes()
        self.carregar_clientes()

    # ==========================
    # LIMPAR CAMPOS
    # ==========================
    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.id_cliente = None

    # ==========================
    # SALVAR CLIENTE
    # ==========================
    def salvar_cliente(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not nome or not cpf or not telefone or not email:
            messagebox.showerror(
                "Campos obrigatórios",
                "Por favor, preencha todos os campos."
            )
            return

        self.db.inserir_cliente(nome, cpf, telefone, email)

        self.limpar_campos()
        self.carregar_clientes()

        messagebox.showinfo(
            "Sucesso",
            "Cliente salvo com sucesso!"
        )

    # ==========================
    # CARREGAR CLIENTES
    # ==========================
    def carregar_clientes(self):
        clientes = self.db.listar_clientes()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for cliente in clientes:
            self.tabela.insert("", tk.END, values=cliente)
        self.label_total.config(
            text=f"Total de clientes: {len(clientes)}"
        )

    def pesquisar_clientes(self):
        texto = self.entry_pesquisa.get().strip()
        if texto == "":
            self.carregar_clientes()
            return
        clientes = self.db.pesquisar_clientes(texto)
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for cliente in clientes:
            self.tabela.insert("", tk.END, values=cliente)
        self.label_total.config(
            text=f"Total de clientes: {len(clientes)}"
        )

    # ==========================
    # SELECIONAR CLIENTE
    # ==========================
    def selecionar_clientes(self, event):
        selecionado = self.tabela.focus()

        if not selecionado:
            return

        valores = self.tabela.item(selecionado, "values")

        self.limpar_campos()

        self.entry_nome.insert(0, valores[1])
        self.entry_cpf.insert(0, valores[2])
        self.entry_telefone.insert(0, valores[3])
        self.entry_email.insert(0, valores[4])

        self.id_cliente = valores[0]

    # ==========================
    # EDITAR (A FAZER)
    # ==========================
    def editar_clientes(self):
        if self.id_cliente is None:
            messagebox.showerror(
                "Aviso",
                "Selecione um cliente para editar."
            )
            return
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        if not nome or not cpf or not telefone or not email:
            messagebox.showerror(
                "Campos obrigatórios",
                "Por favor, preencha todos os campos."
            )
            return
        self.db.atualizar_cliente(self.id_cliente, nome, cpf, telefone, email)
        self.carregar_clientes()
        self.limpar_campos()
        messagebox.showinfo(
            "Sucesso",
            "Cliente atualizado com sucesso!"
        )

    def excluir_cliente(self,):
            if self.id_cliente is None:
                messagebox.showerror(
                    "Aviso",
                    "Selecione um cliente para excluir."
                )
                return
            resposta = messagebox.askyesno(
                "Confirmação",
                "Tem certeza que deseja excluir este cliente?"
            )
            if resposta:
                self.db.excluir_cliente(self.id_cliente)
                self.carregar_clientes()
                self.limpar_campos()
                messagebox.showinfo(
                    "Sucesso",
                    "Cliente excluído com sucesso!"
                )

    def exportar_para_excel(self):
        self.db.exportar_para_excel(self.db.listar_clientes())
        messagebox.showinfo(
            "Sucesso",
            "Arquivo clientes.xlsx exportado com sucesso!"
        )
    
        

    # ==========================
    # INTERFACE
    # ==========================
    def criar_componentes(self):
        menu_bar = tk.Menu(self.janela)
        menu_arquivo = tk.Menu(menu_bar, tearoff=0)
        menu_arquivo.add_command(label="Novo Cadastro", command=self.limpar_campos)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.janela.quit)
        menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_ajuda = tk.Menu(menu_bar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=lambda: messagebox.showinfo(
            "Sobre",
            "Sistema de Cadastro de Clientes\nVersão 1.0\nDesenvolvido por Pedro Henrique"
        ))
        menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
        self.janela.config(menu=menu_bar)

        frame_pesquisa = tk.Frame(self.janela)
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure(
                "Treeview",
                rowheight=28,
                font=("Segoe UI", 10, "bold")
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")

            )
        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )
        frame_pesquisa.pack(pady=10)
        tk.Label(
            frame_pesquisa,
            text="Pesquisar:",    
        ).pack(side="left", padx=5)

        self.entry_pesquisa = tk.Entry(frame_pesquisa, width=30)
        self.entry_pesquisa.pack(side="left", padx=5)
        self.entry_pesquisa.bind(
            "<KeyRelease>",
            lambda event: self.pesquisar_clientes()   
        )
        btn_pesquisar = tk.Button(
            frame_pesquisa,
            text="Pesquisar",
            command=self.pesquisar_clientes
        )
        btn_pesquisar.pack(side="left", padx=5)

        frame_formulario = tk.Frame(self.janela)
        frame_formulario.pack(pady=20)

        titulo = tk.Label(
            frame_formulario,
            text="Sistema de Cadastro de Clientes",
            font=("Segoe UI", 20, "bold"),
            fg="#1E3A8A"
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(frame_formulario, text="Nome:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5
        )

        self.entry_nome = tk.Entry(frame_formulario, width=40)
        self.entry_nome.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_formulario, text="CPF:").grid(
            row=2, column=0, sticky="w", padx=10, pady=5
        )

        self.entry_cpf = tk.Entry(frame_formulario, width=40)
        self.entry_cpf.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_formulario, text="Telefone:").grid(
            row=3, column=0, sticky="w", padx=10, pady=5
        )

        self.entry_telefone = tk.Entry(frame_formulario, width=40)
        self.entry_telefone.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame_formulario, text="Email:").grid(
            row=4, column=0, sticky="w", padx=10, pady=5
        )

        self.entry_email = tk.Entry(frame_formulario, width=40)
        self.entry_email.grid(row=4, column=1, padx=10, pady=5)

        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=20)

        ttk.Button(
            frame_botoes,
            text="Salvar",
            width=12,
            command=self.salvar_cliente
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            frame_botoes,
            text="Limpar",
            width=12,
            command=self.limpar_campos
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            frame_botoes,
            text="Editar",
            width=12,
            command=self.editar_clientes
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            frame_botoes,
            text="Excluir",
            width=12,
            command=self.excluir_cliente
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            frame_botoes,
            text="Exportar para Excel",
            width=18,
            command=self.exportar_para_excel
        ).grid(row=0, column=4, padx=5)

        frame_tabela = tk.Frame(self.janela)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=("ID", "Nome", "CPF", "Telefone", "Email"),
            show="headings"
        )

        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Email", text="Email")

        self.tabela.column("ID", width=50)
        self.tabela.column("Nome", width=180)
        self.tabela.column("CPF", width=120)
        self.tabela.column("Telefone", width=120)
        self.tabela.column("Email", width=220)

        scrollbar = ttk.Scrollbar(
            frame_tabela,
            orient="vertical",
            command=self.tabela.yview
        )
        self.tabela.configure(yscroll=scrollbar.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.label_total = tk.Label(
            self.janela,
            text="Total de clientes: 0",
            font=("Arial", 10, "bold")
        )
        self.label_total.pack(pady=5)

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_clientes
        )
        self.entry_nome.focus_set()