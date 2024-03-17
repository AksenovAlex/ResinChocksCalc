import math

pin_parameters = ['Количество', 'Средний диаметр стержня']

def pin_square(d, n):
    diameter = float(d)
    count = float(n)

    one_pin_square = math.pi * pow(diameter, 2) / 4
    total_pin_square = one_pin_square * count

    return total_pin_square
