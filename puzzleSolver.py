from tkinter import *
root = Tk()

e = Entry(root, width=5)
e.grid(row=0, column=0)
e.insert(END, '')
for c in range(8):
    e = Entry(root, width=5)
    e.grid(row=0, column=c+1)
    e.insert(END, c)
for r in range(8):
    e = Entry(root, width=5)
    e.grid(row=r, column=0)
    e.insert(END, r)
    for c in range(8):
        e = Entry(root, width=5)
        e.grid(row=r, column=c)
        e.insert(END,1)
root.mainloop()