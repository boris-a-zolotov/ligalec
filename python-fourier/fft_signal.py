import numpy as np
import math
import random
import numpy.fft as fft
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ────────────────────────────────
# Параметры графики

dgray = '#0f0f0f'  # серый фон 15 / 15 / 15
dplot = '#96e6ff'  # основной яркий график
tplot = '#385057'  # устаревший бледный график

gr_wdth = 8.4  # ширина всех картинок
gs_hght = 2.7  # высота картинок с сигналами
gw_hght = 1.8  # высота картинок с волнами
gr_ofst = 0.2  # поля сверху и снизу


# ────────────────────────────────
# Установка параметров графики

def setaxes(a, ttl, limdn, limup):
    a.set(xlabel=' ', ylabel=' ', facecolor=dgray)  # подписи осей пустые (сегодня только числа)
    a.set_title(ttl, color='w')
    a.set_ylim(bottom=limdn, top=limup)

    a.spines['bottom'].set_color(dgray)  # цвета рамок графика
    a.spines['left'].set_color(dgray)
    a.spines['right'].set_color(dgray)
    a.spines['top'].set_color(dgray)

    a.xaxis.label.set_color('w')  # цвета штрихов на осях и подписей
    a.yaxis.label.set_color('w')
    a.tick_params(axis='x', colors='w')
    a.tick_params(axis='y', colors='w')


# ────────────────────────────────
# Удаление высоких частот (середины массива)
# 0 — оставляет в начале пустой сегмент
# 1 — оставляет в начале сегмент [0]

def side_seg(a: np.ndarray, n: int) -> np.ndarray:
    sl = len(a)
    res = np.full(sl, 0 + 0j)  # иначе real / complex warning
    for sc in range(n):
        res[sc] = a[sc]
        if sc > 0:
            res[sl - sc] = a[sl - sc]
    return res


# ────────────────────────────────
# Глобальные параметры: длина сигнала,
# разбиение на части

signal_length = 48
signal_parts = 6
signal_partl = 8

signal = np.zeros(signal_length)
arg = np.zeros(signal_length)
sdv = np.zeros(signal_length)

# ────────────────────────────────
# Заполнение сигнала

for x in range(signal_length):
    sdv[x] = 1.5 * np.pi / 40 * x  # хочу, чтобы влезло ровно столько синуса
    arg[x] = 0.72 * sdv[x] + 0.28 * math.pow(sdv[x], 2)
    # в конце аргумент синуса будет двигаться быстрее, чем в начале

cdel = 1.5 * np.pi / arg[40]  # нормализация аргумента, а то квадрат всё пошевелил

for x in range(signal_length):
    arg[x] = arg[x] * cdel
    signal[x] = 1.2 * math.sin(arg[x]) + x / 18
    # слегка возрастающий сдвинутый сжатый к концу синус

for ar_prt in range(signal_parts):  # добавление на кусках сигнала случайного многочлена
    cf3 = random.uniform(-0.5, 0.5)
    cf2 = random.uniform(-0.6, 0.6)
    cf1 = random.uniform(-0.7, 0.7)
    cf0 = random.uniform(-1.2, 1.2)
    for ar_pos in range(signal_partl):
        i = ar_prt * signal_partl + ar_pos
        x = (i - 24) * 0.064
        signal[i] += cf3 * (x ** 3) + cf2 * (x ** 2) + cf1 * x + cf0

fourir = fft.fft(signal)  # преобразование Фурье сигнала; теперь оно и сигнал не меняются

# ────────────────────────────────
# Определение границ изображения

plot_indices = [2, 3, 5, 9, 15, 24, 25]
frir_indices = [x - 1 for x in plot_indices]

signal_max = np.amax(signal)
signal_min = np.amin(signal)
fourir_max = np.amax(np.absolute(fourir[frir_indices])) / signal_length * 2
# делить, потому что формула. *2, потому что рисуем вклад двух симметричных волн

signal_by_cm = (signal_max - signal_min + 2 * gr_ofst) / gs_hght
fourir_by_cm = (2 * fourir_max + 2 * gr_ofst) / gw_hght

max_unit_value = max(signal_by_cm, fourir_by_cm)

signal_limdn = (signal_min - gr_ofst) * max_unit_value / signal_by_cm
signal_limup = (signal_max + gr_ofst) * max_unit_value / signal_by_cm
fourir_lim = (fourir_max + gr_ofst) * max_unit_value / fourir_by_cm
# ужать тот график, который закладывает меньшую разницу значений в отрезок 1 см

print(max_unit_value)  # проверка, что пределы по оси $y$ не безумно большие

# ────────────────────────────────
# Рисуем и пишем

if True:
    texwrite = open("aexample.tex", "w")
    texwrite.write("\n")
    texwrite.close()

figure = plt.figure(facecolor=dgray, figsize=(gr_wdth, gs_hght))
axes = figure.subplots()
axes.plot(signal, color=dplot)

setaxes(axes, ("Сигнал длины %d" % signal_length), signal_limdn, signal_limup)
pdf = PdfPages("signal.pdf")
pdf.savefig(figure)
pdf.close()

if True:
    texwrite = open("aexample.tex", "a")
    texwrite.write("\\begin{frame} \\frametitle{\\vspace*{-2.4cm}}\n")
    texwrite.write("    \\incg{python-fourier/signal}\n")
    texwrite.write("\\end{frame}\n")
    texwrite.write("\n")
    texwrite.close()

# ────────────────────────────────
# Главный цикл по графикам

for i in plot_indices:
    # Слагаемое, которое пойдёт в сумму (ifft, два симметричных)
    imag_e = [fourir[i - 1] / signal_length * 2 *
              np.exp(2 * np.pi * 1j / signal_length * (i - 1) * x)
              for x in range(signal_length)]

    figure = plt.figure(facecolor=dgray, figsize=(gr_wdth, gw_hght))
    axes = figure.subplots()
    axes.plot(np.zeros(signal_length), color=tplot)
    axes.plot(np.real(imag_e), color=dplot)

    setaxes(axes, ("Волна с частотой 2π ⋅ %d / %d" % (i - 1, signal_length)), -fourir_lim, fourir_lim)
    pdf = PdfPages("waveform-%d.pdf" % i)
    pdf.savefig(figure)
    pdf.close()

    figure = plt.figure(facecolor=dgray, figsize=(gr_wdth, gs_hght))
    axes = figure.subplots()  # side_seg подобраны так, чтобы разность была i–1-ой частотой
    axes.plot(np.real(fft.ifft(side_seg(fourir, i - 1))), color=tplot)
    axes.plot(np.real(fft.ifft(side_seg(fourir, i))), color=dplot)

    setaxes(axes, ' ', signal_limdn, signal_limup)
    pdf = PdfPages("fourier-%d.pdf" % i)
    pdf.savefig(figure)
    pdf.close()

    if True:
        texwrite = open("aexample.tex", "a")
        texwrite.write("\\begin{frame} \\frametitle{\\vspace*{-2.4cm}}\n")
        texwrite.write("    \\incg{python-fourier/waveform-%d}\n" % i)
        texwrite.write("\n")
        texwrite.write("    \\incg{python-fourier/fourier-%d}\n" % i)
        texwrite.write("\\end{frame}\n")
        texwrite.write("\n")
        texwrite.close()
