# coding: utf-8
from calculator import calculator


def app():
    while True:
        f = input('>')
        print('={}'.format(calculator(f)))


if __name__ == '__main__':
    app()
