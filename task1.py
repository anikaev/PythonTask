def long_division(dividend, divisor):
    if dividend < divisor:
        return f"{dividend}|{divisor}\n{dividend}|0"

    dividend_str = str(dividend)
    divisor_str = str(divisor)
    result = f"{dividend_str}|{divisor_str}\n"

    numstr = ''
    rem = 0
    fr_div = True
    pos = []

    for idx, digit in enumerate(dividend_str):
        rem = rem * 10 + int(digit)
        if rem < divisor:
            numstr += '0'
            continue
        par_qu = rem // divisor
        numstr += str(par_qu)
        par_pr = par_qu * divisor
        rem -= par_pr

        par_l = len(str(par_pr))
        cur_ind = idx - par_l + 1
        pos.append((cur_ind, par_pr))

        if not fr_div:
            result += (' ' * cur_ind +
                       str(rem + par_pr) + '\n')
        else:
            fr_div = False

        result += (' ' * cur_ind +
                   str(par_pr) + '\n')

    if rem != 0:
        fin_ind = (len(dividend_str) -
                   len(str(rem)))
        result += (' ' * fin_ind +
                   str(rem))
    else:
        if pos:
            l_ind, l_pr = pos[-1]
            result += (' ' * (l_ind
                              + len(str(l_pr)) - 1)
                       + '0')
        else:
            result += (' ' * (len(dividend_str) - 1)
                       + '0')

    lines = result.split('\n')
    for i, line in enumerate(lines):
        if ('|' not in line and line.strip().isdigit()):
            qu = (len(dividend_str) -
                  len(line.strip()))
            if numstr.lstrip("0"):
                lines[i] += (' ' * qu + f"|{int(numstr.lstrip('0'))}")
            else:
                lines[i] += (' ' * qu + f"|0")
            break

    result = '\n'.join(lines)

    return result


def main():
    print(long_division(100000, 500))
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


if __name__ == '__main__':
    main()
