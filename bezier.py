from tkinter import *
import numpy as np

# Classe Paint principal para lidar com a janela de interacao com o usuario
class Paint(object):
    def __init__(self):
        self.root = Tk()
        self.bezier_linear_button = Button(self.root, text='Bézier Linear', command=self.use_bezier_linear)
        self.bezier_linear_button.grid(row = 0, column = 0)

        self.bezier_quadratic_button = Button(self.root, text='Bézier Quadrática', command=self.use_bezier_quadratic)
        self.bezier_quadratic_button.grid(row = 0, column = 1)

        self.bezier_cubic_button = Button(self.root, text='Bézier Cúbica', command=self.use_bezier_cubic)
        self.bezier_cubic_button.grid(row = 0, column = 2)

        self.clear_button = Button(self.root, text='Limpar', command=self.limpar)
        self.clear_button.grid(row = 0, column = 3)

        self.stop_button = Button(self.root, text="Stop")
        #definir canvas (area de desenho do usuario)
        self.c = Canvas(self.root, bg='white', width=800, heigh=600)
        self.c.grid(row=1,columnspan=4)#talvez esse 5 seja 1
        self.root.title("GC - Curvas de Bézier - 562874 - João Castro")

        self.setup()

        self.root.mainloop()
    #Inicializando os elementos do programa como x e y, espessura da linha desenhada e outras informacoes
    def setup(self):
        self.x = None
        self.y = None
        self.line_width = 5
        self.color = 'black'
        self.active_button = self.bezier_linear_button
        self.c.bind('<Button-1>', self.paint) #quando o mouse e' clicado, ele chama o metodo paint para pegar o x e y do local clicado
        self.c.bind('<ButtonRelease-1>', self.reset) #quando o mouse e liberado, ele limpa o x e y para que um novo possa ser atribuido
    # metodo para o botao limpar, que zera a lista de pontos e limpa todos os elementos do canvas
    def limpar(self):
        self.c.delete("all")
        global lista_pontos
        lista_pontos = []
    #Funcoes use_ servem para ativar e desativar os botoes do menu, deixando os afundados quando clicados e os demais normais.
    def use_bezier_linear(self):
        self.activate_button(self.bezier_linear_button)
    
    def use_bezier_quadratic(self):
        self.activate_button(self.bezier_quadratic_button)

    def use_bezier_cubic(self):
        self.activate_button(self.bezier_cubic_button)        
    #Funcao responsavel por deixar o botao como sunken ou raised, ou seja, ativo ou nao.
    def activate_button(self, some_button):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
    #metodo chamado para mostrar os pontos clicados pelo usuario e chamar os metodos de bezier
    def paint(self, event):
        global lista_pontos
        self.x = event.x 
        self.y = event.y
        if(self.active_button != self.stop_button):
            lista_pontos.append((self.x,self.y)) #Colocando o novo ponto clicado como ponto de controle de bezier
            self.c.create_oval(self.x-1, self.y-1, self.x+1, self.y+1, width=5, fill= 'blue', outline='blue') #Plotando uma bolinha para o ponto de controle
            coordinates = "(%s,%s)" %(self.x, self.y)
            self.c.create_text(self.x, self.y-15, text = coordinates, fill='blue' ) #texto de coordenadas x,y do ponto clicado
        #caso a lista ja possua 3 pontos, chama o metodo bezier, e bloqueia os cliques futuros e assim por diante..
        if len(lista_pontos) == 3 and self.active_button == self.bezier_quadratic_button:
            self.activate_button(self.stop_button)
            self.bezier()
        elif len(lista_pontos) == 4 and self.active_button == self.bezier_cubic_button:
            self.activate_button(self.stop_button)
            self.bezier()
        elif len(lista_pontos) == 2 and self.active_button == self.bezier_linear_button:
            self.activate_button(self.stop_button)
            self.bezier()
        else: pass
    #reset limpa o x e y atual.
    def reset(self, event):
        self.x = self.y = None
    #Metodo de chamada para o calculo de bezier, 
    def bezier(self):
        global lista_pontos
        if len(lista_pontos) == 2: #bezier linear
            pontos = np.linspace(0,1, num=1000)
            for t in pontos:
                x, y = self.linear_bezier(lista_pontos[0], lista_pontos[1], t)
                self.c.create_oval(x-1, y-1, x+1, y+1, width=0, fill= 'red', outline='red')
            lista_pontos = []
        elif len(lista_pontos) == 3:#bezier quadratico
            pontos = np.linspace(0,1, num=1000)
            for t in pontos:
                x, y = self.quadratic_bezier(lista_pontos[0], lista_pontos[1], lista_pontos[2], t)
                self.c.create_oval(x-1, y-1, x+1, y+1, width=0, fill= 'red', outline='red')
            lista_pontos = []
        else:
            pontos = np.linspace(0,1, num=1000) #bezier cubico
            for t in pontos:
                x, y = self.cubic_bezier(lista_pontos[0], lista_pontos[1], lista_pontos[2], lista_pontos[3], t)
                self.c.create_oval(x-1, y-1, x+1, y+1, width=0, fill= 'red', outline='red')
            lista_pontos = []


    #Metodo para calcular a curva de bezier linear usando a seguinte formula geral
    # P(t) = (1 - t)P0 + tP1
    def linear_bezier(self, p0, p1, t):
        xp0, yp0 = p0
        xp1, yp1 = p1
        xp0 = (1-t) * xp0
        yp0 = (1-t) * yp0
        xp1 = t * xp1
        yp1 = t * yp1
        return (xp0 + xp1, yp0 + yp1)

    #Metodo para calcular a curva de bezier quadratica usando a segunte formula geral
    # C1(t) = (1 - t)²P0 + 2t(1 - t)P1 + t²P2
    def quadratic_bezier(self, p0, p1, p2, t):
        xp0, yp0 = p0
        xp1, yp1 = p1
        xp2, yp2 = p2
        a = (1-t)**2
        t2 = t**2
        xp0 = a * xp0
        yp0 = a * yp0
        xp1 = 2 * t * (1-t) * xp1
        yp1 = 2 * t * (1-t) * yp1
        xp2 = t2 * xp2
        yp2 = t2 * yp2
        return (xp0 + xp1 + xp2, yp0 + yp1 + yp2)

    # Metodo pra calcular a curva de bezier cubica usando a seguinte formula geral
    # C3(t) = (1 - t)³P0 + 3t(1 - t)²P1 + 3t²(1 - t)P2 + t³P3
    def cubic_bezier(self, p0, p1, p2, p3, t):
        xp0, yp0 = p0
        xp1, yp1 = p1
        xp2, yp2 = p2
        xp3, yp3 = p3
        a = (1-t)**3
        b = (1-t)**2
        t2 = t**2
        t3 = t**3
        xp0 = a * xp0
        yp0 = a * yp0
        xp1 = 3 * t * b * xp1
        yp1 = 3 * t * b * yp1
        xp2 = 3 * t2 * (1-t) * xp2
        yp2 = 3 * t2 * (1-t) * yp2
        xp3 = t3 * xp3
        yp3 = t3 * yp3
        return (xp0 + xp1 + xp2 + xp3, yp0 + yp1 + yp2 + yp3)

if __name__ == '__main__':
    lista_pontos = []
    Paint()
