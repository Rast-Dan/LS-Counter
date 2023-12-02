places_number = 4  # количество мест в раунде (количество участников ЛС за вычетом ведущего)
rounds_number = 4  # количество раундов для каждого участника (количество выпусков за вычетом тех, где он ведёт)


def count_intersections(sums: list, debug: bool = False, skip_permutations: bool = True):
    """
    Функция подсчёта количества пересечений для данного набора сумм.
    :param sums: набор сумм
    :param debug: Вывод информации о найденных пересечениях
    :param skip_permutations: Не считать перестановки набора мест ([1, 2] и [2, 1]) разными наборами.
        Если передать True
            , то результат для наилучшего возможно набора сумм будет 0,
            , иначе - реальное число пересечений с учётом перестановок
    :return: количество пересечений для данного набора
    """
    places_by_sum = {}

    def generate_places():
        """
        Функция генерации наборов мест
        :return: Наборы мест
        """
        def get_places_by_code(code: int):
            """
            Функция генерации набора мест на основе числа.
            Разделяет число на степени places_number и составляет на основе этого список мест
            :param code: Кодовое число от 0 до places_number в степени rounds_number
            :return: Набор мест
            """
            places = []
            for _ in range(rounds_number):
                places.append((code % places_number) + 1)
                code //= places_number
            return places

        for curr_code in range(places_number ** rounds_number):
            curr_places = get_places_by_code(curr_code)
            # Если мы не хотим учитывать перестановки одного и того же набора мест - сортируем
            if skip_permutations:
                curr_places.sort()
            yield curr_places

    def add(places: list):
        """
        Добавляет набор мест в словарь мест по сумме
        :param places: набор мест
        :return: None
        """
        sum_for_curr_places = 0
        for place in places:
            sum_for_curr_places += sums[place - 1]
        if sum_for_curr_places not in places_by_sum:
            places_by_sum[sum_for_curr_places] = set()
        places_by_sum[sum_for_curr_places].add(tuple(places))

    def get_number_collisions():
        """
        Считает количество коллизий на основе словаря мест по сумме
        :return: Количество коллизий
        """
        number_collisions = 0
        for places_sum, places_set in places_by_sum.items():
            number_collisions += len(places_set) * (len(places_set) - 1) // 2
            if debug and len(places_set) > 1:
                print("Intersection for sum {}:\n".format(places_sum))
                for curr_place in places_set:
                    print(curr_place)
        return number_collisions

    for places in generate_places():
        add(places)

    return get_number_collisions()


def generate_sums(iterations: int):
    """
    Генератор сумм
    :param iterations: количество генерируемых сумм
    :return: Сгенерированные суммы
    """
    start_sums = [places_number - i for i in range(places_number)]

    def get_next_sums(sums: list):
        """
        Получение следующей суммы. Логика следующая, находим ближайшее справа число, которое можно увеличить. Нашли - отлично
        :param sums:
        :return:
        """
        for i in range(len(sums) - 1, -1, -1):
            if i == 0 or sums[i] + 1 < sums[i - 1]:
                sums[i] += 1
                for j in range(i + 1, len(sums)):
                    sums[j] = start_sums[j]
                return sums

    curr_sums = start_sums.copy()
    for _ in range(iterations):
        yield curr_sums
        curr_sums = get_next_sums(curr_sums)


minimal_collisions = None
minimal_sums = None

number_iterations = 2000
# Количество перебираемых вариантов сумм,
# чем больше, тем дольше будет работать и тем выше будет шанс найти наилучший ответ.

for sums in generate_sums(number_iterations):
    collisions = count_intersections(sums)
    if minimal_collisions is None or collisions < minimal_collisions:
        minimal_collisions = collisions
        minimal_sums = sums.copy()

print("Minimal number collisions is {} for sums:\n{}".format(minimal_collisions, minimal_sums))

count_intersections(minimal_sums, debug=True)
