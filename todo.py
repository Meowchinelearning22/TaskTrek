import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import time
from datetime import datetime

TODO_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "The tasks file is corrupted. Starting with an empty task list.")
        return []

def save_tasks(tasks):
    try:
        with open(TODO_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
    except IOError:
        messagebox.showerror("Error", "Failed to save tasks. Please check file permissions.")

def animate_task_removal(widget, index):
    for i in range(10, -1, -1):
        widget.configure(fg=f"#{hex(int(255 - i * 25.5))[2:]}0000")
        widget.place_configure(relx=0.5, rely=0.5 - (i * 0.02))
        root.update_idletasks()
        time.sleep(0.03)

    del tasks[index]
    save_tasks(tasks)
    update_task_list()

def add_task():
    task_text = task_entry.get().strip()
    priority = priority_var.get()
    due_date = due_date_entry.get_date().strftime("%Y-%m-%d")

    if task_text:
        tasks.append({"task": task_text, "completed": False, "priority": priority, "due_date": due_date})
        sort_tasks()
        save_tasks(tasks)
        update_task_list(animated=True)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def sort_tasks():
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: (priority_order.get(x["priority"], 2), x["due_date"]))

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    theme = dark_theme if dark_mode else light_theme
    root.configure(bg=theme["bg"])
    task_frame.configure(bg=theme["frame_bg"])
    header_label.configure(bg=theme["bg"], fg=theme["fg"])
    due_date_label.configure(bg=theme["bg"], fg=theme["fg"])

    toggle_button.configure(
        bg=theme["button_bg"],
        fg=theme["fg"],
        activebackground=theme["button_bg"],
        activeforeground=theme["fg"]
    )
    
    add_button.configure(
        bg=theme["button_add"],
        fg="white",
        activebackground=theme["button_add"],
        activeforeground="white"
    )
    
    delete_button.configure(
        bg=theme["button_del"],
        fg="white",
        activebackground=theme["button_del"],
        activeforeground="white"
    )

    for i in range(10):
        root.update_idletasks()
        time.sleep(0.02)

    update_task_list()

def update_task_list(animated=False):
    for widget in task_frame.winfo_children():
        widget.destroy()

    theme = dark_theme if dark_mode else light_theme
    global task_vars
    task_vars = []

    for i, task in enumerate(tasks):
        var = tk.BooleanVar(value=task["completed"])

        task_item = tk.Frame(
            task_frame,
            bg=theme["task_bg"],
            relief="flat",
            bd=3,
            highlightbackground=theme["task_border"],
            highlightthickness=2
        )
        task_item.pack(fill="x", padx=10, pady=5, ipadx=5, ipady=5)

        chk = tk.Checkbutton(
            task_item,
            text=f"{task['task']} (Due: {task['due_date']})",
            variable=var,
            command=lambda i=i: animate_task_removal(task_item, i),
            font=("Poppins", 12),
            padx=10,
            bg=theme["task_bg"],
            fg=theme["fg"],
            selectcolor=theme["task_bg"],
            activebackground=theme["task_bg"]
        )

        if task["priority"] == "High":
            chk.config(fg="red", font=("Poppins", 12, "bold"))
            task_item.configure(highlightbackground="red", highlightthickness=3)
        elif task["priority"] == "Medium":
            chk.config(fg="orange")
        else:
            chk.config(fg="blue")

        chk.pack(anchor="w", padx=10)
        task_vars.append(var)

        if animated:
            fade_in(task_item)

def fade_in(widget):
    for i in range(10):
        widget.configure(bg=f"#{hex(255 - i * 25)[2:]}5050")
        root.update_idletasks()
        time.sleep(0.03)

def delete_selected_tasks():
    selected_indices = [i for i, var in enumerate(task_vars) if var.get()]
    if not selected_indices:
        messagebox.showinfo("Info", "No tasks selected!")
        return
    
    if messagebox.askyesno("Confirm", "Are you sure you want to delete the selected tasks?"):
        for index in reversed(selected_indices):
            del tasks[index]
        save_tasks(tasks)
        update_task_list()

# Initialize the main window
root = tk.Tk()
root.title("🔥 Modern To-Do List")
root.geometry("550x650")

# Theme definitions
dark_theme = {
    "bg": "#1e1e1e",
    "fg": "white",
    "task_bg": "#282828",
    "frame_bg": "#333",
    "task_border": "#444",
    "button_bg": "#444",
    "button_add": "#4CAF50",
    "button_del": "#E74C3C"
}

light_theme = {
    "bg": "#f9f9f9",
    "fg": "#333",
    "task_bg": "#fff",
    "frame_bg": "#e0e0e0",
    "task_border": "#ccc",
    "button_bg": "#ddd",
    "button_add": "#2E86C1",
    "button_del": "#C0392B"
}

# Initialize variables
dark_mode = True
tasks = load_tasks()
sort_tasks()

# Create UI elements
header_label = tk.Label(
    root,
    text="🔥 Modern To-Do List",
    font=("Poppins", 18, "bold"),
    fg="white"
)
header_label.pack(pady=10)

task_entry = tk.Entry(
    root,
    width=40,
    font=("Poppins", 12),
    relief="flat",
    bd=2
)
task_entry.pack(pady=10, ipady=5)

priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(
    root,
    textvariable=priority_var,
    values=["High", "Medium", "Low"],
    state="readonly"
)
priority_menu.pack()

due_date_label = tk.Label(
    root,
    text="📅 Due Date:",
    font=("Poppins", 12)
)
due_date_label.pack()

due_date_entry = DateEntry(
    root,
    width=12,
    background="darkblue",
    foreground="white",
    borderwidth=2,
    date_pattern="yyyy-mm-dd"
)
due_date_entry.pack()

toggle_button = tk.Button(
    root,
    text="🌗 Toggle Dark Mode",
    command=toggle_theme,
    font=("Poppins", 12, "bold"),
    relief="flat",
    bd=2
)
toggle_button.pack(pady=5, ipadx=5, ipady=2)

add_button = tk.Button(
    root,
    text="➕ Add Task",
    command=add_task,
    font=("Poppins", 12, "bold"),
    relief="flat",
    bd=2
)
add_button.pack(pady=5, ipadx=5, ipady=5)

delete_button = tk.Button(
    root,
    text="❌ Delete Selected",
    command=delete_selected_tasks,
    font=("Poppins", 12, "bold"),
    relief="flat",
    bd=2
)
delete_button.pack(pady=5, ipadx=5, ipady=5)

task_frame = tk.Frame(
    root,
    bg=dark_theme["frame_bg"],
    relief="flat",
    bd=3
)
task_frame.pack(pady=10, fill="both", expand=True)

# Apply initial theme
apply_theme()

# Start the application
root.mainloop()
