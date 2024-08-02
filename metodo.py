from libs import *
import construcao 
from vizinhanca import neighborhood_change
from plot import plot_solution

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

    #solution['fitness'] = 0
    #solution['penalty'] = 0
    #solution['penalty_fitness'] = 0

    # Calculo da função objetivo
    solution['fitness'] = np.sum(np.multiply(solution['client_pa_distances'], solution['x']))
    #print(f"FITNESS SOLUÇÃO: {solution['fitness']}")

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints)
    #print(f"PENALIDADE SOLUÇÃO: {solution['penalty']}")

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

    return solution

# Aplicar as penalidades para as violações de restrições
def penalty_method(solution, constraints):
    penalty = 0
    iterador = 1
    for constraint in constraints:
      if not constraint(solution):
        print(f"Contraint problematica: {iterador}")
        penalty += 1
      iterador += 1

    return penalty

# Atualizar a melhor solução encontrada e altera a vizinhança se necessário
def solution_check(new_solution, solution, neighborhood):

    if (new_solution['penalty'] < solution['penalty']):
        neighborhood = 1
        return new_solution, neighborhood
    elif (new_solution['fitness'] < solution['fitness'] and new_solution['penalty'] == solution['penalty']):
        neighborhood = 1
        return new_solution, neighborhood
    else:
        neighborhood += 1
        return solution, neighborhood

# Algoritmo para otimizar cada função objetivo individualmente
def bvns_method(objective_function, constraints, construct_heuristc=False, max_iter=1000, neighborhood_max = 1):

    progress = {
        'fitness': np.zeros(max_iter),
        'penalty': np.zeros(max_iter),
        'penalty_fitness': np.zeros(max_iter)
    }

    # Gerar uma solução aleatória viável
    solution = construcao.generate_solution(construcao.get_clients())
    solution = objective_function(solution, constraints)

    for i in range(max_iter):
      neighborhood = 1

      progress['fitness'][i] = solution['fitness']
      progress['penalty'][i] = solution['penalty']
      #progress['fitness'][i] = solution['fitness']

      while neighborhood <= neighborhood_max:

        new_solution = neighborhood_change(solution, neighborhood)

        # Avaliar a solução
        new_solution = objective_function(new_solution, constraints)

        # Compara a solução nova com a atual com as soluções da vizinhança
        solution, neighborhood = solution_check(new_solution, solution, neighborhood)

    print("\n----------------------------------------------------------\n")

    #solution = copy.deepcopy(solution)
    print("FIT   : ", solution['fitness'])
    print("SOMA Y: ", np.sum(solution['y']))
    return solution, progress