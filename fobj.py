from libs import *
from constrains import constraints_name

def penalty_method(solution, constraints):

  # Aplicar as penalidades para as violações de restrições
    penalty = 0
    iterador = 0
    for constraint in constraints:
      if not constraint(solution):
          penalty += 100
          #print(constraints_name[iterador])

      iterador += 1

   # print('\n')

    return penalty

# Função objetivo 1: Minimizar a quantidade de PAs ativos
def objective_function_1(solution, constraints):

    solution['fitness'] = 0
    solution['penalty'] = 0
    solution['penalty_fitness'] = 0

    # Calculo da função objetivo
    solution['fitness'] = np.sum(solution['y'])

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints)

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

    return solution

# Função objetivo 2: Minimizar a soma total das distâncias entre os PAs ativos e clientes atendidos
def objective_function_2(solution, constraints):

    solution['fitness'] = 0
    solution['penalty'] = 0
    solution['penalty_fitness'] = 0

    # Calculo da função objetivo
    solution['fitness'] = np.sum(np.multiply(solution['client_pa_distances'], solution['x']))

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints)

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

    return solution
