import numpy as np
import scipy as scp
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dgray = '#0f0f0f'
dplot = '#96e6ff'
tplot = '#385057'


def setaxes(a, ttl, xl, yl):
    a.set(xlabel=xl, ylabel=yl, facecolor=dgray)
    a.set_title(ttl, color='w')
    # a.set_ylim(bottom=0, top=10)  пределов по оси y на этот раз нет

    a.spines['bottom'].set_color(dgray)
    a.spines['left'].set_color(dgray)
    a.spines['right'].set_color(dgray)
    a.spines['top'].set_color(dgray)

    a.xaxis.label.set_color('white')
    a.yaxis.label.set_color(dgray)
    a.tick_params(axis='x', colors='white')
    a.tick_params(axis='y', colors=dgray)


def unitalize(arr: np.ndarray) -> np.ndarray:  # сделать массив с суммой эл-тов = 1
    npsum = np.sum(arr)
    return arr / npsum / dx


def copyfc(x: np.ndarray) -> np.ndarray:  # скопировать массив, чтобы не оказалось,
    # что мы храним ссылку
    copylen = len(x)
    retarray = np.zeros(copylen, dtype=float)
    for cyci in range(copylen):
        retarray[cyci] = x[cyci]
    return retarray


# ────────
# Инициализация массивов

sampleSemilength = 2000
kernelSemilength = 1000
dx = 1 / 250  # вес одного элемента массива

func = np.zeros(2 * sampleSemilength - 1, dtype=float)

lbls = range(2 * sampleSemilength - 1)  # значения на числовой оси, отсчитываемся от них
lbls = [(x - sampleSemilength + 1) * dx for x in lbls]


# ────────
# Нормальное распределение, умножаем на dx, чтобы дисперсия
# не была супер-маленькой

def normalkernel(s: float) -> np.ndarray:
    kernl = np.zeros(2 * kernelSemilength - 1, dtype=float)
    for st in range(kernelSemilength):
        kernl[kernelSemilength - 1 - st] = math.exp(-0.5 * (st * dx / s) ** 2)
        kernl[kernelSemilength - 1 + st] = math.exp(-0.5 * (st * dx / s) ** 2)
    kernl = unitalize(kernl)
    return kernl


# ────────
# Заполняем исходную функцию по кусочкам случайными многочленами

for i in range(2 * sampleSemilength - 1):
    if i % 300 == 0:
        cf3 = random.uniform(-4, 4)
        cf2 = random.uniform(-12, 12)
        cf1 = random.uniform(-200, 200)
        cf0 = random.uniform(-720, 720)
    vx = lbls[i]
    func[i] = cf3 * (vx ** 3) + cf2 * (vx ** 2) + cf1 * vx + cf0

# ────────
# График исходной функции без приближений

figure = plt.figure(facecolor=dgray, figsize=(8.2, 4.1))
axes = figure.subplots()

axes.plot(lbls, func, color=dplot)

setaxes(axes, "Очень негладкая функция", ' ', ' ')

pdf = PdfPages("smoothing-0.pdf")
pdf.savefig(figure)
pdf.close()

# ────────
# Графики для нескольких значений дисперсии

for sigma in [2, 1, 0.5, 0.2, 0.05]:
    figure = plt.figure(facecolor=dgray, figsize=(8.2, 4.1))
    axes = figure.subplots()

    kernel = normalkernel(sigma)

    rest = scp.signal.fftconvolve(func, kernel) * dx
    rest = rest[kernelSemilength - 1:-1 * kernelSemilength + 1]
    # Магически подобранный сдвиг индексов

    axes.plot(lbls, func, color=tplot)
    axes.plot(lbls, rest, color=dplot)

    setaxes(axes, ("σ = %.2f" % sigma), ' ', ' ')

    pdf = PdfPages("smoothing-%.2f.pdf" % sigma)
    pdf.savefig(figure)
    pdf.close()
