import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Настройки графиков


ax = plt.axes()

ax.set(xlabel="Month",
       ylabel="Precipitation\n(inches)",
       facecolor="#0f0f0f")

ax.set_title("Ковидные бляди", color='w')

ax.spines['bottom'].set_color("#0f0f0f")
ax.spines['left'].set_color("#0f0f0f")
ax.spines['right'].set_color("#0f0f0f")
ax.spines['top'].set_color("#0f0f0f")

ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')


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

axes1.plot(res[4:8], color='w')

pdf1 = PdfPages("Figures.pdf")
pdf1.savefig(figure1)
pdf1.close()
