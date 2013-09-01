import string


def baseEncode(number, base=0):
    if isinstance(number, str):
        if number == '':
            number = 0
        number = long(number)
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')
    if base < 0:
        raise ValueError('base must be positive')

    alphabet = string.digits + string.ascii_letters + '_'

    if base > len(alphabet):
        raise ValueError('base is too big (%s>%s)' % (base, len(alphabet)))

    if base == 0:
        base = len(alphabet)

    baseN = ''
    while number:
        number, i = divmod(number, base)
        baseN = alphabet[i] + baseN

    return baseN or alphabet[0]