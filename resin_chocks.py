resin_chock_parameters = ['Длина', 'Ширина', 'Количество']

resin_chock_material = [
    'EPY',
    'Epocast 36',
    'Chockfast orange',
    'ЭПМ'
]

resin_chock_material_parameters = {
    'EPY': {'weight_load': 0.9, 'total_load': 5, 'friction_ratio': 0.36, 'detsity': 1590},
    'Epocast 36': {'weight_load': 0.7, 'total_load': 5, 'friction_ratio': 0.57, 'detsity': 1580},
    'Chockfast orange': {'weight_load': 0.7, 'total_load': 5, 'friction_ratio': 0.7, 'detsity': 1580},
    'ЭПМ': {'weight_load': 0.9, 'total_load': 5, 'friction_ratio': 0.7, 'detsity': 1580}}


def resin_chocks_square(*args):
    chocks = list(args)[0].split(',')
    square = 0
    for chock in chocks:
        length, width, count = map(float, chock.split('-'))
        square += (length * width * count)

    return square
