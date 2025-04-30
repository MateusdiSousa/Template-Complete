import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import functions.functions_relatory as fk

class RelatoryGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Relatórios")
        self.root.geometry("800x600")
        
        # Variáveis de controle
        self.template_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.selected_files = []
        self.selected_dirs = []
        
        # Criar interface
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Seção do template
        ttk.Label(main_frame, text="Template Markdown:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.template_path, width=50).grid(row=0, column=1, sticky=tk.EW)
        ttk.Button(main_frame, text="Procurar", command=self.browse_template).grid(row=0, column=2, padx=5)
        
        # Seção de saída
        ttk.Label(main_frame, text="Arquivo de Saída:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, sticky=tk.EW)
        ttk.Button(main_frame, text="Procurar", command=self.browse_output).grid(row=1, column=2, padx=5)
        
        # Notebook (abas)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, columnspan=3, pady=20, sticky=tk.NSEW)
        
        # Aba para diretórios
        dir_frame = ttk.Frame(notebook)
        self.create_dir_tab(dir_frame)
        notebook.add(dir_frame, text="Por Diretórios")
        
        # Aba para arquivos
        file_frame = ttk.Frame(notebook)
        self.create_file_tab(file_frame)
        notebook.add(file_frame, text="Por Arquivos")
        
        # Botão de gerar
        ttk.Button(main_frame, text="Gerar Relatório", command=self.generate_relatory).grid(row=3, column=0, columnspan=3, pady=20)
        
        # Configurar pesos das colunas
        main_frame.columnconfigure(1, weight=1)
        
    def create_dir_tab(self, parent):
        # Lista de diretórios
        self.dir_listbox = tk.Listbox(parent, height=10, selectmode=tk.MULTIPLE)
        self.dir_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.dir_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dir_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botões
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Adicionar Diretório", command=self.add_directory).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover Selecionados", command=self.remove_selected_dirs).pack(side=tk.LEFT, padx=5)
        
    def create_file_tab(self, parent):
        # Lista de arquivos
        self.file_listbox = tk.Listbox(parent, height=10, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botões
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Adicionar Arquivo", command=self.add_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover Selecionados", command=self.remove_selected_files).pack(side=tk.LEFT, padx=5)
        
    def browse_template(self):
        file_path = filedialog.askopenfilename(
            title="Selecione o template",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if file_path:
            self.template_path.set(file_path)
    
    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            title="Salvar relatório como",
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)
    
    def add_directory(self):
        dir_path = filedialog.askdirectory(title="Selecione um diretório com JSONs")
        if dir_path:
            self.selected_dirs.append(dir_path)
            self.dir_listbox.insert(tk.END, dir_path)
    
    def remove_selected_dirs(self):
        selected = self.dir_listbox.curselection()
        for index in reversed(selected):
            self.selected_dirs.pop(index)
            self.dir_listbox.delete(index)
    
    def add_file(self):
        file_paths = filedialog.askopenfilenames(
            title="Selecione arquivos JSON",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        for file_path in file_paths:
            self.selected_files.append(file_path)
            self.file_listbox.insert(tk.END, file_path)
    
    def remove_selected_files(self):
        selected = self.file_listbox.curselection()
        for index in reversed(selected):
            self.selected_files.pop(index)
            self.file_listbox.delete(index)
    
    def generate_relatory(self):
        if not self.template_path.get():
            messagebox.showerror("Erro", "Selecione um template primeiro!")
            return
            
        if not self.output_path.get():
            messagebox.showerror("Erro", "Selecione um arquivo de saída!")
            return
            
        try:
            # Método mais confiável para obter a aba ativa
            notebook = None
            for child in self.root.winfo_children():
                if isinstance(child, ttk.Frame):  # O frame principal contém o notebook
                    for subchild in child.winfo_children():
                        if isinstance(subchild, ttk.Notebook):
                            notebook = subchild
                            break
                    if notebook:
                        break
            
            if notebook is None:
                messagebox.showerror("Erro", "Não foi possível encontrar o notebook!")
                return
                
            current_tab = notebook.index(notebook.select())
            
            if current_tab == 0:  # Aba de diretórios
                if not self.selected_dirs:
                    messagebox.showerror("Erro", "Adicione pelo menos um diretório!")
                    return
                    
                fk.generate_relatory_by_many_dir(
                    self.template_path.get(),
                    self.selected_dirs,
                    self.output_path.get()
                )
            else:  # Aba de arquivos
                if not self.selected_files:
                    messagebox.showerror("Erro", "Adicione pelo menos um arquivo!")
                    return
                    
                fk.generate_relatory_by_many_json(
                    self.template_path.get(),
                    self.selected_files,
                    self.output_path.get()
                )
                
            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o relatório:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RelatoryGeneratorApp(root)
    root.mainloop()