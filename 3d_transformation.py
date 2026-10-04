from graphics import *
import numpy as np
import math as mt

#---------------------------------- координати паралелепіпеда ------------------------------------
xw = 600; yw = 600; 
length = 350
width = 300
height = 200
Prlpd = np.array([ [0, 0, 0, 1],
                  [length, 0, 0, 1],
                  [length, width, 0, 1],
                  [0, width, 0, 1],
                  [0, 0, height, 1],
                  [length, 0, height, 1],
                  [length, width, height, 1],
                  [0, width, height, 1]])
print('enter matrix')
print(Prlpd)

def ShiftXYZ (Figure, l, m, n):
   f = np.array([ [1, 0, 0, l], [0, 1, 0, m], [0, 0, 1, n], [0, 0, 0, 1] ])
   Prxy = Figure.dot(f.T)
   print('зміщення')
   print(Prxy)
   return Prxy

def rotateX (Figure, TetaG):
    TetaR = mt.radians(TetaG)
    f = np.array([ [1, 0, 0, 0], [0, mt.cos(TetaR), -mt.sin(TetaR), 0], [0, mt.sin(TetaR),  mt.cos(TetaR), 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    print('обертання коло х')
    print(Prxy)
    return Prxy

def rotateY (Figure, TetaG):
    TetaR = mt.radians(TetaG)
    f = np.array([ [mt.cos(TetaR), 0, mt.sin(TetaR), 0], [0, 1, 0, 0], [-mt.sin(TetaR), 0, mt.cos(TetaR), 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)
    print('обертання коло y')
    print(Prxy)
    return Prxy

currentFigures = []

def clearScreen():
    global currentFigures

    for fig in currentFigures:
        fig.undraw()
    currentFigures = []

COLORS_SET = [['#fff3cc', '#ffe799', '#ffdb66'],
              ['#ffcceb', '#ff99d6', '#ff66c2'],
              ['#ccdfff', '#99beff', '#669eff']]

def PrlpdWiz(Prxy, shades):
    clearScreen()

    xs = Prxy[:, 0]
    ys = Prxy[:, 1]

    def sort_quad(indices):
        by_x = sorted(indices, key=lambda i: Prxy[i, 0])
        left_sorted = sorted(by_x[:2], key=lambda i: Prxy[i, 1])
        right_sorted = sorted(by_x[2:], key=lambda i: Prxy[i, 1], reverse=True)
        ordered = [
            left_sorted[0],
            left_sorted[1],
            right_sorted[0],
            right_sorted[1],
        ]
        return [Point(Prxy[i, 0], Prxy[i, 1]) for i in ordered]

    sorted_y_indices = np.argsort(ys)
    top_indices = sorted_y_indices[:4]
    p_lowest_1 = sorted_y_indices[-1]
    p_lowest_2 = sorted_y_indices[-2]

    if round(ys[p_lowest_1]) == round(ys[p_lowest_2]):
        bottom_front = sorted_y_indices[-2:]
        top_front = sorted_y_indices[-6:-4]
        front_face_idx = list(bottom_front) + list(top_front)
                
        poly_front = Polygon(*sort_quad(front_face_idx))
        poly_front.setFill(shades[1])
        poly_front.setOutline("black")
        poly_front.draw(win)
        currentFigures.append(poly_front)
    else:
        idx_max_y = np.argmax(ys)
        ref_x = xs[idx_max_y]

        front_edge_indices = set(np.argsort(np.abs(xs - ref_x))[:2])
        right_edge_indices = set(np.argsort(xs)[-2:])
        left_edge_indices = set(np.argsort(xs)[:2])

        right_face_idx = list(front_edge_indices | right_edge_indices)
        left_face_idx = list(front_edge_indices | left_edge_indices)

        if len(right_face_idx) == 4:
            poly_right = Polygon(*sort_quad(right_face_idx))
            poly_right.setFill(shades[1])
            poly_right.setOutline("black")
            poly_right.draw(win)
            currentFigures.append(poly_right)

        if len(left_face_idx) == 4:
            poly_left = Polygon(*sort_quad(left_face_idx))
            poly_left.setFill(shades[2])
            poly_left.setOutline("black")
            poly_left.draw(win)
            currentFigures.append(poly_left)

    top_indices = np.argsort(ys)[:4]
    poly_top = Polygon(*sort_quad(top_indices))
    poly_top.setFill(shades[0])
    poly_top.setOutline("black")
    poly_top.draw(win)
    currentFigures.append(poly_top)

win = GraphWin("3-D модель паралелепіпеда оберт коло Х аксонометрічна проекція на ХУ", xw, yw)
win.setBackground('white')
ThetaX = 30
l = length / 2; m = width / 2; n = height / 2
shiftedPrlpd = ShiftXYZ(Prlpd, -l, -m, -n)

VISIBLE_DURATION = 3
HIDDEN_DURATION = 1

is_visible = True
phase_end = time.time() + VISIBLE_DURATION
ThetaY = 0
color_schema = 0

while True:
    if win.checkMouse() is not None:
        break

    if time.time() > phase_end:
        is_visible = not is_visible
        phase_end = time.time() + (VISIBLE_DURATION if is_visible else HIDDEN_DURATION)
        color_schema = (color_schema + 1) % len(COLORS_SET)

    ThetaY = (ThetaY + 10) % 360

    if is_visible:
        rotatedYPrlpd = rotateY(shiftedPrlpd, ThetaY)
        rotatedXPrlpd = rotateX(rotatedYPrlpd, ThetaX)
        centeredPrlpd = ShiftXYZ(rotatedXPrlpd, xw/2, yw/2, 0)
        PrlpdWiz(centeredPrlpd, COLORS_SET[color_schema])
    else:
        clearScreen()
        
    time.sleep(0.05)

win.close()