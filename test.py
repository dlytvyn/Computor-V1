import sys
import re


def square_root(num):
    k = 1.0
    while (k*k - num) > 0.0000000001 or (num - k * k) > 0.0000000001:
        k = (k + num / k) / 2
    return k


def reduced(degree, c, b, a):
    if degree != 2:
        text = '{:+.1f} * X^0{:+.1f} * X^1 = 0'.format(c, b)
    else:
        text = '{:+.1f} * X^0{:+.1f} * X^1{:+.1f} * X^2 = 0'.format(c, b, a)
    if text[0] == '+':
        text = text[1:]
    text = text.replace('-', ' - ')
    text = text.replace('+', ' + ')
    return text


def syntax(part):
    space_degree = re.compile(r'([Xx]\s+\^)')
    space_degree_1 = re.compile(r'([Xx]\^\s+)')
    negative_power = re.compile(r'[Xx]\^-[0-2]')

    space_degree_find = re.findall(space_degree, part)
    space_degree_find_1 = re.findall(space_degree_1, part)
    if space_degree_find or space_degree_find_1:
        exit("Invalid degree syntax")
    n_degree = re.findall(negative_power, part)
    if n_degree:
        exit("Negative degree")


def matcher(part):
    power_2_matcher = re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\^2')
    power_1_matcher = re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\^1')
    power_1_matcher_1 = re.compile(r'([-+]|)\s*[Xx][^\^]')
    power_1_matcher_2 = re.compile(r'([-+]|)\s*[Xx]\^0\s*')
    power_1_matcher_3 = re.compile(r'([-+]|)\s*[Xx]\^1\s*')
    power_1_matcher_4 = re.compile(r'([-+]|)\s*[Xx]\^2\s*')
    power_0_matcher = re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\^0')
    power_0_matcher_1 = re.compile(r'[^\^-]\s*(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*[-+=]')
    absent_power = re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\s*[-+=]')

    a1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_2_matcher, part))))
    b1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_1_matcher, part))))
    c1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_0_matcher, part))))
    c1_1 = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(power_0_matcher_1, part))))
    minus_x_1 = sum(map(float, map(lambda x: "-1" if x == "-" else ("1" if x == "" else "0"),
                                   re.findall(power_1_matcher_1, part))))
    absent_coeff_find_1 = sum(map(float, map(lambda x: "-1" if x == "-" else ("1" if x == "" else "0"),
                                             re.findall(power_1_matcher_2, part))))
    absent_coeff_find_2 = sum(map(float, map(lambda x: "-1" if x == "-" else ("1" if x == "" else "0"),
                                             re.findall(power_1_matcher_3, part))))
    absent_coeff_find_3 = sum(map(float, map(lambda x: "-1" if x == "-" else ("1" if x == "" else "0"),
                                             re.findall(power_1_matcher_4, part))))
    absent_degree_find = sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(absent_power, part))))

    print("PRINT", b1, minus_x_1, absent_degree_find, absent_coeff_find_2)
    b1 = sum([b1, minus_x_1, absent_degree_find, absent_coeff_find_2])
    c1 = sum([c1, c1_1, absent_coeff_find_1])
    a1 = sum([a1, absent_coeff_find_3])

    return [a1, b1, c1]


def main(equation):
    empty = re.compile(r'(\s*=\s*)')
    is_empty = re.match(empty, equation)
    if is_empty:
        exit('Invalid equation')
    parts = equation.split('=')
    # print(parts)
    if not len(parts) == 2:
        exit('There is no right part of equation')
    parts[0] += "="
    parts[0] = " " + parts[0]
    if re.findall(r'[xX]\^([3-9]|\d{2,})', equation):
        print("The polynomial degree is strictly greater than 2, I can't solve")
        sys.exit(0)

    syntax(parts[0])
    syntax(parts[1])

    left_result = matcher(parts[0])
    right_result = matcher(parts[1])

    a = left_result[0] + right_result[0] * -1
    b = left_result[1] + right_result[1] * -1
    c = left_result[2] + right_result[2] * -1

    print('a = {}, b = {}, c = {}'.format(a, b, c))
    if a or b:
        degree = 2 if a else 1
    else:
        if left_result[2] == -right_result[2]:
            exit('All real number are solutions')
        exit('No solutions')
    print('Reduced form: {}'.format(reduced(degree, c, b, a)))
    print('Polynomial degree: {}'.format(degree))
    if degree == 2:
        d = b ** 2 - 4 * a * c
        print('D = {}'.format(d))
        print("x = {:.5f} [+|-] sqrt({:.3f}) / 2 * {:.3f}".format(-b, d, a))
        if d >= 0:
            x1 = (-b + square_root(d)) / (2 * a)
            x2 = (-b - square_root(d)) / (2 * a)
            print("The solution is:\nx1 = {:.5f}\nx2 = {:.5}".format(x1, x2))
        else:
            x1R = (-b / (2 * a))
            x1I = square_root(-d) / (2 * a)
            sign1 = "+" if x1I > 0 else "-"
            x2R = -b / (2 * a)
            x2I = -square_root(-d) / (2 * a)
            sign2 = "+" if x2I > 0 else "-"
            print("The solution is:\nx1 = {:.5f} {} {:.5f}*i\nx2 = {:.5f} {} {:.5}*i".format(abs(x1R), sign1, abs(x1I), abs(x2R), sign2, abs(x2I)))
    else:
        x = c / -b
        print("The solution is:\nx = {:.5f}".format(x))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit('usage: python main.py "equation"')
    main(sys.argv[1])