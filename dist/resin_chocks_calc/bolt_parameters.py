import math

THREAD_TYPE = [
    '', 'M2x0.4', 'M2.2x0.45', 'M2.5x0.45', 'M3x0.5',
    'M3.5x0.6', 'M4x0.7', 'M4.5x0.75', 'M5x0.8',
    'M6x1', 'M8x1.25', 'M10x1.5', 'M12x1.75',
    'M14x2', 'M16x2', 'M18x2.5', 'M20x2.5',
    'M22x2.5', 'M24x3', 'M27x3', 'M30x3.5',
    'M33x3.5', 'M36x4', 'M39x4', 'M42x4.5',
    'M45x4.5', 'M48x5', 'M52x5',
    'M56x5.5', 'M60x5.5', 'M64x6', 'M68x6',
]

BOLT_CLASS = [
    '', '3.6', '4.6', '4.8', '5.6',
    '5.8', '6.6', '6.8', '8.8',
    '9.8', '10.9', '12.9'
]

BOLT_TYPE = ['', 'Проходной', 'Призонный', 'Отжимной']

BOLT_PARAMETERS = ['Резьба', 'Класс прочности', 'Количество', 'Диаметр отверстия', 'Тип болта']


def bolt_thread_parameters(thread: str) -> dict:
    d, p = map(float, thread[1:].split('x'))
    h = round(0.866025 * p, 3)
    dv = round(d - 2 * (5 / 8) * h, 3)
    s = round(math.pi * pow((dv / 2), 2), 2)

    return {'D': d, 'P': p, 'H': h, 'd': dv, 'S': s}


def bolt_class_parameters(bolt_class: str) -> dict:
    cls_param = list(map(int, bolt_class.split('.')))
    sigma_v = cls_param[0] * 100
    sigma_t = cls_param[0] * cls_param[1] * 10

    return {'sigma_v': sigma_v, 'sigma_t': sigma_t}


def bolt_force_by_tightening(sigma_t, s):
    q = eval(f'0.6 * {sigma_t} * {s}')
    return q


def bolt_tightening_load(sigma_t=0, square=0):
    sigma_t = sigma_t
    square = square
    tightening_load = round(0.6 * sigma_t * square, 2)
    return tightening_load


def bolt_tightening_torque(thq_diam=0, load=0):
    thread_diameter = thq_diam
    tightening_load = load
    tightening_torque = round((tightening_load * thread_diameter) / 5000)
    return tightening_torque



