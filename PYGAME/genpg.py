def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

for i in range(10):
    print(next(infinite_sequence()))