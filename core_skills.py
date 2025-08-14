import random

rand_list = [random.randint(1, 20) for _ in range(10)]
print(rand_list)

list_comprehension_below_10 = [num for num in rand_list if num < 10]
print(list_comprehension_below_10)

list_comprehension_below_10 = list(filter(lambda num: num < 10, rand_list))
print(list_comprehension_below_10)