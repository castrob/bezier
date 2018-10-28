from tkinter import *
import numpy as np

class Paint(object):
    def __init__(self):
        self.root = Tk()
        self.bezier_linear_button = Button(self.root, text='Bezier Linear', command=self.use_bezier_linear)
        #defindo botão para criar bezier linear
        self.bezier_linear_button.grid(row = 0, column = 0)

        #definir canvas
        self.c = Canvas(self.root, bg='white', width=600, heigh=600)
        self.c.grid(row=1,columnspan=1)#talvez esse 5 seja 1

        self.setup()

        self.root.mainloop()

    def setup(self):
        self.x = None
        self.y = None
        self.line_width = 5
        self.color = 'black'
        self.active_button = self.bezier_linear_button
        self.c.bind('<Button-1>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.root.bind('<Return>', self.bezier)

    def use_bezier_linear(self):
        self.activate_button(self.bezier_linear_button)
    
    def activate_button(self, some_button):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button

    def paint(self, event):
        global lista_pontos
        self.x = event.x
        self.y = event.y
        lista_pontos.append((self.x,self.y))
        print("Clicked at: ", self.x, self.y)
        self.c.create_oval(self.x-1, self.y-1, self.x+1, self.y+1, width=5, fill= 'blue', outline='blue')
        coordinates = "(%s,%s)" %(self.x, self.y)
        self.c.create_text(self.x, self.y-15, text = coordinates, fill='blue' )

    def reset(self, event):
        self.x = self.y = None

    def bezier(self, event):
        pontos = np.linspace(0,1, num=1000)
        for t in pontos:
            a = self.point_in_line(lista_pontos[0], lista_pontos[1], t)
            b = self.point_in_line(lista_pontos[1], lista_pontos[2], t)
            c = self.point_in_line(lista_pontos[2], lista_pontos[3], t)
            d = self.point_in_line(a,b,t)
            e = self.point_in_line(b,c,t)
            f = self.point_in_line(d,e,t)
            x, y = f
            self.c.create_oval(x-1, y-1, x+1, y+1, width=0, fill= 'red', outline='red')

    def point_in_line(self, p0, p1, t):
        x, y = p0
        w, z = p1
        u = x - ((x - w)* t)
        v = y - ((y - z)* t)
        return (u,v)

if __name__ == '__main__':
    lista_pontos = []
    Paint()
