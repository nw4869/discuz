#!/bin/sh
python3 get_seed.py "$1" | xargs ./php_mt_seed |  python3 clean_seeds.py | php get_randoms_stdin.php | python3 get_authkey.py "$2" "$3"

