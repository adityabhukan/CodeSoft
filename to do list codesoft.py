import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x400")
        
        self.filename = "todo_gui.json"
        self.tasks = self.load_tasks()
        
        self.setup_ui()
        self.update_task_list()
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []
    
    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)
    
    def setup_ui(self):
        # Task Entry Frame
        entry_frame = ttk.Frame(self.root, padding="10")
        entry_frame.pack(fill=tk.X)
        
        ttk.Label(entry_frame, text="New Task:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(entry_frame, width=40)
        self.task_entry.grid(row=0, column=1, sticky=tk.EW)
        
        ttk.Label(entry_frame, text="Priority:").grid(row=1, column=0, sticky=tk.W)
        self.priority_var = tk.StringVar(value="medium")
        ttk.Combobox(entry_frame, textvariable=self.priority_var, 
                    values=["high", "medium", "low"], width=10).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(entry_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W)
        self.due_date_entry = ttk.Entry(entry_frame, width=15)
        self.due_date_entry.grid(row=2, column=1, sticky=tk.W)
        
        add_button = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=3, column=1, sticky=tk.E)
        
        # Task List Frame
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "description", "priority", "due_date", "completed")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.task_tree.heading("id", text="ID")
        self.task_tree.heading("description", text="Description")
        self.task_tree.heading("priority", text="Priority")
        self.task_tree.heading("due_date", text="Due Date")
        self.task_tree.heading("completed", text="Completed")
        
        self.task_tree.column("id", width=30, anchor=tk.CENTER)
        self.task_tree.column("description", width=200)
        self.task_tree.column("priority", width=80, anchor=tk.CENTER)
        self.task_tree.column("due_date", width=100, anchor=tk.CENTER)
        self.task_tree.column("completed", width=80, anchor=tk.CENTER)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action Buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        complete_button = ttk.Button(button_frame, text="Mark Completed", command=self.complete_task)
        complete_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Completed", command=self.clear_completed)
        clear_button.pack(side=tk.RIGHT, padx=5)
    
    def add_task(self):
        description = self.task_entry.get().strip()
        if not description:
            messagebox.showwarning("Warning", "Task description cannot be empty!")
            return
        
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get().strip() or None
        
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.update_task_list()
        
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
    
    def update_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        for task in self.tasks:
            completed = "Yes" if task["completed"] else "No"
            self.task_tree.insert("", tk.END, values=(
                task["id"],
                task["description"],
                task["priority"].capitalize(),
                task["due_date"] or "-",
                completed
            ))
    
    def complete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to mark as completed!")
            return
        
        item = self.task_tree.item(selected[0])
        task_id = item["values"][0]
        
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                self.update_task_list()
                return
    
    def delete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            return
        
        item = self.task_tree.item(selected[0])
        task_id = item["values"][0]
        
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
        self.update_task_list()
    
    def clear_completed(self):
        if not any(task["completed"] for task in self.tasks):
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to clear all completed tasks?"):
            return
        
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.save_tasks()
        self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
