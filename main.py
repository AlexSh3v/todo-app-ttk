import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

from ttkbootstrap import Window

from todo_list import TaskManager


@dataclass
class TodoApp:
    def __init__(self, root: Window):
        self.root = root
        self.root.title("✓ Simple Todo List")
        self.root.geometry('448x265+40+69')
        self.root.resizable(False, False)
        self.task_manager = TaskManager()

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill="both", expand=True)

        self.task_list = tk.Listbox(self.frame, width=40, height=10, font=("Helvetica", 14))
        self.task_list.pack(fill="both", expand=True)

        self.entry_frame = ttk.Frame(self.frame)
        self.entry_frame.pack(fill="x")

        self.task_name_entry = ttk.Entry(self.entry_frame, width=30)
        self.task_name_entry.pack(side="left")

        self.add_button = ttk.Button(self.entry_frame, text="➕", command=self.add_task)
        self.add_button.pack(side="left")

        self.delete_button = ttk.Button(self.entry_frame, text="✖", command=self.delete_task)
        self.delete_button.pack(side="left")

        self.mark_button = ttk.Button(self.entry_frame, text="✔️", command=self.mark_task)
        self.mark_button.pack(side="left")

        # self.move_button = ttk.Button(self.entry_frame, text="Move Task", command=self.move_task)
        # self.move_button.pack(side="left")

        self.move_down_button = ttk.Button(self.entry_frame, text="↓", command=self.move_down)
        self.move_down_button.pack(side="left")

        self.move_up_button = ttk.Button(self.entry_frame, text="↑", command=self.move_up)
        self.move_up_button.pack(side="left")

        self.update_task_list()

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.task_manager.tasks:
            completed_str = "✓" if task["is_completed"] else ""
            self.task_list.insert(tk.END, f"{completed_str} {task['name']}")

    def add_task(self):
        task_name = self.task_name_entry.get()

        if task_name:
            self.task_manager.add_task(task_name, False)
            self.task_manager.save()
            self.update_task_list()
            self.task_name_entry.delete(0, tk.END)
            self.task_name_entry.configure(bootstyle='default')
            return

        self.task_name_entry.configure(bootstyle='danger')

    def delete_task(self):
        selection = self.task_list.curselection()
        if selection:
            index, *_ = selection
            task = self.task_manager.tasks[index]
            if self.task_manager.delete_task(task['id']):
                self.task_manager.save()
                self.update_task_list()

    def mark_task(self):
        selection = self.task_list.curselection()
        if selection:
            index, *_ = selection
            task = self.task_manager.tasks[index]
            if self.task_manager.mark_task(task['id']):
                self.task_manager.save()
                self.update_task_list()

    def move_task(self):
        selection = self.task_list.curselection()
    #     if selection:
    #         index, *_ = selection
    #         task = self.task_manager.tasks[index]
    #         pos = selection[0]
    #         if self.task_manager.move(task_id, pos):
    #             self.task_manager.save()
    #             self.update_task_list()

    def move_down(self):
        selection = self.task_list.curselection()
        if selection:
            index, *_ = selection
            task = self.task_manager.tasks[index]
            index = selection[0]
            if index < len(self.task_manager.tasks):
                self.task_manager.move(task['id'], index+1)
                self.task_manager.save()
                self.update_task_list()

    def move_up(self):
        selection = self.task_list.curselection()
        if selection:
            index, *_ = selection
            task = self.task_manager.tasks[index]
            index = selection[0]
            if index > 0:
                self.task_manager.move(task['id'], index - 1)
                self.task_manager.save()
                self.update_task_list()


if __name__ == "__main__":
    root = Window()
    app = TodoApp(root)
    root.mainloop()
