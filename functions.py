import pygame as pg
pg.init()


def text(font, txt, color):
    font = font.render(txt, 1, color)
    return font, font.get_width(), font.get_height()


def text_down(txt, font, width):
    textr = []
    pointer = 0
    l = len(txt)
    while pointer < l:
        a = ""
        while text(font, a, 0, )[1] < width:
            a += txt[pointer]
            pointer += 1
            if pointer == l:
                break
        if pointer != l or text(font, a, 0, )[1] >= width:
            a = a[:-1]
            pointer -= 1
        textr.append(a)
    return textr
import math
import random

def random_unit_vector():
    angle = random.uniform(0, 2 * math.pi)
    return math.cos(angle), math.sin(angle)


def normalised_vec(start,end):
    if start==end:
        return [0,0]
    res=[end[0]-start[0],end[1]-start[1]]
    c=(res[0]**2+res[1]**2)**(1/2)
    res[0]/=c
    res[1]/=c

    return res

def pitagolas(start,end):
    return (start[0]-end[0])**2+(start[1]-end[1])**2
def pidarolas(start,end):
    return ((start[0]-end[0])**2+(start[1]-end[1])**2)**0.5