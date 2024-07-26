import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Global window variable
window = None

# Database setup
def setup_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_task_to_db(task, time):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (task, time))
    conn.commit()
    conn.close()

def delete_task_from_db(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def fetch_tasks_from_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, time FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Functions for UI actions
def new_task():
    task = entry_task.get()
    time = entry_time.get() or ' '
    if task:
        lb_tasks.insert(tk.END, f'□ {task}')
        lb_times.insert(tk.END, time)
        add_task_to_db(task, time)
        entry_task.delete(0, tk.END)
        entry_time.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Nothing entered!")

def delete_task():
    selected_index = lb_tasks.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        task_ids = [task[0] for task in fetch_tasks_from_db()]
        if selected_index < len(task_ids):
            task_id = task_ids[selected_index]
            delete_task_from_db(task_id)
            lb_tasks.delete(selected_index)
            lb_times.delete(selected_index)

def cross_out():
    task = lb_tasks.get(tk.ANCHOR)
    crossed_task = ''.join([f'\u0336{c}' for c in task])
    lb_tasks.insert(tk.ANCHOR, crossed_task)
    lb_tasks.delete(tk.ANCHOR)

def clock_time():
    current_time = datetime.datetime.now().strftime("Сьогодні: %d.%m.%Y \n %H:%M:%S")
    lb_clock.config(text=current_time)
    lb_clock.after(1000, clock_time)

def plot_graph(window, Productivity_Rate, color="red"):
    hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    fig = Figure(figsize=(5, 2), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(hours, Productivity_Rate, color=color, marker='o')
    ax.set_title('Продуктивність роботи', fontsize=10)
    ax.set_xlabel('Години', fontsize=10)
    ax.set_ylabel('Продуктивність роботи', fontsize=10)
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=210, y=550)

def update_graph():
    productivity_rates = {
        0: [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3, 6.0, 5.8, 5.4],
        1: [6.5, 6.2, 5.5, 9.8, 12, 8, 7.2, 6.9, 7, 6.3, 6.0, 5.8, 5.4],
        2: [6.5, 6.2, 7.5, 9.8, 10.3, 11.0, 12, 8, 7.2, 6.9, 7, 5.8, 5.4]
    }
    color_map = {0: "red", 1: "green", 2: "blue"}
    selected_value = var.get()
    plot_graph(window, productivity_rates.get(selected_value, []), color=color_map.get(selected_value, "red"))



# UI Setup
def setup_ui():
    global windo, entry_task, entry_time, lb_tasks, lb_times, lb_clock, var

    window = tk.Tk()
    window.geometry('850x850+500+50')
    window.title('TO-DO List')
    window.config(bg='SkyBlue1')
    window.resizable(width=True, height=True)

    lb_clock = tk.Label(window, font=('Times', 18), bg="SkyBlue1")
    lb_clock.place(x=600, y=20)
    clock_time()

    tk.Label(window, text="Введіть нове завдання", font=('Times', 20, 'italic', 'bold'), bg='SkyBlue1').pack(pady=10)

    tk.Label(window, text="Який ми обираємо шлях,\n визначає те,\n куди ми прийдемо", font=('Times', 16, 'italic', 'bold'), bg='SkyBlue1', fg='Gold').place(x=600, y=150)

    tk.Label(window, text="Виберіть\n хронотип", font=('Times', 16, 'bold'), bg='SkyBlue1', fg='orange').place(x=60, y=540)

    entry_task = tk.Entry(window, font=('times', 24))
    entry_task.pack(pady=10)

    tk.Label(window, text="Заплануйте час виконання", font=('Times', 18, 'italic'), bg="SkyBlue1").pack(pady=10)

    entry_time = tk.Entry(window, font=('times', 24))
    entry_time.pack(pady=10)

    button_frame = tk.Frame(window)
    button_frame.pack()

    tk.Button(button_frame, text='Додати', font=('times 14'), bg='light blue', command=new_task).pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    frame_tasks = tk.Frame(window)
    frame_tasks.place(x=405, y=300)

    lb_tasks = tk.Listbox(frame_tasks, width=25, height=6, font=('Times', 18, 'bold'), bd=0, fg='blue', highlightthickness=0, selectbackground='#ff8b61', activestyle="none")
    lb_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

    sb_tasks = tk.Scrollbar(frame_tasks)
    sb_tasks.pack(side=tk.RIGHT, fill=tk.BOTH)
    lb_tasks.config(yscrollcommand=sb_tasks.set)
    sb_tasks.config(command=lb_tasks.yview)

    frame_times = tk.Frame(window)
    frame_times.place(x=205, y=300)

    lb_times = tk.Listbox(frame_times, width=15, height=6, font=('Times', 18), bd=0, fg='purple4', highlightthickness=0, selectbackground='#ff8b61', activestyle="none")
    lb_times.pack(side=tk.LEFT, fill=tk.BOTH)

    sb_times = tk.Scrollbar(frame_times)
    sb_times.pack(side=tk.RIGHT, fill=tk.BOTH)
    lb_times.config(yscrollcommand=sb_times.set)
    sb_times.config(command=lb_times.yview)

    button_frame2 = tk.Frame(window)
    button_frame2.place(x=300, y=480)

    tk.Button(button_frame2, text='Видалити завдання', font=('times 14'), bg='Gold', command=delete_task).pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    tk.Button(button_frame2, text='ЗРОБЛЕНО!', font=('times 14'), bg='Gold', command=cross_out).pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

    var = tk.IntVar()
    var.set(0)
    tk.Radiobutton(window, text="Сова", font=('times 13'), variable=var, value=0).place(x=70, y=600)
    tk.Radiobutton(window, text="Жайворонок", font=('times 13'), variable=var, value=1).place(x=70, y=630)
    tk.Radiobutton(window, text="Голуб", font=('times 13'), variable=var, value=2).place(x=70, y=660)
    tk.Button(window, text="Показати", font=('times 14'), bg='light blue', command=update_graph).place(x=70, y=690)

    image1 = Image.open('D:\\python\\todo_list\\logo31.png').resize((200, 200), Image.LANCZOS)
    test = ImageTk.PhotoImage(image1)
    tk.Label(window, image=test, bg='SkyBlue1').place(x=20, y=20)

    tasks = fetch_tasks_from_db()
    for _, task, time in tasks:
        lb_tasks.insert(tk.END, f'□ {task}')
        lb_times.insert(tk.END, time)

    window.mainloop()

if __name__ == "__main__":
    setup_database()
    setup_ui()
