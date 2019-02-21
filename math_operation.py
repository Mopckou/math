import math


def get_aver_and_error(data):
    summ = 0
    for i in data:
        summ = summ + float(i)
    average_sour = summ / len(data)
    data.sort()
    max_data = float(data[-1])
    error_data = abs(average_sour - max_data)
    print('Массив %s, максимальное = %s' % (data, max_data))
    print('Среднее значение = %s mm +- %s mm,' % (average_sour, error_data))
    print('Число перевод в вольты %s' % transfer)
    average_in_volt = average_sour * transfer
    persent = (error_data / average_sour) * 100
    return average_in_volt, persent


def get_error(errors_list):
    summ = 0

    for error in errors_list:
        summ += error * error

    return math.sqrt(summ)

transfer = None
obs = None

while 1:
    print('Изменить шкалу?')
    data = input()
    if data or transfer is None or obs is None:
        print('Введите вид наблюдения, начало отсчета [v] конец отсчета [v] длину [mm] (для подсчета шкалы)')
        print('Пример: P, 0 3.5 148')
        data = input().split(',')
        obs = data[0].upper()
        begin, end, length = data[1].split()
        transfer = (float(end) - float(begin)) / float(length)
        print(float(end), float(begin), float(length), float(end) - float(begin), (float(end) - float(begin)) / float(length))
    print('Наблюдение: %s' % obs)
    print('Шкала (%s - %s) / %s = %s' % (end, begin, length, transfer))
    print('Введите аплитуду источников [mm], амплитуду системы [mm]\n')
    data = input()
    amp_data, sys_data = data.split(',')
    sour_list = amp_data.split()
    sys_list = sys_data.split()

    sour_aver, sour_persent = get_aver_and_error(sour_list)
    print('Среднее значение источника = %s Вольт, Процент = %s\n' % (sour_aver, sour_persent))
    print('\n')

    for num, value in enumerate(sys_list):
        sys_list[num] = (float(value) * transfer) + float(begin)

    sys_aver, sys_persent = get_aver_and_error(sys_list)
    print('Среднее значение шума = %s Вольт, Процент = %s\n' % (sys_aver, sys_persent))
    print('\n')

    if obs not in ['L', 'P', 'K', 'C']:  # (18cm, 92cm, 1.35, 6)
        raise Exception('Unknown observation')
    nul = {'K': 0.527, 'C': 0.378, 'L': 0, 'P': 0}
    sys = float(sys_aver) - nul[obs]

    print('sys = (%s - %s) = %s\n' % (sys_aver, nul[obs], sys))
    print('sys / sour = %s +- %s / %s +- %s = %s +- %s' % (sys, 0, sour_aver, sour_persent, sys/sour_aver, get_error([sour_persent, sys_persent])))
    print('-------------------------------------------\n')