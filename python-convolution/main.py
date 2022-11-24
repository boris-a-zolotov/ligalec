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
    return arr / npsum


pandDuration = 105

days = np.zeros(pandDuration, dtype=float)
samp = np.zeros(pandDuration, dtype=float)

for x in range(pandDuration):
    days[x] = 2500 + 1000 * np.arctan(0.08 * (x - 75))
    samp[x] = 2500 + 1000 * np.arctan(0.08 * (x - 75))

for w in range(pandDuration // 7):
    defic = days[7 * w + 2] - 400
    days[7 * w + 2] = 400
    days[7 * w + 3] += defic / 2
    days[7 * w + 4] += defic * 0.4
    days[7 * w + 5] += defic / 10

for x in range(pandDuration):
    days[x] += max(np.random.normal(0, 400), -1 * days[x])

kernel = np.full(7, 1, dtype=float)

kernel = unitalize(kernel)

wavg = scp.signal.fftconvolve(days, kernel)


outarray = [[0, days[6:], dplot, 'Заболеваемость: сырые данные'],
            [1, wavg[6:-6], '#ebaf9b', 'Заболеваемость: недельное среднее'],
            [2, samp[6:], '#73f587', 'Недельное среднее и тренд']]

for s in outarray:
    figure = plt.figure(facecolor=dgray, figsize=(8.2, 4.1))
    axes = figure.subplots()

    for k in range(s[0] + 1):
        axes.plot(outarray[k][1], color=outarray[k][2])

    setaxes(axes, s[3], 'дни', 'значения')

    pdf = PdfPages("covid-%d.pdf" % (s[0]))
    pdf.savefig(figure)
    pdf.close()
