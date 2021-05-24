
def main():
    value, number = list(map(int, input().split()))
    for i in range(number):
        if value % 10 == 0:
            value //= 10
        else:
            value -= 1
    print(value)

main()