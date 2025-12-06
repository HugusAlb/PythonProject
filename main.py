import os
import sys
import uuid
import gspread
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from oauth2client.service_account import ServiceAccountCredentials

class SistemaEscolar:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Santa Ursula")
        self.root.geometry("850x600")
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(base_path, "logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass 

        try:
            self.conectar_banco()
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha ao conectar: {e}")
            self.root.destroy()
            return

        self.setup_ui()
        self.listar_alunos()

    def conectar_banco(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        
        base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "credenciais.json")
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        ss = client.open("Banco-Alunos")
        self.sheet_alunos = ss.sheet1
        self.sheet_logs = ss.worksheet("Logs")

    def setup_ui(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        
        p_top = tk.Frame(self.root, pady=10)
        p_top.pack(fill="x", padx=10)

        tk.Label(p_top, text="Nome:").pack(side="left")
        self.e_nome = tk.Entry(p_top, width=25)
        self.e_nome.pack(side="left", padx=5)

        tk.Label(p_top, text="Idade:").pack(side="left")
        self.e_idade = tk.Entry(p_top, width=5)
        self.e_idade.pack(side="left", padx=5)

        tk.Label(p_top, text="Nota:").pack(side="left")
        self.e_nota = tk.Entry(p_top, width=5)
        self.e_nota.pack(side="left", padx=5)

        tk.Button(p_top, text="Cadastrar", command=self.cadastrar, bg="#4CAF50", fg="white").pack(side="left", padx=10)

        p_mid = tk.Frame(self.root, pady=5)
        p_mid.pack(fill="x", padx=10)

        tk.Button(p_mid, text="Recarregar", command=self.listar_alunos).pack(side="left")
        tk.Button(p_mid, text="Excluir", command=self.remover, bg="#f44336", fg="white").pack(side="left", padx=5)
        tk.Button(p_mid, text="Média da turma", command=self.media).pack(side="left", padx=5)
        
        self.e_busca = tk.Entry(p_mid, width=20)
        self.e_busca.pack(side="right", padx=5)
        tk.Button(p_mid, text="Buscar", command=self.buscar).pack(side="right")

        cols = ("ID", "Nome", "Idade", "Nota")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        
        self.tree.column("ID", width=220, minwidth=220)
        self.tree.column("Nome", width=200)
        self.tree.column("Idade", width=50)
        self.tree.column("Nota", width=50)

        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scroll.pack(side="right", fill="y", pady=10)

    def log(self, acao, obs=""):
        try:
            self.sheet_logs.append_row([datetime.now().strftime('%d/%m/%Y %H:%M:%S'), acao, obs])
        except: pass

    def cadastrar(self):
        n, i, nt = self.e_nome.get().lower(), self.e_idade.get(), self.e_nota.get()
        if not n or not i or not nt: return
        try:
            uid = str(uuid.uuid4())
            self.sheet_alunos.append_row([uid, n, int(i), float(nt.replace(',', '.'))])
            self.log("CADASTRO", f"{n} ({uid})")
            self.e_nome.delete(0, 'end'); self.e_idade.delete(0, 'end'); self.e_nota.delete(0, 'end')
            self.listar_alunos()
            messagebox.showinfo("OK", "Salvo!")
        except ValueError: messagebox.showerror("Erro", "Dados inválidos.")

    def listar_alunos(self):
        [self.tree.delete(x) for x in self.tree.get_children()]
        try:
            for r in self.sheet_alunos.get_all_records():
                self.tree.insert("", "end", values=(r.get("ID"), r.get("Nome"), r.get("Idade"), r.get("Nota")))
        except: pass

    def remover(self):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])['values']
        if messagebox.askyesno("Confirmar", f"Excluir {vals[1]}?"):
            try:
                cell = self.sheet_alunos.find(vals[0])
                self.sheet_alunos.delete_rows(cell.row)
                self.log("REMOÇÃO", f"{vals[1]} ({vals[0]})")
                self.listar_alunos()
            except: messagebox.showerror("Erro", "Não encontrado.")

    def buscar(self):
        term = self.e_busca.get().lower()
        if not term: return self.listar_alunos()
        rows = [self.tree.item(i)['values'] for i in self.tree.get_children()]
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=r) for r in rows if term in str(r[1]).lower()]

    def media(self):
        recs = self.sheet_alunos.get_all_records()
        notas = [float(str(r.get("Nota",0)).replace(',','.')) for r in recs if r.get("Nota")]
        if notas:
            m = sum(notas)/len(notas)
            self.log("CONSULTA", f"Média: {m:.2f}")
            messagebox.showinfo("Média", f"{m:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEscolar(root)
    root.mainloop()