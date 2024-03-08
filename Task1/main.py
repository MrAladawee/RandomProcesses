import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram

data = pd.read_csv('2.csv', header=None,skiprows=1)
data.columns = ['t', 'xi']
data['xi'] = data['xi'].astype(float)
frequencies, spectrum = periodogram(data['xi'])

sorted_indices = np.argsort(spectrum)[::-1]
most_significant_freqs = frequencies[sorted_indices[:2]]
frequencies, spectrum = periodogram(data['xi'])
sorted_indices = np.argsort(spectrum)[::-1]
periods = 1 / most_significant_freqs
total_amplitude_sum = np.sum(spectrum[1:])
amplitude_ratios = spectrum[sorted_indices[:2]] / total_amplitude_sum

most_significant_freq = most_significant_freqs[0]
seasonal_component = np.sin(2 * np.pi * most_significant_freq * data['t'])

n = len(data['xi'])

def aj(j):
    n = len(data['xi'])
    s = 0
    for i in range(n):
        s += data['xi'][i] * math.cos(2 * math.pi * j * i / n)
    return s * 2/n

def bj(j):
    n = len(data['xi'])
    s = 0
    for i in range(n):
        s += data['xi'][i] * math.sin(2 * math.pi * j * i / n)
    return s * 2/n

def P(j):
    return math.pow(aj(j), 2) + math.pow(bj(j), 2)

# Создание массива значений j от 1 до n
j_values = np.arange(1, (n//2)+1)

# Вычисление значений периодограммы P(j) для каждого j
P_values = [P(j) for j in j_values]

# Найдем индексы максимальных значений периодограммы
max_indices = sorted(range(len(P_values)), key=lambda i: P_values[i], reverse=True)

# Найдем два максимальных пика, учитывая условие о точках слева и справа
peak_coordinates = []
for idx in max_indices:
    if idx > 0 and idx < len(P_values) - 1:
        if P_values[idx] > P_values[idx-1] and P_values[idx] > P_values[idx+1]:
            peak_coordinates.append(j_values[idx])
    if len(peak_coordinates) == 2:
        break

# Построение графика периодограммы
plt.figure(figsize=(10, 6))
plt.plot(j_values, P_values, color='b', linestyle='-')
plt.xlabel('j')
plt.ylabel('P(j)')
plt.title('Периодограмма')
plt.grid(True)
plt.show()

def seas():
    rez = []
    n = len(data['xi'])
    for t in data['t']:
        s = 0
        for j in [peak_coordinates[0], peak_coordinates[1]]:
            s += aj(j)*math.cos(2*math.pi*j*t/n)+bj(j)*math.sin(2*math.pi*j*t/n)
        rez.append(s)
    return rez

# Построение сезонной компоненты
plt.figure(figsize=(14, 8))
plt.plot(data['t'], data['xi'], label='Исходная выборочная траектория')
plt.plot(data['t'], seas(), label='Найденная сезонная компонента', linestyle='--')
plt.xlabel('Время')
plt.ylabel('Значение')
plt.title('Сравнение исходной выборочной траектории и сезонной компоненты')
plt.legend()
plt.grid(True)
plt.show()

print("Самые существенные сезонные компоненты:", peak_coordinates[0], peak_coordinates[1])
print("Период:", periods)
print("Доля амплитуды", amplitude_ratios)
