import re


def camel_to_snake(str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def left_pad(s, the_char, length):
    """
    >>> print(n.zfill(3))
    >>> print('{:03d}'.format(n))  # python 3
    >>> print(f'{n:03}') # python >= 3.6
    004
    :param s: the string
    :param the_char: the char
    :param length:
    """
    if type(s) is int:
        a_format = "{:" + str(the_char) + str(length) + "}"
        return a_format.format(s)
    elif type(s) is str:
        return s.rjust(length, the_char)
