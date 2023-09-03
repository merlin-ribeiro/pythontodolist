import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def view_tasks(self):
        return self.tasks

    def update_task(self, task_index, new_description, new_status):
        if 1 <= task_index <= len(self.tasks):
            self.tasks[task_index - 1]['description'] = new_description
            self.tasks[task_index - 1]['completed'] = new_status
            return True
        else:
            return False

    def complete_task(self, task_index, new_status):
        if 1 <= task_index <= len(self.tasks):
            self.tasks[task_index - 1]['completed'] = new_status
            return True
        else:
            return False

    def remove_task(self, task_index):
        if 1 <= task_index <= len(self.tasks):
            del self.tasks[task_index - 1]
            return True
        else:
            return False

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.tasks, file)

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                self.tasks = json.load(file)

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.todo_list = ToDoList()
        self.filename = "tasks.json"
        self.load_tasks()

        self.create_widgets()

    def load_tasks(self):
        self.todo_list.load_from_file(self.filename)

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Gerenciador de Tarefas", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.refresh_listbox()

        self.add_button = tk.Button(self.root, text="Adicionar Tarefa", command=self.add_task)
        self.add_button.pack(padx=20, pady=5, fill=tk.X)

        self.update_button = tk.Button(self.root, text="Atualizar Tarefa", command=self.update_task)
        self.update_button.pack(padx=20, pady=5, fill=tk.X)

        self.update_button = tk.Button(self.root, text="Completar Tarefa", command=self.complete_task)
        self.update_button.pack(padx=20, pady=5, fill=tk.X)

        self.remove_button = tk.Button(self.root, text="Remover Tarefa", command=self.remove_task)
        self.remove_button.pack(padx=20, pady=5, fill=tk.X)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, task in enumerate(self.todo_list.view_tasks(), start=1):
            status = "Concluída" if task["completed"] else "Pendente"
            self.listbox.insert(tk.END, f"{idx}. {task['description']} - {status}")

    def add_task(self):
        description = tk.simpledialog.askstring("Adicionar Tarefa", "Digite a descrição da tarefa:")
        if description:
            completed = False
            task = {"description": description, "completed": completed}
            self.todo_list.add_task(task)
            self.todo_list.save_to_file(self.filename)
            self.refresh_listbox()

    def update_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0] + 1  # Adjust for 0-based index
            task = self.todo_list.view_tasks()[selected_index - 1]
            new_description = tk.simpledialog.askstring("Atualizar Tarefa", "Digite a nova descrição da tarefa:", initialvalue=task["description"])
            if new_description:
                new_status = tk.messagebox.askyesno("Tarefa Concluída?", "A tarefa está concluída?", initial=task["completed"])
                if self.todo_list.update_task(selected_index, new_description, new_status):
                    self.todo_list.save_to_file(self.filename)
                    self.refresh_listbox()
                else:
                    tk.messagebox.showerror("Erro", "Índice de tarefa inválido.")
        else:
            tk.messagebox.showinfo("Informação", "Selecione uma tarefa para atualizar.")

    def complete_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0] + 1  # Adjust for 0-based index
            new_status = True
            if self.todo_list.complete_task(selected_index, new_status):
                self.todo_list.save_to_file(self.filename)
                self.refresh_listbox()
            else:
                    tk.messagebox.showerror("Erro", "Índice de tarefa inválido.")
        else:
            tk.messagebox.showinfo("Informação", "Selecione uma tarefa para atualizar.")


    def remove_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0] + 1  # Adjust for 0-based index
            if self.todo_list.remove_task(selected_index):
                self.todo_list.save_to_file(self.filename)
                self.refresh_listbox()
            else:
                tk.messagebox.showerror("Erro", "Índice de tarefa inválido.")
        else:
            tk.messagebox.showinfo("Informação", "Selecione uma tarefa para remover.")

def main():
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
