import sys


if __name__ == '__main__':
    for line in sys.stdin:
        if '=' in line:
            random = line.replace(' ', '').split('=')[1].strip()
            print(random)
