import numpy as np
import pylab as py

# Define "x" range.
x = np.linspace(0, 10, 1000)

# Define "T", i.e functions' period.
T = 2
L = T / 2

# "f(x)" function definition.
def f(x): 
    return np.sin((np.pi) * x) + np.sin((2 * np.pi) * x) + np.sin((5 * np.pi) * x)

# "a" coefficient calculation.
def a(n, L, accuracy = 1000):
    a, b = -L, L
    dx = (b - a) / accuracy
    integration = 0
    for x in np.linspace(a, b, accuracy):
        integration += f(x) * np.cos((n * np.pi * x) / L)
    integration *= dx
    return (1 / L) * integration

# "b" coefficient calculation.
def b(n, L, accuracy = 1000):
    a, b = -L, L
    dx = (b - a) / accuracy
    integration = 0
    for x in np.linspace(a, b, accuracy):
        integration += f(x) * np.sin((n * np.pi * x) / L)
    integration *= dx
    return (1 / L) * integration

# Fourier series.
def Sf(x, L, n = 10):
    a0 = a(0, L)
    sum = np.zeros(np.size(x))
    for i in np.arange(1, n + 1):
        sum += ((a(i, L) * np.cos((i * np.pi * x) / L)) + (b(i, L) * np.sin((i * np.pi * x) / L)))
    return (a0 / 2) + sum   

# x axis.
py.plot(x, np.zeros(np.size(x)), color = 'black')

# y axis.
py.plot(np.zeros(np.size(x)), x, color = 'black')

# Original signal.
py.plot(x, f(x), linewidth = 1.5, label = 'Signal')

# Approximation signal (Fourier series coefficients).
py.plot(x, Sf(x, L), '.', color = 'red', linewidth = 1.5, label = 'Fourier series')

# Specify x and y axes limits.
py.xlim([0, 5])
py.ylim([-2.2, 2.2])

py.legend(loc = 'upper right', fontsize = '10')

py.show()