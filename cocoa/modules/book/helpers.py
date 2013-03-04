# -*- coding: utf-8 -*-

def isbn10_to_13(isbn10):

    isbn13 = '978' + isbn10[:-1]
    r = sum(int(x) * weight for x, weight in zip(isbn13, (1, 3) * 6))
    chksum = (10 - r % 10) % 10
    return isbn13 + str(chksum)


def isbn13_to_10(isbn13):

    isbn10 = isbn13[3:12]
    r = sum((10 - i) * (int(x) if x != 'X' else 10) \
        for i, x in enumerate(isbn10) if i != 9)
    chksum = (11 - r % 11) % 11
    return isbn10 + str(chksum)
