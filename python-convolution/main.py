import numpy as np
import scipy as scp
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


sampleSemilength = 1600
kernelSemilength = 1000
dx = 1 / 2000  # вес одного элемента массива

func = np.zeros(2 * sampleSemilength - 1, dtype=float)

for i in range(kernelSemilength):
    func[sampleSemilength - 1 - i] = 1
    func[sampleSemilength - 1 + i] = 1

func = unitalize(func)

kernel = np.full(2 * kernelSemilength - 1, 1, dtype=float)

kernel = unitalize(kernel)

lbls = range(2 * sampleSemilength - 1)
lbls = [(x - sampleSemilength + 1) * dx for x in lbls]

plotnumber = 0

outarray = [[0, copyfc(func), 1]]

for i in [t + 1 for t in range(15)]:
    funcst = 1

    while ((i + 1) * funcst / i <= sampleSemilength - 1):
        funck = (i + 1) * funcst // i
        func[sampleSemilength - 1 + funcst] = func[sampleSemilength - 1 + funck]
        func[sampleSemilength - 1 - funcst] = func[sampleSemilength - 1 - funck]
        funcst += 1

    while (funcst <= sampleSemilength - 1):
        func[sampleSemilength - 1 + funcst] = 0
        func[sampleSemilength - 1 - funcst] = 0
        funcst += 1
    func = unitalize(func)

    st = 1
    while ((i + 1) * st / i <= kernelSemilength - 1):
        k = (i + 1) * st // i
        kernel[kernelSemilength - 1 + st] = kernel[kernelSemilength - 1 + k]
        kernel[kernelSemilength - 1 - st] = kernel[kernelSemilength - 1 - k]
        st += 1
    while (st <= kernelSemilength - 1):
        kernel[kernelSemilength - 1 + st] = 0
        kernel[kernelSemilength - 1 - st] = 0
        st += 1
    kernel = unitalize(kernel)

    func = scp.signal.fftconvolve(func, kernel) * dx
    func = func[kernelSemilength - 1:-1 * kernelSemilength + 1]
    if (i % 3 == 0):
        plotnumber += 1
        outarray += [[plotnumber, copyfc(func), i]]

for s in outarray:
    figure = plt.figure(facecolor=dgray, figsize=(8.2, 4.1))
    axes = figure.subplots()

    for k in range(s[0]):
        axes.plot(lbls, outarray[k][1], color=tplot)

    axes.plot(lbls, outarray[s[0]][1], color=dplot)

    setaxes(axes, ("f^(*%d)" % (s[2])), ' ', ' ')

    pdf = PdfPages("probability-%d.pdf" % (s[0]))
    pdf.savefig(figure)
    pdf.close()
