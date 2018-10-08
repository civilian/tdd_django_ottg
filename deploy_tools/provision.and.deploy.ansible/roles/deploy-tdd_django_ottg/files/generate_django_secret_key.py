#!/usr/bin/env python
"""
Pseudo-random django secret key generator
"""
from __future__ import print_function
import random

chars = 'abcdefghijklmnopqrstuvwxyz' \
        'ABCDEFGHIJKLMNOPQRSTUVXYZ' \
        '0123456789' \
        '#()^[]-_*%&=+/'

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

write_file = open(".django_secret_key", "w")
write_file.write(SECRET_KEY)
# Cierro el archivo para guardar lo que escribimos
write_file.close()