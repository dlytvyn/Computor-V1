import sys
import re


def square_root(num):
    k = 1.0
    while (k*k - num) > 0.0000000001 or (num - k * k) > 0.0000000001:
        k = (k + num / k) / 2
    return k


def reduced(c, b, a):
    coefs = c, b, a
    options = ('{:+.2f} * X^0', '{:+.1f} * X^1', '{:+.1f} * X^2')
    text = ' '.join([expression.format(item) for expression, item in zip(options, coefs) if item])
    if text:
        text += ' = 0'
        if text[0] == '+':
            text = text[1:]
    return text


def solve_complex_roots(b, a, d):
    r = -b / (2 * a)
    r = 0 if r == 0 else r
    i = square_root(d) / (2 * a)
    i = -i if i < 0 else i
    x1 = "{:.5f} + {:.5f}i".format(r, i)
    x2 = "{:.5f} - {:.5f}i".format(r, i)
    print("The solution is:\nx1 = {:s}\nx2 = {:s}".format(x1, x2))


def coefs_from_sign(data):
    res = 0
    for item in data:
        if '-' in item:
            res -= 1
        else:
            res += 1
    return res


def get_coefs(equation):
    regs = [re.compile(r'(-\s*\d+|\s*\d+.\d+|-\s*\d+.\d+|\s*\d+)\s*\*\s*[Xx]\s*\^\s*{:d}'.format(power)) for power in range(3)]
    res = list(map(lambda reg: sum(map(float, map(lambda x: x.replace(' ', ''), re.findall(reg, equation)))), regs))

    regs2 = [re.compile(r'([-/+]|^)\s*[Xx]\s*\^\s*2'),  # a = x^2
             re.compile(r'([-+=]|^)\s*[Xx][^\^]'),  # b = x
             re.compile(r'(([+-]|^)\s*([0-9]+|[0-9]+.[0-9]+))\s*\*\s*[xX]([ ]|$)'),  # b = n * x   group 0
             re.compile(r'((([-+=]|^)\s*([0-9]+|[0-9]+.[0-9]+))\s*([-+=]|$))')]  # c = C group 1

    a = list(map(str, map(lambda x: x.replace(' ', ''), re.findall(regs2[0], equation))))
    b = list(map(str, map(lambda x: x.replace(' ', ''), re.findall(regs2[1], equation))))
    b2 = re.findall(regs2[2], equation)
    b2 = sum(list(map(float, map(lambda x: x.replace(' ', ''), [item[0] for item in b2]))))
    c = re.findall(regs2[3], equation)
    c = sum(list(map(float, map(lambda x: x.replace(' ', ''), [item[1] for item in c]))))
    res[2] += coefs_from_sign(a)
    res[1] += coefs_from_sign(b)
    res[1] += b2
    res[0] += c

    return res


def check_syntax(equation):
    valid = '0123456789-+=xX. \t*^'
    for sign in equation:
        if sign not in valid:
            exit('There is a syntax error!')


def main(equation):
    check_syntax(equation)
    parts = equation.split('=')
    if len(parts) < 2 or (not parts[0] or not parts[1]):
        exit('There is no equation or it is incorrect')
    if not len(parts) == 2:
        exit('There is no right part of equation')
    if re.findall('[xX]\s*\^\s*([3-9]|\d{2,})', equation):
        exit("The polynomial degree is strictly greater than 2, I can't solve it!")
    c1, b1, a1 = get_coefs(parts[0])
    c2, b2, a2 = map(lambda x: x * (-1), get_coefs(parts[1]))
    a = a1 + a2
    b = b1 + b2
    c = c1 + c2
    if not a and not b:
        if c1 == -c2:
            exit('All real number are solutions')
        exit('This expression is not an equation!')
    degree = 2 if a else 1 if b else 0
    print('Initial equation: ', equation)
    print('Reduced form: ', reduced(c, b, a))
    print('Polynomial degree: ', degree)
    if degree == 2:
        d = b ** 2 - 4 * a * c
        print('D = {}'.format(d))
        print("x = ({:.5f} +- sqrt({:.3f})) / (2 * {:.3f})".format(-b, d, a))
        if d >= 0:
            x1 = (-b + square_root(d)) / (2 * a)
            x2 = (-b - square_root(d)) / (2 * a)
            print("The solution is:\nx1 = {:.5f}\nx2 = {:.5f}".format(x1, x2))
        else:
            print('Descriminant is less than 0, roots are complex')
            solve_complex_roots(b, a, -d)
    else:
        if c1 == -c2 and (b1 == 0 and b2 == 0):
            exit('There is no possible solutions')
        if b1 == -b2 and c1 == -c2:
            exit('All real number are solutions')
        x = c / -b
        x = 0 if c == 0 else x
        print("The solution is:\nx = {:.5f}".format(x))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        par = input("Enter your equation: ")
        main(par)
    else:
        main(sys.argv[1])
