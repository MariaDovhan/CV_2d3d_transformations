from graphics import *
import time
import numpy as np
import math as mt

# створення вікна, задання розміру фігури та зміщення
xw = 600; yw = 600; st1 = 40; st2 = 60
win = GraphWin("2-D переміщення", xw, yw)
win.setBackground('white')
dx = 50; dy = 50
x1 = xw - 10
y1 = 10
x2 = x1 - st1
y2 = y1 + st2

# відображення першої фігури та її переміщення
obj = Rectangle(Point(x1, y1), Point(x2, y2))
obj.draw(win)
ii = mt.floor(xw/dx) - 1
for i in range(1, ii):
    time.sleep(0.3)
    x1 = x1 - dx
    y1 = y1 + dy
    x2 = x2 - dx
    y2 = y2 + dy
    obj = Rectangle(Point(x1, y1), Point(x2, y2))
    obj.draw(win)
win.getMouse()
win.close()

# обертання + переміщення
win = GraphWin("2-D обертання+масштабування", xw, yw)
win.setBackground('white')

# координати центра і прямокутника в центрі
xc = xw / 2; yc = yw / 2
x1 = xc - st1/2; y1 = yc - st2/2
x2 = x1 + st1; y2 = y1
x3 = x2; y3 = y1 + st2
x4 = x1; y4 = y3

obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
obj.draw(win)

# матриця перетворень
TetaR = mt.radians(60)
fp = np.array([[1.15*mt.cos(TetaR), -1.15*mt.sin(TetaR), 0], [1.15*mt.sin(TetaR), 1.15*mt.cos(TetaR), 0], [0, 0, 1]])
ftp = fp.T

R0 = mt.sqrt((st1 / 2) ** 2 + (st2 / 2) ** 2)
ii = int(mt.log((xw/2-10)/R0)/mt.log(1.15))

for i in range(ii):
    time.sleep(0.3)

    # нові координати шляхом множення матриць
    a1p = np.array([[x1 - xc, y1 - yc, 1]])
    total1p = a1p.dot(ftp)
    x1 = total1p[0, 0] + xc;  y1=total1p[0, 1] + yc

    a2p = np.array([[x2 - xc, y2 - yc, 1]])
    total2p = a2p.dot(ftp)
    x2 = total2p[0, 0] + xc;  y2 = total2p[0, 1] + yc

    a3p = np.array([[x3 - xc, y3 - yc, 1]])
    total3p = a3p.dot(ftp)
    x3 = total3p[0, 0] + xc;  y3 = total3p[0, 1] + yc

    a4p = np.array([[x4 - xc, y4 - yc, 1]])
    total4p = a4p.dot(ftp)
    x4 = total4p[0, 0] + xc;  y4 = total4p[0, 1] + yc

    obj = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
    obj.draw(win)

win.getMouse()
win.close()
