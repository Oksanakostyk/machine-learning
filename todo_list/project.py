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

def plot_graph(Productivity_Rate, color="red"):
    global window
    hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    fig = Figure(figsize=(5, 2), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(hours, Productivity_Rate, color=color)

    ax.fill_between(hours, Productivity_Rate, color=color, alpha=0.3)

    ax.set_title('Продуктивність роботи', fontsize=10)
    ax.set_xlabel('Години', fontsize=10)
    ax.set_ylabel('Продуктивність роботи', fontsize=10)

    ax.set_xticks(range(0, 25, 2))  # Поділки осі x через кожні 2 години
    ax.set_yticks(range(0, max(Productivity_Rate) + 1, 1))

    ax.grid(True, which='both', linestyle='--', linewidth=0.3)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=210, y=550)

def update_graph():
    productivity_rates = {
        0: [2, 2, 2, 3, 4, 4.5, 3, 4, 8, 9, 8, 7, 2],
        1: [1, 1, 8, 9, 7.5, 6, 5, 3, 2.5, 2, 1, 1, 1],
        2: [2, 2, 3, 4, 6, 7, 5, 6, 9, 6, 4, 3, 2]
    }
    color_map = {0: "Gold", 1: "SkyBlue", 2: "blue"}
    selected_value = var.get()
    plot_graph(productivity_rates.get(selected_value, []), color=color_map.get(selected_value, "red"))

def new_task():
    task = entry_task.get()
    hour = cb_hour.get()
    minute = cb_minute.get()
    time = f"{hour}:{minute}"
    if task != "":
        lb.insert(tk.END, (u'\u25A1 ' + task))
        entry_task.delete(0, tk.END)
        lb_time.insert(tk.END, time)
        cb_hour.set('')
        cb_minute.set('')
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, time) VALUES (?, ?)", (task, time))
        conn.commit()
        conn.close()
    else:
        messagebox.showwarning("Warning", "Нічого не введено!")

def delete_task():
    selected_index = lb.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks")
        task_ids = cursor.fetchall()
        conn.close()
        if selected_index < len(task_ids):
            task_id = task_ids[selected_index][0]
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            conn.close()
            lb.delete(selected_index)
            lb_time.delete(selected_index)

def cross_out():
    task = lb.get(tk.ANCHOR)
    lb.insert(tk.ANCHOR, ''.join([u'\u0336{}'.format(c) for c in task]))
    lb.delete(tk.ANCHOR)

def clock_time():
    time = datetime.datetime.now()
    time = (time.strftime("Сьогодні: %d.%m.%Y \n %H:%M:%S"))
    lb_clock.config(text=time)
    lb_clock.after(1000, clock_time)

def setup_ui():
    global window
    window = tk.Tk()
    window.geometry('850x850+500+50')
    window.title('TO-DO List')
    window.config(bg='SkyBlue1')
    window.resizable(width=True, height=True)

    global lb_clock, entry_task, cb_hour, cb_minute, lb, lb_time, var

    lb_clock = tk.Label(window, font=('Times', 18), bg="SkyBlue1")
    lb_clock.place(x=600, y=20)
    clock_time()

    enterTask = tk.Label(window, text="Введіть нове завдання", font=('Times', 20, 'italic', 'bold'), bg='SkyBlue1')
    enterTask.pack(pady=10)

    quote = tk.Label(window, text="Який ми обираємо шлях,\n визначає те,\n куди ми прийдемо",
                     font=('Times', 16, 'italic', 'bold'), bg='SkyBlue1', fg='Gold')
    quote.place(x=600, y=150)

    chron = tk.Label(window, text="Виберіть\n хронотип",
                     font=('Times', 16, 'bold'), bg='SkyBlue1', fg='orange')
    chron.place(x=60, y=540)

    entry_task = tk.Entry(window, font=('times', 24))
    entry_task.pack(pady=10)

    enterTime = tk.Label(window, text="Заплануйте час виконання", font=('Times', 18, 'italic'), bg="SkyBlue1")
    enterTime.pack(pady=10)

    time_frame = tk.Frame(window)
    time_frame.pack(pady=10)

    cb_hour = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=5, font=('times', 24))
    cb_hour.pack(side=tk.LEFT, padx=5)
    cb_minute = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=5, font=('times', 24))
    cb_minute.pack(side=tk.LEFT, padx=5)

    button_frame = tk.Frame(window)
    button_frame.pack()

    add_task_btn = tk.Button(
        button_frame,
        text='Додати',
        font=('times 14'),
        bg='light blue',
        command=new_task
    )
    add_task_btn.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    frame = tk.Frame(window)
    frame.place(x=405, y=300)

    lb = tk.Listbox(
        frame,
        width=25,
        height=6,
        font=('Times', 18, 'bold'),
        bd=0,
        fg='blue',
        highlightthickness=0,
        selectbackground='#ff8b61',
        activestyle="none",
    )
    lb.pack(side=tk.LEFT, fill=tk.BOTH)

    sb = tk.Scrollbar(frame)
    sb.pack(side=tk.RIGHT, fill=tk.BOTH)

    lb.config(yscrollcommand=sb.set)
    sb.config(command=lb.yview)

    frame2 = tk.Frame(window)
    frame2.place(x=205, y=300)

    lb_time = tk.Listbox(
        frame2,
        width=15,
        height=6,
        font=('Times', 18),
        bd=0,
        fg='purple4',
        highlightthickness=0,
        selectbackground='#ff8b61',
        activestyle="none",
    )
    lb_time.pack(side=tk.LEFT, fill=tk.BOTH)

    sb_t = tk.Scrollbar(frame2)
    sb_t.pack(side=tk.RIGHT, fill=tk.BOTH)

    lb_time.config(yscrollcommand=sb_t.set)
    sb_t.config(command=lb_time.yview)

    button_frame2 = tk.Frame(window)
    button_frame2.place(x=300, y=480)

    del_task_btn = tk.Button(
        button_frame2,
        text='Видалити завдання',
        font=('times 14'),
        bg='Gold',
        command=delete_task
    )
    del_task_btn.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    cross_task_btn = tk.Button(
        button_frame2,
        text='ЗРОБЛЕНО!',
        font=('times 14'),
        bg='Gold',
        command=cross_out
    )
    cross_task_btn.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

    var = tk.IntVar()
    var.set(0)
    c1 = tk.Radiobutton(text="Сова", font=('times 13'),
                        variable=var, value=0)
    c2 = tk.Radiobutton(text="Жайворонок", font=('times 13'),
                        variable=var, value=1)
    c3 = tk.Radiobutton(text="Голуб", font=('times 13'),
                        variable=var, value=2)
    button = tk.Button(text="Показати", font=('times 14'),
                       bg='light blue', command=update_graph)

    c1.place(x=70, y=600)
    c2.place(x=70, y=630)
    c3.place(x=70, y=660)
    button.place(x=70, y=690)

    image1 = Image.open('D:\\python\\todo_list\\logo31.png')
    image1 = image1.resize((200, 200), Image.LANCZOS)
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image=test, bg='SkyBlue1')
    label1.image = test
    label1.place(x=20, y=20)

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task, time FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    for task, time in tasks:
        lb.insert(tk.END, (u'\u25A1 ' + task))
        lb_time.insert(tk.END, time)

if __name__ == "__main__":
    setup_database()
    setup_ui()
    window.mainloop()