import datetime
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

import sqlite3

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Data base creation

# Create a connection to the database
conn = sqlite3.connect("tasks.db")

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create a table to store tasks and times
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        time TEXT
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()



# DEFINE FUNCTIONS



def new_task():
    task = entry.get()
    time = entry2.get()
    if time == "":
        time = ' '
    if task != "":
        lb.insert(END, (u'\u25A1 ' + task))
        entry.delete(0, "end")
        lb_time.insert(END, time)
        entry2.delete(0, "end")

        # Save task and time to the database
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
        selected_index = int(selected_index[0])  # Convert to an integer

        # Get the actual task ID from the database
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks")
        task_ids = cursor.fetchall()
        conn.close()

        if selected_index < len(task_ids):
            task_id = task_ids[selected_index][0]

            # Delete task from the database using the correct ID
            conn = sqlite3.connect("tasks.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            conn.close()

            lb.delete(selected_index)
            lb_time.delete(selected_index)

def cross_out():
    task = lb.get(ANCHOR)
    lb.insert(ANCHOR, ''.join([u'\u0336{}'.format(c) for c in task]))
    lb.delete(ANCHOR)


def clock_time():
    time = datetime.datetime.now()
    time = (time.strftime("Сьогодні: %d.%m.%Y \n %H:%M:%S"))
    lb_clock.config(text=time)
    lb_clock.after(1000, clock_time)





def plot_graph(Productivity_Rate, color="red"):
    Hour = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    #Productivity_Rate = [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3, 6.0, 5.8, 5.4]

    fig = Figure(figsize=(5, 2), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.plot(Hour, Productivity_Rate, color=color, marker='o')
    plot.set_title('Продуктивність роботи', fontsize=10)
    plot.set_xlabel('Години', fontsize=10)
    plot.set_ylabel('Продуктивність роботи', fontsize=10)
    plot.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=210, y=550)

def change():
    if var.get() == 0:
        Productivity_Rate = [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3, 6.0, 5.8, 5.4]
        plot_graph(Productivity_Rate, color="red")

    elif var.get() == 1:
        Productivity_Rate2 = [ 6.5, 6.2, 5.5, 9.8, 12, 8, 7.2, 6.9, 7, 6.3, 6.0, 5.8, 5.4]
        plot_graph(Productivity_Rate2, color="green")

    elif var.get() == 2:
        Productivity_Rate3 = [6.5, 6.2, 7.5, 9.8, 10.3, 11.0, 12, 8, 7.2, 6.9, 7, 5.8, 5.4]
        plot_graph(Productivity_Rate3, color="blue")



if (__name__ == "__main__"):
    window = Tk()
    window.geometry('850x850+500+50')
    window.title('TO-DO List')
    window.config(bg='SkyBlue1')
    window.resizable(width=True, height=True)

    lb_clock = Label(window, font=('Times', 18), bg="SkyBlue1")
    lb_clock.place(x=600, y=20)
    clock_time()



    enterTask = Label(window, text="Введіть нове завдання", font=('Times', 20, 'italic', 'bold'), bg='SkyBlue1')
    enterTask.pack(pady=10)

    quote = Label(window, text="Який ми обираємо шлях,\n визначає те,\n куди ми прийдемо",
                  font=('Times', 16, 'italic', 'bold'), bg='SkyBlue1', fg='Gold')
    quote.place(x=600, y=150)

    chron = Label(window, text="Виберіть\n хронотип",
                  font=('Times', 16, 'bold'), bg='SkyBlue1', fg='orange')
    chron.place(x=60, y=540)

    entry = Entry(window, font=('times', 24))

    entry.pack(pady=10)
    enterTime = Label(window, text="Заплануйте час виконання", font=('Times', 18, 'italic'), bg="SkyBlue1")
    enterTime.pack(pady=10)

    entry2 = Entry(window, font=('times', 24))

    entry2.pack(pady=10)

    button_frame = Frame(window)
    button_frame.pack()

    add_task_btn = Button(
        button_frame,
        text='Додати',
        font=('times 14'),
        bg='light blue',

        command=new_task
    )
    add_task_btn.pack(fill=BOTH, expand=True, side=LEFT)

    frame = Frame(window)

    frame.place(x=405, y=300)

    lb = Listbox(
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

    lb.pack(side=LEFT, fill=BOTH)

    sb = Scrollbar(frame)
    sb.pack(side=RIGHT, fill=BOTH)

    lb.config(yscrollcommand=sb.set)
    sb.config(command=lb.yview)
    frame2 = Frame(window)

    frame2.place(x=205, y=300)

    lb_time = Listbox(
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

    lb_time.pack(side=LEFT, fill=BOTH)

    sb_t = Scrollbar(frame2)
    sb_t.pack(side=RIGHT, fill=BOTH)

    lb_time.config(yscrollcommand=sb_t.set)
    sb_t.config(command=lb_time.yview)

    button_frame2 = Frame(window)

    button_frame2.place(x=300, y=480)

    del_task_btn = Button(
        button_frame2,
        text='Видалити завдання',
        font=('times 14'),
        bg='Gold',
        command=delete_task
    )
    del_task_btn.pack(fill=BOTH, expand=True, side=LEFT)

    cross_task_btn = Button(
        button_frame2,
        text='ЗРОБЛЕНО!',
        font=('times 14'),
        bg='Gold',
        command=cross_out
    )
    cross_task_btn.pack(fill=BOTH, expand=True, side=RIGHT)

    # Retrieve tasks and times from the database
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task, time FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    for task, time in tasks:
        lb.insert(END, (u'\u25A1 ' + task))
        lb_time.insert(END, time)

    var = IntVar()
    var.set(0)
    c1 = Radiobutton(text="Сова", font=('times 13'),
                     variable=var, value=0)
    c2 = Radiobutton(text="Жайворонок", font=('times 13'),
                     variable=var, value=1)
    c3 = Radiobutton(text="Голуб", font=('times 13'),
                     variable=var, value=2)
    button = Button(text="Показати", font=('times 14'),
                    bg='light blue', command=change)


    c1.place(x=70, y=600)
    c2.place(x=70, y=630)
    c3.place(x=70, y=660)
    button.place(x=70, y=690)


    image1 = Image.open('D:\\python\\todo_list\\logo31.png')

    image1 = image1.resize((200, 200), Image.LANCZOS)
    test = ImageTk.PhotoImage(image1)
    label1 = tkinter.Label(image=test, bg='SkyBlue1')
    label1.image = test

    # Position image
    label1.place(x=20, y=20)

    window.mainloop()
