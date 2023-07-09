from tkinter import *
import os

def btn_clicked():
    print("Button Clicked")

window = Tk()
window.geometry("600x700")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=700,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

background_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "background.png"))
background = canvas.create_image(300.0, 350.0, image=background_img)

img0 = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img0.png"))
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

b0.place(x=61, y=547, width=173, height=44)

img1 = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img1.png"))
b1 = Button(
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

b1.place(x=362, y=261, width=173, height=44)

img2 = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img2.png"))
b2 = Button(
    image=img2,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

b2.place(x=367, y=578, width=173, height=44)

img3 = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img3.png"))
b3 = Button(
    image=img3,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat"
)

b3.place(x=61, y=609, width=173, height=44)

entry0_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox0.png"))
entry0_bg = canvas.create_image(533.0, 132.5, image=entry0_img)

entry0 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0
)

entry0.place(x=480.0, y=124, width=106.0, height=15)

entry1_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox1.png"))
entry1_bg = canvas.create_image(533.0, 151.5, image=entry1_img)

entry1 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0
)

entry1.place(x=480.0, y=143, width=106.0, height=15)

entry2_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox2.png"))
entry2_bg = canvas.create_image(533.0, 170.5, image=entry2_img)

entry2 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0
)

entry2.place(x=480.0, y=162, width=106.0, height=15)

entry3_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox3.png"))
entry3_bg = canvas.create_image(533.0, 189.5, image=entry3_img)

entry3 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0
)

entry3.place(x=480.0, y=181, width=106.0, height=15)

entry4_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox4.png"))
entry4_bg = canvas.create_image(487.5, 222.5, image=entry4_img)

entry4 = Entry(
    bd=0,
    bg="#324965",
    highlightthickness=0
)

entry4.place(x=389.0, y=214, width=197.0, height=15)

canvas.create_text(497.0, 415.5, text="numero", fill="#ffffff", font=("Alata-Regular", int(12.0)))
canvas.create_text(508.0, 433.5, text="custo_total", fill="#ffffff", font=("Alata-Regular", int(12.0)))
canvas.create_text(515.5, 450.5, text="valor_total_b", fill="#ffffff", font=("Alata-Regular", int(12.0)))
canvas.create_text(489.5, 491.5, text="lucro", fill="#ffffff", font=("Alata-Regular", int(12.0)))
canvas.create_text(513.0, 508.5, text="multiplicador", fill="#ffffff", font=("Alata-Regular", int(12.0)))
canvas.create_text(513.5, 468.5, text="valor_total_l", fill="#ffffff", font=("Alata-Regular", int(12.0)))

entry5_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gui", "img_textBox5.png"))
entry5_bg = canvas.create_image(150.5, 309.0, image=entry5_img)

entry5 = Entry(
    bd=0,
    bg="#16202d",
    highlightthickness=0
)

entry5.place(x=18.0, y=95, width=265.0, height=426)

window.resizable(False, False)
window.mainloop()
