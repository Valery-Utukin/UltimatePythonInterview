import time
import random
import asyncio
from typing import Callable, Any, Awaitable
from functools import wraps, lru_cache


# Декоратор для подсчета времени выполнения функции. Функции не должны принимать параметров!
def timer_decorator(func: Callable) -> Callable:
    print("timer_decorator started")

    def wrapper():
        print("time_decorator's wrapper started")
        start = time.time()
        func()
        finish = time.time()
        print(f"Func {func} runs for {finish - start} sec.")

    return wrapper


# @timer_decorator
def count_till_5():
    for i in range(5):
        print(f"Count: {i+1}")
        time.sleep(1.0)


def param_timer_deco(func: Callable) -> Callable:
    print("param_timer_deco started")

    def wrapper(*args, **kwargs):
        print("time_decorator's wrapper started")
        start = time.time()
        func(*args, **kwargs)
        finish = time.time()
        print(f"Func {func} runs for {finish - start} sec.")

    return wrapper


# @param_timer_deco
def count_till_param(count, sleep_time):
    for i in range(count):
        print(f"Count: {i+1}")
        time.sleep(sleep_time)


# У декоратора с параметром добавляется один уровень вложенности
def limit_run(limit: int) -> Callable:
    original_limit = limit

    def wrapper(func: Callable) -> Callable:
        def inner(*args, **kwargs):
            nonlocal limit  # limit следует искать в ближайших внешних функциях. Что-то про замыкание :)
            if limit == 0:
                raise ValueError(f"func: {func} can't run more than {original_limit} times")
            res = func(*args, **kwargs)
            limit -= 1
            return res
        return inner
    return wrapper


@limit_run(1)
def create_map(length: int, width: int) -> list[list[int]]:
    # Функция создаёт условную игровую карту высот.
    # В случае реальной игры, подобная функция должна быть выполнена только один раз!
    return [[random.randint(0, 10) for _ in range(0, length)] for _ in range(0, width)]


def important_deco(func: Callable) -> Callable:
    """Doc string from important decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Doc string from wrapper in the important decorator"""
        return func(*args, **kwargs)
    return wrapper


@important_deco
def important_func() -> None:
    """Some really important doc string"""
    print("Really important things are happening...")


# PyCharm ругается, если в качестве типа корутины указать Coroutine из модуля typing. Но код при этом
# будет работать. ChatGPT подсказал такую аннотацию: Callable[..., Awaitable[Any]]. С ней тоже всё работает,
# и IDE не ругается.
def async_decorator(coroutine: Callable[..., Awaitable[Any]]):
    print("async_decorator started")

    async def wrapper(*args, **kwargs):
        res = await coroutine(*args, **kwargs)
        print(f"Coroutine {coroutine.__name__} finished")
        return res
    return wrapper


# @async_decorator
async def async_func():
    await asyncio.sleep(2.0)
    return 1


@lru_cache()
def solve_the_universe():
    time.sleep(2.0)
    return 42


if __name__ == '__main__':
    # Декоратор без параметра.

    # Первый способ использования декоратора. Функция count_till_5 не помечается как @timer_decorator,
    # а декорируется таким образом: count_till_5 = timer_decorator(count_till_5). Последующий вызов
    # этой функции применит команды из обертки декоратора.
    # count_till_5 = my_decorator(count_till_5)
    # count_till_5()

    # Второй способ использовать декоратор, это синтаксис c @. Наиболее предпочтительный!
    # count_till_5()

    # Декорирование функций, которые принимают параметры.
    # count_till_param(10, 0.1)  # Вызов используя *args
    # count_till_param(count=5, sleep_time=0.5)  # Вызов используя **kwargs
    # count_till_param(10, sleep_time=0.2)  # Вызов используя и *args и **kwargs

    # Декоратор с параметром.
    # limit_run(1) - декоратор с параметром, ограничивающий количество вызовов функции
    # print(create_map(5, 2))  # Выполнится первый раз, без ошибок
    # Пытаясь вызвать функцию create_map снова, будет поднято исключение ValueError.
    # Может ValueError не самый подходящий эксепшн, но в моменте других не вспомнил. Может стоит поискать другой :)
    # try:
    #     print(create_map(5, 2))
    # except ValueError as ve:
    #     print(ve)

    # Декоратор @wraps
    # Если декорируемая функция содержит строку документации, то попытка её просмотра с помощью __doc__
    # покажет строку документации функции-обертки. В случае чтения имени функции мы также получим имя функции-обертки.
    # Решение - использование декоратора wraps из модуля functools
    # print(important_func.__doc__)
    # print(important_func.__name__)

    # Вызов корутины с декоратором.
    # asyncio.run(async_func())

    # Декоратор lru_cache. Используется для кэширования результата выполнения некоторой функции.
    # Имеет смысл использовать для долго работающих функций.
    print(solve_the_universe())  # Первый раз функция честно выполнится и результат будет записан в кэш
    print(solve_the_universe())  # Второй раз функция просто вернет результат из кэша
