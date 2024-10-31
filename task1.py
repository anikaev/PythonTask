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

    dividend_str = str(dividend)
    divider_int = int(divider)
    line = []

    if divider_int == 0:
        return f"{dividend_str}|{divider_int}\n"

    if dividend < divider_int:
        line.append(f"{dividend_str}|{divider_int}")
        line.append(f"{' ' * len(dividend_str)}|0")
        return '\n'.join(line)


    idx = 0
    nw_num = int(dividend_str[idx])
    chis = ''
    step = []
    pos = []

    while (idx < len(dividend_str)):

        while nw_num < divider_int and idx + 1 < len(dividend_str):
            idx += 1
            nw_num = nw_num * 10 + int(dividend_str[idx])
            if len(chis) > 0:
                chis += '0'

        if nw_num < divider_int and idx + 1 == len(dividend_str):
            chis += '0'
            break

        quot = nw_num // divider_int
        prd = quot * divider_int
        pm = nw_num - prd
        chis += str(quot)
        pos.append(idx - len(str(nw_num)) + 1)
        step.append((pos[-1], nw_num, prd))
        idx += 1
        if idx < len(dividend_str):
            nw_num = pm * 10 + int(dividend_str[idx])
        else:
            nw_num = pm

    line.append(f"{dividend_str}|{divider_int}")


    first_pos = step[0][0]
    first_prd = step[0][2]
    spac_bf_prd = ' ' * first_pos
    spaces_af_prd = ' ' * (len(dividend_str) - first_pos - len(str(first_prd)))
    line.append(f"{spac_bf_prd}{first_prd}{spaces_af_prd}|{chis}")

    for i in range(1, len(step)):
        pos = step[i][0]
        num = step[i][1]
        prod = step[i][2]
        spaces = ' ' * pos
        line.append(f"{spaces}{num}")
        line.append(f"{spaces}{prod}")

    last_pos = len(dividend_str) - len(str(nw_num))
    spaces = ' ' * last_pos
    line.append(f"{spaces}{nw_num}")

    return '\n'.join(line)


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
