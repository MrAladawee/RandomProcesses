import pandas as pd
import numpy as np

gamma = 0.01

data = pd.read_csv('links.csv')

# Группировка данных по столбцу 'from' и преобразование в словарь
waves = data.groupby('from')['to'].apply(list).to_dict()

# Вывод словаря
print(waves)
sites = list(waves.keys())

size = len(waves)
print(f'{size} - количество сайтов')

matrix = np.zeros((size,size))

for i in range(size):
    for j in range(size):

        if sites[j] in waves[sites[i]]: # Если сайт Sj лежит в списке, куда ведет сайт Si
            matrix[i, j] = (1-size*gamma)/len(waves[sites[i]])
        matrix[i, j] += gamma

Q = np.copy(matrix)
for i in range(2000):
    Q = np.dot(Q,matrix)

l = Q[0]

print(l)

# Сортировка вектора l в порядке убывания
sorted_indices = np.argsort(l)[::-1]
sorted_l = l[sorted_indices]

# Вывод значений вектора и приписывание к индексу элемента из списка sites
for i, value in enumerate(sorted_l):
    index = sorted_indices[i]
    print(f"Значение {value}, сайт {sites[index]}")


#{'A': ['C', 'D', 'E', 'G'], 'B': ['A', 'F', 'J', 'K'], 'C': ['G', 'I', 'K'], 'D': ['G', 'H', 'J', 'L'], 'E': ['A', 'B', 'C', 'I'], 'F': ['A', 'D', 'I', 'J'], 'G': ['F', 'I', 'K'], 'H': ['G', 'K', 'L'], 'I': ['C', 'F', 'G'], 'J': ['D', 'G', 'L'], 'K': ['A', 'F', 'J'], 'L': ['D', 'H', 'K']}
#12 - количество сайтов
#[0.07909559 0.01602823 0.06368967 0.10457162 0.02740103 0.1192901
# 0.1438846  0.05575107 0.1031605  0.09607312 0.11351363 0.07754085]
#Значение 0.14388459775158208, сайт G
#Значение 0.11929010232725641, сайт F
#Значение 0.11351362585453087, сайт K
#Значение 0.10457161656386972, сайт D
#Значение 0.10316050080671976, сайт I
#Значение 0.09607311823953563, сайт J
#Значение 0.07909558910832733, сайт A
#Значение 0.07754085146969604, сайт L
#Значение 0.06368966968664619, сайт C
#Значение 0.055751072075162195, сайт H
#Значение 0.027401029603832023, сайт E
#Значение 0.01602822651284306, сайт B
