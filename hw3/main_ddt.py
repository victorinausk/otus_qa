""" Open, read and edit .csv file and write output to .txt """


# -*- coding: UTF-8 -*-

def gen_file():
    """Подготовка тестовых данных"""

    with open('data.csv', mode='r+', encoding='windows-1251') as my_file:
        f = my_file.read().splitlines()
        # убираем первую строку с информацией о данных таблицы
        f.pop(0)
        fn = []
        for i in f:
            # разделяем строки на списки, каждый тип данных (фио, город, тд) - отдельный элемент списка
            s = i.split(',')
            fn.append(s)

        # создаем множества для каждого типа данных (фио, город, наличие карты/депозита/ипотеки)
        names = set()
        cities = set()
        credit_cards = set()
        deposits = set()
        mortgages = set()

        # заполняем множества строками данных из списков
        for i in fn:
            names.add(i[0])
            cities.add(i[1])
            credit_cards.add(i[2])
            deposits.add((i[3]))
            mortgages.add(i[4])

        # убираем пустые значения
        credit_cards.remove('')
        deposits.remove('')
        mortgages.remove('')

        final = ((name, city, credit_card, deposit, mortgage) for name in names for city in cities
                 for credit_card in credit_cards for deposit in deposits for mortgage in mortgages)

        with open('result_data.txt', 'a') as f_txt:
            for i in final:
                f_txt.write(' '.join(i) + '\n')
