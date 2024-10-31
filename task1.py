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
    output_lines = []

    if divider_int == 0:
        return f"{dividend_str}|{divider_int}\n"

    if dividend < divider_int:
        output_lines.append(f"{dividend_str}|{divider_int}")
        output_lines.append(f"{' ' * len(dividend_str)}|0")
        return '\n'.join(output_lines)


    idx = 0
    current_num = int(dividend_str[idx])
    quotient_str = ''
    steps = []
    positions = []

    while (idx < len(dividend_str)):

        while current_num < divider_int and idx + 1 < len(dividend_str):
            idx += 1
            current_num = current_num * 10 + int(dividend_str[idx])
            if len(quotient_str) > 0:
                quotient_str += '0'

        if current_num < divider_int and idx + 1 == len(dividend_str):
            quotient_str += '0'
            break

        partial_quotient = current_num // divider_int
        product = partial_quotient * divider_int
        remainder = current_num - product
        quotient_str += str(partial_quotient)
        positions.append(idx - len(str(current_num)) + 1)
        steps.append((positions[-1], current_num, product))
        idx += 1
        if idx < len(dividend_str):
            current_num = remainder * 10 + int(dividend_str[idx])
        else:
            current_num = remainder

    output_lines.append(f"{dividend_str}|{divider_int}")


    first_pos = steps[0][0]
    first_product = steps[0][2]
    spaces_before_product = ' ' * first_pos
    spaces_after_product = ' ' * (len(dividend_str) - first_pos - len(str(first_product)))
    output_lines.append(f"{spaces_before_product}{first_product}{spaces_after_product}|{quotient_str}")

    for i in range(1, len(steps)):
        pos = steps[i][0]
        num = steps[i][1]
        prod = steps[i][2]
        spaces = ' ' * pos
        output_lines.append(f"{spaces}{num}")
        output_lines.append(f"{spaces}{prod}")

    last_pos = len(dividend_str) - len(str(current_num))
    spaces = ' ' * last_pos
    output_lines.append(f"{spaces}{current_num}")

    return '\n'.join(output_lines)


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
