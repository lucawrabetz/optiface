#!/usr/bin/env python3

from front.app import OptiFaceTUI


def generator():
    for i in range(10):
        yield i


def main():
    app = OptiFaceTUI()
    app.run()
    gen = generator()
    for i in gen:
        print(i)


if __name__ == "__main__":
    main()
