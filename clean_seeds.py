import sys


if __name__ == '__main__':
    for line in sys.stdin:
        if '=' in line and '7.1' in line:
            random = line.split('=')[2].split()[0]
            print(random)
