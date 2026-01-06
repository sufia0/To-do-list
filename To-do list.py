import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Todo Dashboard")
        self.root.geometry("900x650")
        self.root.configure(bg="#1a1a2e")
        
        # Data storage
        self.tasks = []
        self.load_tasks()
        
        # Color scheme
        self.bg_dark = "#1a1a2e"
        self.bg_medium = "#16213e"
        self.bg_light = "#0f3460"
        self.accent = "#e94560"
        self.accent_light = "#ff6b81"
        self.text_color = "#eaeaea"
        self.success = "#26de81"
        
        self.setup_ui()
        self.refresh_task_list()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.bg_medium, height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        title = tk.Label(header, text="📋 Todo Dashboard", font=("Helvetica", 28, "bold"),
                        bg=self.bg_medium, fg=self.text_color)
        title.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_dark)
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left panel - Task input
        left_panel = tk.Frame(main_container, bg=self.bg_light, width=350)
        left_panel.pack(side="left", fill="both", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Input section
        input_frame = tk.Frame(left_panel, bg=self.bg_light)
        input_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(input_frame, text="Task Title", font=("Helvetica", 12, "bold"),
                bg=self.bg_light, fg=self.text_color).pack(anchor="w", pady=(0, 5))
        
        self.task_title = tk.Entry(input_frame, font=("Helvetica", 11), bg=self.bg_medium,
                                   fg=self.text_color, insertbackground=self.text_color,
                                   relief="flat", bd=5)
        self.task_title.pack(fill="x", ipady=8)
        
        tk.Label(input_frame, text="Description", font=("Helvetica", 12, "bold"),
                bg=self.bg_light, fg=self.text_color).pack(anchor="w", pady=(15, 5))
        
        self.task_desc = tk.Text(input_frame, font=("Helvetica", 10), bg=self.bg_medium,
                                fg=self.text_color, insertbackground=self.text_color,
                                relief="flat", bd=5, height=4, wrap="word")
        self.task_desc.pack(fill="x")
        
        # Priority selection
        tk.Label(input_frame, text="Priority", font=("Helvetica", 12, "bold"),
                bg=self.bg_light, fg=self.text_color).pack(anchor="w", pady=(15, 5))
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_frame = tk.Frame(input_frame, bg=self.bg_light)
        priority_frame.pack(fill="x", pady=5)
        
        for priority in ["Low", "Medium", "High"]:
            rb = tk.Radiobutton(priority_frame, text=priority, variable=self.priority_var,
                               value=priority, bg=self.bg_light, fg=self.text_color,
                               selectcolor=self.bg_medium, font=("Helvetica", 10))
            rb.pack(side="left", padx=10)
        
        # Buttons
        button_frame = tk.Frame(left_panel, bg=self.bg_light)
        button_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        self.add_btn = tk.Button(button_frame, text="➕ Add Task", command=self.add_task,
                                bg=self.accent, fg="white", font=("Helvetica", 12, "bold"),
                                relief="flat", cursor="hand2", pady=10)
        self.add_btn.pack(fill="x", pady=5)
        
        self.update_btn = tk.Button(button_frame, text="✏️ Update Task", command=self.update_task,
                                    bg=self.success, fg="white", font=("Helvetica", 12, "bold"),
                                    relief="flat", cursor="hand2", pady=10, state="disabled")
        self.update_btn.pack(fill="x", pady=5)
        
        self.cancel_btn = tk.Button(button_frame, text="❌ Cancel", command=self.cancel_edit,
                                    bg=self.bg_medium, fg="white", font=("Helvetica", 12, "bold"),
                                    relief="flat", cursor="hand2", pady=10, state="disabled")
        self.cancel_btn.pack(fill="x", pady=5)
        
        # Stats frame
        stats_frame = tk.Frame(left_panel, bg=self.bg_medium)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.stats_label = tk.Label(stats_frame, text="", font=("Helvetica", 10),
                                    bg=self.bg_medium, fg=self.text_color, justify="left")
        self.stats_label.pack(pady=10, padx=10)
        
        # Right panel - Task list
        right_panel = tk.Frame(main_container, bg=self.bg_light)
        right_panel.pack(side="left", fill="both", expand=True)
        
        # Task list header
        list_header = tk.Frame(right_panel, bg=self.bg_medium, height=50)
        list_header.pack(fill="x")
        list_header.pack_propagate(False)
        
        tk.Label(list_header, text="Your Tasks", font=("Helvetica", 16, "bold"),
                bg=self.bg_medium, fg=self.text_color).pack(side="left", padx=20, pady=10)
        
        # Task list with scrollbar
        list_frame = tk.Frame(right_panel, bg=self.bg_light)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame, bg=self.bg_light)
        scrollbar.pack(side="right", fill="y")
        
        self.task_canvas = tk.Canvas(list_frame, bg=self.bg_light, highlightthickness=0,
                                     yscrollcommand=scrollbar.set)
        self.task_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.task_canvas.yview)
        
        self.task_frame = tk.Frame(self.task_canvas, bg=self.bg_light)
        self.task_canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        
        self.task_frame.bind("<Configure>", lambda e: self.task_canvas.configure(
            scrollregion=self.task_canvas.bbox("all")))
        
        self.editing_task_id = None
        
    def add_task(self):
        title = self.task_title.get().strip()
        desc = self.task_desc.get("1.0", "end-1c").strip()
        priority = self.priority_var.get()
        
        if not title:
            messagebox.showwarning("Input Error", "Please enter a task title!")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": desc,
            "priority": priority,
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.clear_inputs()
        self.refresh_task_list()
        
    def create_task_widget(self, task):
        # Task card
        card = tk.Frame(self.task_frame, bg=self.bg_medium, relief="flat", bd=0)
        card.pack(fill="x", pady=5, padx=5)
        
        # Priority indicator
        priority_colors = {"Low": "#3498db", "Medium": "#f39c12", "High": "#e74c3c"}
        priority_bar = tk.Frame(card, bg=priority_colors[task["priority"]], width=5)
        priority_bar.pack(side="left", fill="y")
        
        # Content area
        content = tk.Frame(card, bg=self.bg_medium)
        content.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Title with strikethrough if completed
        title_text = task["title"]
        if task["completed"]:
            title_label = tk.Label(content, text=f"✓ {title_text}", font=("Helvetica", 12, "bold", "overstrike"),
                                  bg=self.bg_medium, fg="#888", anchor="w")
        else:
            title_label = tk.Label(content, text=title_text, font=("Helvetica", 12, "bold"),
                                  bg=self.bg_medium, fg=self.text_color, anchor="w")
        title_label.pack(anchor="w")
        
        # Description
        if task["description"]:
            desc_label = tk.Label(content, text=task["description"], font=("Helvetica", 9),
                                 bg=self.bg_medium, fg="#aaa", anchor="w", wraplength=350, justify="left")
            desc_label.pack(anchor="w", pady=(3, 0))
        
        # Meta info
        meta_text = f"Priority: {task['priority']} | Created: {task['created']}"
        meta_label = tk.Label(content, text=meta_text, font=("Helvetica", 8),
                             bg=self.bg_medium, fg="#666", anchor="w")
        meta_label.pack(anchor="w", pady=(5, 0))
        
        # Buttons
        btn_frame = tk.Frame(card, bg=self.bg_medium)
        btn_frame.pack(side="right", padx=10)
        
        if not task["completed"]:
            complete_btn = tk.Button(btn_frame, text="✓", command=lambda: self.complete_task(task["id"]),
                                    bg=self.success, fg="white", font=("Helvetica", 10, "bold"),
                                    width=3, relief="flat", cursor="hand2")
            complete_btn.pack(side="left", padx=2)
        
        edit_btn = tk.Button(btn_frame, text="✏", command=lambda: self.edit_task(task["id"]),
                            bg=self.accent_light, fg="white", font=("Helvetica", 10, "bold"),
                            width=3, relief="flat", cursor="hand2")
        edit_btn.pack(side="left", padx=2)
        
        delete_btn = tk.Button(btn_frame, text="🗑", command=lambda: self.delete_task(task["id"]),
                              bg="#c0392b", fg="white", font=("Helvetica", 10, "bold"),
                              width=3, relief="flat", cursor="hand2")
        delete_btn.pack(side="left", padx=2)
        
    def refresh_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        
        if not self.tasks:
            empty_label = tk.Label(self.task_frame, text="No tasks yet! Add your first task.",
                                  font=("Helvetica", 12), bg=self.bg_light, fg="#666", pady=50)
            empty_label.pack()
        else:
            for task in self.tasks:
                self.create_task_widget(task)
        
        self.update_stats()
        
    def update_stats(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed
        
        stats_text = f"📊 Statistics\n\nTotal Tasks: {total}\nCompleted: {completed}\nPending: {pending}"
        self.stats_label.config(text=stats_text)
        
    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                break
        self.save_tasks()
        self.refresh_task_list()
        
    def edit_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.task_title.delete(0, "end")
                self.task_title.insert(0, task["title"])
                self.task_desc.delete("1.0", "end")
                self.task_desc.insert("1.0", task["description"])
                self.priority_var.set(task["priority"])
                
                self.editing_task_id = task_id
                self.add_btn.config(state="disabled")
                self.update_btn.config(state="normal")
                self.cancel_btn.config(state="normal")
                break
                
    def update_task(self):
        title = self.task_title.get().strip()
        desc = self.task_desc.get("1.0", "end-1c").strip()
        priority = self.priority_var.get()
        
        if not title:
            messagebox.showwarning("Input Error", "Please enter a task title!")
            return
        
        for task in self.tasks:
            if task["id"] == self.editing_task_id:
                task["title"] = title
                task["description"] = desc
                task["priority"] = priority
                break
        
        self.save_tasks()
        self.cancel_edit()
        self.refresh_task_list()
        
    def cancel_edit(self):
        self.clear_inputs()
        self.editing_task_id = None
        self.add_btn.config(state="normal")
        self.update_btn.config(state="disabled")
        self.cancel_btn.config(state="disabled")
        
    def delete_task(self, task_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            self.save_tasks()
            self.refresh_task_list()
            
    def clear_inputs(self):
        self.task_title.delete(0, "end")
        self.task_desc.delete("1.0", "end")
        self.priority_var.set("Medium")
        
    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=2)
            
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()