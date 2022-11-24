import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dgray = '#0f0f0f'  # цвета фона и графиков
dplot = '#96e6ff'


def setaxes(a, ttl, xl, yl):
    a.set(xlabel=xl, ylabel=yl, facecolor=dgray)  # заголовок, подписи осей, цвет внутри рамок
    a.set_title(ttl, color='w')

    a.spines['bottom'].set_color(dgray)  # цвета рамок графика
    a.spines['left'].set_color(dgray)
    a.spines['right'].set_color(dgray)
    a.spines['top'].set_color(dgray)

    a.xaxis.label.set_color('white')  # цвета штрихов на осях и подписей
    a.yaxis.label.set_color('white')
    a.tick_params(axis='x', colors='white')
    a.tick_params(axis='y', colors='white')


def unitalize(arr: np.ndarray) -> np.ndarray:  # сделать массив с суммой эл-тов = 1
    npsum = np.sum(arr)
    return arr / npsum


days = [7, 7, 7, 1, 1, 1, 1]

kernel = [0, 0, 1, 1, 1]

kernel = unitalize(kernel)

res = scp.signal.fftconvolve(days, kernel)

figure1 = plt.figure(facecolor=dgray, figsize=(8.2, 4.1))

axes1 = figure1.subplots()

setaxes(axes1, 'ковид', 'дни', 'значения')

axes1.plot(res[4:8], color=dplot)

pdf1 = PdfPages("Figures.pdf")
pdf1.savefig(figure1)
pdf1.close()
