from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np
import re

def parse_coefficients(expression):
    terms = re.split(r'\+|\-', expression)
    coefficients = []
    for term in terms:
        if term == '':
            continue
        elif term == '-':
            coefficients.append(-1)
        else:
            coefficient = term.split('x')[0]
            if coefficient == '':
                coefficient = '1'
            coefficients.append(int(coefficient))
    return coefficients





def parse_constraint(expression):
    coefficients = parse_coefficients(expression)
    operator = re.search(r'<=|>=|=', expression).group()
    rhs = int(expression.split(operator)[1])
    return coefficients, rhs, operator

def parse_objective(expression):
    coefficients = parse_coefficients(expression)
    return coefficients

def plot_linear_programming_problem_alt(objective, constraints, problem_type):
    c = parse_objective(objective)
    A = []
    b = []
    operators = []
    for constraint in constraints:
        coefficients, rhs, operator = parse_constraint(constraint)
        A.append(coefficients)
        b.append(rhs)
        operators.append(operator)

    # Adjust the signs of the objective function coefficients based on the problem type
    if problem_type == "max":
        c = [-val for val in c]

    # Solve the linear programming problem
    result = linprog(c, A_ub=A, b_ub=b)

    # Adjust the sign of the optimal objective value based on the problem type
    if problem_type == "min":
        optimal_value = result.fun
    else:
        optimal_value = -result.fun

    # Plot the constraints
    x_max = max([b_value / coefficient for coefficients, b_value, _ in zip(A, b, operators) for coefficient in coefficients if coefficient != 0])
    x = np.linspace(0, x_max + 5, 100)
    for i in range(len(A)):
        coefficients = A[i]
        rhs = b[i]
        operator = operators[i]
        constraint_label = f'Constraint {i+1}: {coefficients[0]}x1'
        for j in range(1, len(coefficients)):
            if coefficients[j] >= 0:
                constraint_label += f' + {coefficients[j]}x{j+1}'
            else:
                constraint_label += f' - {abs(coefficients[j])}x{j+1}'
        constraint_label += f' {operator} {rhs}'
        plt.plot(x, (rhs - coefficients[0] * x) / coefficients[1], label=constraint_label)

    # Ajustar o eixo y para se concentrar no ponto ótimo
    plt.ylim(result.x[1] - 10, result.x[1] + 10)

    # Plot the optimal solution
    label_text = f"({result.x[0]:.2f}, {result.x[1]:.2f})"
    plt.plot(result.x[0], result.x[1], 'ro', label=f'Optimal Solution: {label_text}')
    plt.text(result.x[0], result.x[1], label_text, ha='right', va='bottom')

    # Add optimal value below the table
    plt.text(0.45, -0.1, f"Optimal value: {round(optimal_value, 2)}", fontsize=10, transform=plt.gca().transAxes)

    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title('LP: Graphical Solution')
    plt.grid(True)
    plt.legend()
    plt.show()