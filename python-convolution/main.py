import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# Настройки графиков

def setcolors(a):
    a.set(xlabel="Month",
           ylabel="Precipitation\n(inches)",
           facecolor="#0f0f0f")

    a.set_title("Ковидные бляди", color='w')

    a.spines['bottom'].set_color("#0f0f0f")
    a.spines['left'].set_color("#0f0f0f")
    a.spines['right'].set_color("#0f0f0f")
    a.spines['top'].set_color("#0f0f0f")

    a.xaxis.label.set_color('white')
    a.yaxis.label.set_color('white')
    a.tick_params(axis='x', colors='white')
    a.tick_params(axis='y', colors='white')


# ax.set_facecolor("#0f0f0f")

# plt.ylabel(" ")

def unitalize(arr: np.ndarray) -> np.ndarray:
    npsum = np.sum(arr)
    return arr / npsum


days = [7, 7, 7, 1, 1, 1, 1]

kernel = [0, 0, 1, 1, 1]

kernel = unitalize(kernel)

res = scp.signal.fftconvolve(days, kernel)

figure1 = plt.figure(facecolor="#0f0f0f")

axes1 = figure1.subplots()

setcolors(axes1)

axes1.plot(res[4:8], color='w')

pdf1 = PdfPages("Figures.pdf")
pdf1.savefig(figure1)
pdf1.close()
