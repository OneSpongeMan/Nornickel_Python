# Основы Python, Задача 1
data = input()
data = [int(i) for i in data.split()]

i = 0
while data[i] != 237:
    if data[i] % 2 == 0:
        print(data[i])
    i += 1