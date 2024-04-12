import numpy as np
import matplotlib.pyplot as plt


N = 1000
alpha = 0.01
lambda_rate = 16.4
theta = 1 / 6.0

"""
Генерирует времена прихода заявок на основе экспоненциального распределения (пуассоновский процесс).
tau хранит текущее время, и заявки генерируются до тех пор, пока время не превысит заданный лимит time_limit (8 часов).
"""
def simulate_requests(lambda_rate, time_limit):
    tau = 0
    taus = []
    while tau <= time_limit:
        tau += np.random.exponential(1 / lambda_rate)
        if tau <= time_limit:
            taus.append(tau)
    return taus


"""
Вычисляет максимальное количество одновременно активных заявок в течение рабочего дня.
T представляет собой массив временных точек для анализа.
active_requests считает, сколько заявок активно в каждый момент времени t.
"""
def count_active_requests(taus, gammas):
    T = np.linspace(0, max(taus), num=100)
    max_active = 0
    for t in T:
        active_requests = sum((t >= taus[j]) and (t <= taus[j] + gammas[j]) for j in range(len(taus)))
        if active_requests > max_active:
            max_active = active_requests
    return max_active


"""
Запускает метод Монте-Карло, генерируя наборы времен прихода заявок (taus) и времен их обработки (gammas) для каждой
итерации.
Qs хранит максимальное количество активных заявок для каждой итерации.
"""
Qs = []
for i in range(N):
    taus = simulate_requests(lambda_rate, 8)
    gammas = np.random.exponential(theta, size=len(taus))
    Qs.append(count_active_requests(taus, gammas))


"""
Сортирует Qs для удобства расчета.
Вычисляет вероятности превышения для каждого значения s от 0 до максимально наблюдаемого.
Определяет минимальное значение s, при котором вероятность не превышает заданного уровня alpha.
"""
Qs.sort(reverse=True)
s_values = []
probabilities = []
s_min = 0
for s in range(max(Qs) + 1):
    probability = sum(q > s for q in Qs) / N
    probabilities.append(probability)
    s_values.append(s)
    if probability <= alpha:
        s_min = s
        break


plt.figure(figsize=(10, 6))
plt.plot(s_values, probabilities, marker='o', linestyle='-', color='b')
plt.axhline(y=alpha, color='gray', linestyle='--')
plt.axvline(x=s_min, color='g', linestyle='--')
plt.title('Probability of Exceeding Number of Active Requests')
plt.xlabel('Number of Service Units (s)')
plt.ylabel('Probability of Exceeding s')
plt.grid(True)
plt.show()

print(f"Минимальное количество обслуживающих элементов s: {s_min}")
