from collections import defaultdict


def dehuff(code, huff):

    result = ''

    dict_dehuff = defaultdict(lambda: 2)

    for num in huff:
        dict_dehuff[num[1]] = num[0]

    temp = ''
    for digit in code:
        temp += digit
        if dict_dehuff[temp] != 2:
            result += dict_dehuff[temp]
            temp = ''
    return result