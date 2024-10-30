def long_division(dividend, divider):
    '''
       Вернуть строку с процедурой деления «уголком» чисел dividend и divider.
       Формат вывода приведён на примерах ниже.

       Примеры:
       12345|25
       100  |493
        234
        225
          95
          75
          20

       1234|1423
       1234|0

       24600|123
       246  |200
         0

       246001|123
       246   |2000
            1
       '''

    delimoe_str = str(dividend)
    delitel_int = int(divider)
    stroki = []
    stroki.append(f"{delimoe_str}|{delitel_int}")

    if delitel_int == 0:
        stroki.append(f"{delimoe_str}|0")
        return '\n'.join(stroki)

    if int(delimoe_str) < delitel_int:
        stroki[0] += '\n' + (len(delimoe_str))*" " + "|0"
        return '\n'.join(stroki)

    idx = 0
    num = int(delimoe_str[idx])
    chast = ''
    poz_list = []

    while idx < len(delimoe_str):
        while num < delitel_int and idx + 1 < len(delimoe_str):
            idx += 1
            num = num * 10 + int(delimoe_str[idx])
            if len(chast) > 0:
                chast += '0'

        if num < delitel_int and idx + 1 == len(delimoe_str):
            chast += '0'
            break

        chastnoe = num // delitel_int
        ostatok = num % delitel_int
        chast += str(chastnoe)
        poz = idx - len(str(num)) + 1
        poz_list.append((poz, num, chastnoe * delitel_int))
        num = ostatok
        idx += 1

        if idx < len(delimoe_str):
            num = num * 10 + int(delimoe_str[idx])

    poz, num, proiz = poz_list[0]
    probel = ' ' * poz
    proiz_str = str(proiz)
    probel_ch = ' ' * (len(delimoe_str) - (poz + len(proiz_str)))
    stroka2 = f"{probel}{proiz_str}{probel_ch}|{chast}"
    stroki.append(stroka2)

    for i in range(1, len(poz_list)):
        poz, num, proiz = poz_list[i]
        probely = ' ' * poz
        stroki.append(f"{probely}{num}")
        stroki.append(f"{probely}{proiz}")

    if num != 0:
        probely = ' ' * (idx - len(str(num)))
        stroki.append(f"{probely}{num}")

    return '\n'.join(stroki)


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))

if __name__ == '__main__':
    main()