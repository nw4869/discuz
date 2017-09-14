import hashlib
from multiprocessing import Pool
from multiprocessing.sharedctypes import Value
import sys
import argparse
from time import sleep, time

ended = Value('b', 0, lock=False)
counter = Value('l', 0)


def dsign(iddwdh, authkey):
    m = hashlib.md5()
    iddwdh_authkey = iddwdh + authkey
    m.update(iddwdh_authkey.encode('utf-8'))
    return m.hexdigest()[:16]


def get_prefixes():
    for i in range(0x000000, 0x1000000):
        yield '%06x' % i


def get_suffixes(file):
    return [suffix.strip() for suffix in file]


def get_authkey(suffix):
    for prefix in get_prefixes():
        yield prefix + suffix


def crack(suffix):
    try:
        count = 0
        for authkey in get_authkey(suffix):
            if ended.value:
                return
            # print('trying:', authkey)

            count += 1
            if count % 100 == 0:
                with counter.get_lock():
                    counter.value += count
                count = 0

            dsign_result = dsign(to_sign, authkey)
            # print('authkey: %s, sign: %s, sign_target: %s' % (authkey, dsign_result, sign))
            if dsign_result == sign:
                print('[*] authkey: ' + authkey)
                ended.value = 1
    except KeyboardInterrupt:
        ended.value = 1


def print_stats():
    time_usage = time() - start_time
    current = counter.value
    print('\r%.2f%%: %s / %s, %.2fs' % (current / total_try * 100, current, total_try, time_usage), file=sys.stderr, end='')


def main(args):
    suffixes = get_suffixes(randoms_file)
    global total_try
    total_try = len(suffixes) * 16 ** 6

    global start_time
    start_time = time()

    with Pool() as pool:
        result = pool.map_async(crack, suffixes)
        while not ended.value:
            print_stats()
            if result.ready():
                print('not found?', file=sys.stderr)
                break
            sleep(1)

    print('done.', file=sys.stderr)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('to_sign')
        parser.add_argument('sign')
        parser.add_argument('--randoms_file', type=argparse.FileType('r'), default=sys.stdin, required=False)
        args = parser.parse_args()

        print(args)

        to_sign = args.to_sign
        sign = args.sign
        randoms_file = args.randoms_file

        main(args)
    except KeyboardInterrupt:
        print('KeyboardInterrupt', file=sys.stderr)
