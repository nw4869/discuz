import argparse

s = 'uie7'
# s = 'W7pq'
rand_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'


def get_seed():
    php_mt_seed_args = ['0 61 0 61'] * 10
    for c in args.prefix:
        pos = rand_str.index(c)
        php_mt_seed_args.append('%s %s 0 %s' % (pos, pos, len(rand_str) - 1))
    return ' '.join(php_mt_seed_args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('prefix')

    args = parser.parse_args()

    php_mt_seed_args = get_seed()

    print(php_mt_seed_args)
