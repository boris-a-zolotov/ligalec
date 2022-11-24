import numpy as np
import scipy as scp
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dgray = '#0f0f0f'  # цвета фона и графиков
dplot = '#96e6ff'
tplot = '#385057'


def setaxes(a, ttl, xl, yl):
    a.set(xlabel=xl, ylabel=yl, facecolor=dgray)  # заголовок, подписи осей, цвет внутри рамок
    a.set_title(ttl, color='w')
    a.set_ylim(bottom=0, top=5.95)  # фиксированные пределы по оси y

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
    return arr / npsum / dx


def copyfc(x: np.ndarray) -> np.ndarray:
    copylen = len(x)
    retarray = np.zeros(copylen, dtype=float)
    for cyci in range(copylen):
        retarray[cyci] = x[cyci]
    return retarray


# Мы считаем длины образца и ядра нечётными, чтобы ноль был нулём

sampleSemilength = 2000
kernelSemilength = 1000
dx = 1 / 250  # вес одного элемента массива

func = np.zeros(2 * sampleSemilength - 1, dtype=float)

for i in range(2 * sampleSemilength - 1):
    func[i] = i % 300


def normalkernel(s: float) -> np.ndarray:
    kernl = np.zeros(2 * kernelSemilength - 1, dtype=float)
    for st in range(kernelSemilength):
        kernl[kernelSemilength - 1 - st] = math.exp(-0.5 * (st * dx / s) ** 2)
        kernl[kernelSemilength - 1 + st] = math.exp(-0.5 * (st * dx / s) ** 2)
    kernl = unitalize(kernl)
    return kernl


kernel = normalkernel(0.2)

lbls = range(2 * sampleSemilength - 1)
lbls = [(x - sampleSemilength + 1) * dx for x in lbls]

lblsKern = range(2 * kernelSemilength - 1)
lblsKern = [(x - kernelSemilength + 1) * dx for x in lblsKern]

# plt.plot(lblsKern, kernel)

# plt.show()

# plotnumber = 0  # для нумерации файлов

# outarray = [[0, copyfc(func), 1]]


rest = scp.signal.fftconvolve(func, kernel) * dx
rest = rest[kernelSemilength - 1:-1 * kernelSemilength + 1]

plt.plot(lbls, func)
plt.plot(lbls, rest)

plt.show()

# for s in outarray:
#     figure = plt.figure(facecolor=dgray, figsize=(8.2, 4.1))
#     axes = figure.subplots()
#
#     for k in range(s[0]):
#         axes.plot(lbls, outarray[k][1], color=tplot)
#
#     axes.plot(lbls, outarray[s[0]][1], color=dplot)
#
#     setaxes(axes, ("f^(*%d)" % (s[2])), ' ', ' ')
#
#     pdf = PdfPages("probability-%d.pdf" % (s[0]))
#     pdf.savefig(figure)
#     pdf.close()
