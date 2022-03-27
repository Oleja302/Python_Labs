from sympy import *


def nonLinSolve(equa, unknown):
    return nonlinsolve(equa, unknown)


x = Symbol('x')
exp = x ** 2

print('Function (black line): ' + f'{exp}')
p = plot(exp, line_color='black', show=False, legend=True)

print('Integrate (red line): ' + f'{integrate(exp, x)}')
p.extend(plot(integrate(exp, x), line_color='red', show=False))

print('Derivative (blue line): ' + f'{diff(exp, x)}')
p.extend(plot(diff(exp, x), line_color='blue', show=False))

print()

a, b = symbols('a b')
res = nonLinSolve([a ** 2 + a, a - b], [a, b])
for i, j in res:
    print(f'a = {i} b = {j}')

p.show()
