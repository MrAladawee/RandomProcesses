import numpy as np
import matplotlib.pyplot as plt

r = 0.45; sigma = 0.12
x0 = 1; dt = 0.001; n = 200
T0 = [2, 4, 6, 8, 10]
T_max = max(T0)
nt = int(T_max / dt)

def euler_maruyama_approximation(r, sigma, x0, dt, nt):
    """
        Метод Эйлера-Маруямы для аппроксимации стохастического дифференциального уравнения.
        params:
        r, sigma: параметры модели
        x0: начальное значение процесса Ksi(0)
        dt: размер шага по времени (задается 0.001 по условию)
        steps: количество шагов по времени
    """
    X = np.zeros(nt + 1)
    X[0] = x0
    for i in range(1, nt + 1):
        dW = np.random.normal(0, np.sqrt(dt))
        X[i] = X[i - 1] + r * X[i - 1] * dt + sigma * X[i - 1] * dW
    return X

plt.figure(figsize=(10, 5))
for epoch in range(4):
    X = euler_maruyama_approximation(r, sigma, x0, dt, nt)
    plt.plot(np.arange(0, T_max + dt, dt), X)
plt.ylabel('X(t)')
plt.xlabel('t')
plt.title('Траектории $X(t)$')
plt.grid(True)
plt.show()

def monte_carlo(r, sigma, x0, dt, steps, n, T0):
    """
        params:
        r, sigma: параметры модели
        x0: начальное значение процесса Ksi(0)
        dt: размер шага по времени (задается 0.001 по условию)
        steps: количество шагов по времени
        n: количество траекторий
    """
    quantiles = {t0: [] for t0 in T0}
    quantile_values = {}
    quants = [5, 50, 95]

    for _ in range(n):
        X = euler_maruyama_approximation(r, sigma, x0, dt, steps)
        for t0 in T0:
            iteration = int(t0 / dt)
            quantiles[t0].append(X[iteration])

    for t0 in T0:
        quantile_values[t0] = np.percentile(quantiles[t0], quants)
    return quantile_values

quantile = monte_carlo(r, sigma, x0, dt, nt, n, T0)

for t in T0:
    quantile5, quantile50, quantile95 = quantile[t]
    print(f'Время t = {t}:')
    print(f'5% квантиль = {quantile5:.5f},\n'
          f'50% квантиль = {quantile50:.5f},\n'
          f'95% квантиль = {quantile95:.5f}\n')
