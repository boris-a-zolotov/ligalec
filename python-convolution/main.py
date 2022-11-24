import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dgray = '#0f0f0f'  # цвета фона и графиков
dplot = '#96e6ff'


def setaxes(a, ttl, xl, yl):
    a.set(xlabel=xl, ylabel=yl, facecolor=dgray)  # заголовок, подписи осей, цвет внутри рамок
    a.set_title(ttl, color='w')
    a.set_ylim(bottom=0)  # фиксированный низ оси y — на нуле

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


sampleSemilength = 900
kernelSemilength = 100
dx = 1 / 200  # вес одного элемента массива

func = np.zeros(2 * sampleSemilength - 1, dtype=float)

for i in range(kernelSemilength):
    func[sampleSemilength - 1 - i] = 1
    func[sampleSemilength - 1 + i] = 1

func = unitalize(func)

kernel = np.full(2 * kernelSemilength - 1, 1, dtype=float)

kernel = unitalize(kernel)

lbls = range(2 * sampleSemilength - 1)
lbls = [(x - sampleSemilength + 1) * dx for x in lbls]

plt.plot(lbls, func)

func = scp.signal.fftconvolve(func, kernel) * dx

func = func[kernelSemilength - 1:-1 * kernelSemilength + 1]

func = scp.signal.fftconvolve(func, kernel) * dx

func = func[kernelSemilength - 1:-1 * kernelSemilength + 1]

func = scp.signal.fftconvolve(func, kernel) * dx

func = func[kernelSemilength - 1:-1 * kernelSemilength + 1]

plt.plot(lbls, func)

plt.show()

# print(lbls)

# wavg = scp.signal.fftconvolve(days, kernel)


# outarray = [[0, days[6:], dplot, 'Заболеваемость: сырые данные'],
#             [1, wavg[6:-6], '#ebaf9b', 'Заболеваемость: недельное среднее'],
#             [2, samp[6:], '#73f587', 'Недельное среднее и тренд']]
#
# for s in outarray:
#     figure = plt.figure(facecolor=dgray, figsize=(8.2, 4.1))
#     axes = figure.subplots()
#
#     for k in range(s[0] + 1):
#         axes.plot(outarray[k][1], color=outarray[k][2])
#
#     setaxes(axes, s[3], 'дни', 'значения')
#
#     pdf = PdfPages("covid-%d.pdf" % (s[0]))
#     pdf.savefig(figure)
#     pdf.close()
