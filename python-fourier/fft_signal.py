import numpy as np
import math
import random
import numpy.fft as fft
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages

dgray = '#0f0f0f'  # цвета фона и графиков
dplot = '#96e6ff'
tplot = '#385057'
splot = '#756325'


def setaxes(a, ttl, alim):
    a.set(xlabel=' ', ylabel=' ', facecolor=dgray)  # заголовок, подписи осей, цвет внутри рамок
    a.set_title(ttl, color='w')
    a.set_ylim(bottom=-alim, top=alim)  # фиксированные пределы по оси y

    a.spines['bottom'].set_color(dgray)  # цвета рамок графика
    a.spines['left'].set_color(dgray)
    a.spines['right'].set_color(dgray)
    a.spines['top'].set_color(dgray)

    a.xaxis.label.set_color('white')  # цвета штрихов на осях и подписей
    a.yaxis.label.set_color('white')
    a.tick_params(axis='x', colors='white')
    a.tick_params(axis='y', colors='white')


def side_seg(a: np.ndarray, n: int) -> np.ndarray:
    sl = len(a)
    res = np.full(sl, 0 + 0j)
    for sc in range(n):
        res[sc] = a[sc]
        if sc > 0:
            res[sl - sc] = a[sl - sc]
    return res


fig, ax = plt.subplots()

signal_length = 48
signal_parts = 6
signal_partl = 8

signal = np.zeros(signal_length)

arg = np.zeros(signal_length)

sdv = np.zeros(signal_length)

for x in range(signal_length):
    sdv[x] = 1.5 * np.pi / 40 * x
    arg[x] = 0.72 * sdv[x] + 0.28 * math.pow(sdv[x], 2)

cdel = 1.5 * np.pi / arg[40]

for x in range(signal_length):
    arg[x] = arg[x] * cdel
    signal[x] = math.sin(arg[x]) + x / 18

for ar_prt in range(signal_parts):
    cf3 = random.uniform(-0.5, 0.5)
    cf2 = random.uniform(-0.6, 0.6)
    cf1 = random.uniform(-0.7, 0.7)
    cf0 = random.uniform(-0.8, 0.8)
    for ar_pos in range(signal_partl):
        i = ar_prt * signal_partl + ar_pos
        x = (i - 24) * 0.064
        signal[i] += cf3 * (x ** 3) + cf2 * (x ** 2) + cf1 * x + cf0

fourir = fft.fft(signal)

plot_indices = [2, 3, 5, 9, 15, 24, 25]
frir_indices = [x - 1 for x in plot_indices]

signal_max = np.amax(signal)
signal_min = np.amin(signal)
fourir_max = np.amax(np.absolute(fourir[frir_indices])) / 24

max_unit_value = max((signal_max - signal_min + 0.8) / 2.7, (2 * fourir_max + 0.8) / 1.8)

print(fourir[plot_indices])
print(max_unit_value)

texwrite = open("aexample.tex", "w")
texwrite.write("    ")
texwrite.close()

figure = plt.figure(facecolor=dgray, figsize=(8.4, 2.7))
axes = figure.subplots()

axes.plot(signal, color=dplot)

setaxes(axes, ("Сигнал длины %d" % signal_length), 2.7 * max_unit_value)

pdf = PdfPages("signal.pdf")
pdf.savefig(figure)
pdf.close()

texwrite = open("aexample.tex", "a")
texwrite.write("\\begin{frame} \\frametitle{\\vspace*{-2.4cm}}\n")
texwrite.write("    \\incg{python-fourier/signal}\n")
texwrite.write("\\end{frame}\n")
texwrite.write("\n")
texwrite.close()


for i in plot_indices:
    figure = plt.figure(facecolor=dgray, figsize=(8.4, 1.8))
    axes = figure.subplots()

    imag_e = [fourir[i - 1] / 24 * np.exp(2 * np.pi * 1j / signal_length * (i - 1) * x) for x in range(signal_length)]

    axes.plot(np.real(imag_e), color=dplot)

    setaxes(axes, ("Волна с частотой 2π ⋅ %d / %d" % (i-1, signal_length)), 1.8 * max_unit_value)

    pdf = PdfPages("waveform-%d.pdf" % i)
    pdf.savefig(figure)
    pdf.close()

    figure = plt.figure(facecolor=dgray, figsize=(8.4, 2.7))
    axes = figure.subplots()

    axes.plot(np.real(fft.ifft(side_seg(fourir, i - 1))), color=tplot)
    axes.plot(np.real(fft.ifft(side_seg(fourir, i))), color=dplot)

    setaxes(axes, ' ', 2.7 * max_unit_value)

    pdf = PdfPages("fourier-%d.pdf" % i)
    pdf.savefig(figure)
    pdf.close()

    texwrite = open("aexample.tex", "a")
    texwrite.write("\\begin{frame} \\frametitle{\\vspace*{-2.4cm}}\n")
    texwrite.write("    \\incg{python-fourier/waveform-%d}\n" % i)
    texwrite.write("\n")
    texwrite.write("    \\incg{python-fourier/fourier-%d}\n" % i)
    texwrite.write("\\end{frame}\n")
    texwrite.write("\n")
    texwrite.close()
