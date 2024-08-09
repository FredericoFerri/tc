from libs import *
import construcao 
from vizinhanca import neighborhood_change
from plot import plot_solution

# Função objetivo 1: Minimizar a quantidade de PAs ativos
def objective_function_1(solution, constraints):

    solution['fitness'] = 0
    solution['penalty'] = 0
    #solution['penalty_fitness'] = 0

    # Calculo da função objetivo
    solution['fitness'] = np.sum(solution['y'])

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints)

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']


# Função objetivo 2: Minimizar a soma total das distâncias entre os PAs ativos e clientes atendidos
def objective_function_2(solution, constraints):

    solution['fitness'] = 0
    solution['penalty'] = 0
    #solution['penalty_fitness'] = 0

    #CÁLCULO DO FITNESS
    active_pa_indices = np.where(solution['y'] == 1)[0]
    # Inicializa a soma total das distâncias
    sum_active_pa_distances = 0
    
    for pa_index in active_pa_indices:
        clients_associated = np.where(solution['x'][pa_index, :] == 1)[0]
        
        # Soma as distâncias desses clientes para o PA ativo
        if len(clients_associated) > 0:
            distances = solution['client_pa_distances'][pa_index, clients_associated]
            sum_active_pa_distances += np.sum(distances)
    
    solution['fitness'] = sum_active_pa_distances

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints)
    #print(f"PENALIDADE SOLUÇÃO: {solution['penalty']}")

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']


# Aplicar as penalidades para as violações de restrições
def penalty_method(solution, constraints):
    penalty = 0
    iterador = 1
    for constraint in constraints:
      if not constraint(solution):
        #print(f"Contraint problematica: {iterador}")
        penalty += 1
      iterador += 1

    return penalty

# Atualizar a melhor solução encontrada e altera a vizinhança se necessário
def solution_check(new_solution, solution):
    # Aceita se a nova solução tiver menor penalidade
    if new_solution['penalty'] < solution['penalty']:
        return True

    # Aceita se a penalidade for a mesma e o fitness for melhor
    if new_solution['penalty'] == solution['penalty'] and new_solution['fitness'] <= solution['fitness']:
        if (np.sum(new_solution['x']) >= np.sum(solution['x'])) or np.sum(new_solution['x']) >= (0.98 * num_clients) :
            return True
        else:
           return False
    return False
    
# Algoritmo para otimizar cada função objetivo individualmente
def bvns_method(objective_function, constraints, construct_heuristc=False, max_iter=1000, neighborhood_max = 3):

    progress = {
        'fitness': np.zeros(max_iter),
        'penalty': np.zeros(max_iter),
        'penalty_fitness': np.zeros(max_iter)
    }

    obj_function = 0
    if objective_function == objective_function_1:
        obj_function = 1
    elif objective_function == objective_function_2:
        obj_function = 2

    solution = construcao.generate_solution(construcao.get_clients(),obj_function)
    objective_function(solution, constraints)

    for i in range(max_iter):
      print(i)
      neighborhood = 1

      progress['fitness'][i] = solution['fitness']
      progress['penalty'][i] = solution['penalty']

      while neighborhood <= neighborhood_max:

        new_solution = neighborhood_change(solution, neighborhood,obj_function)

        # Avaliar a solução
        objective_function(new_solution, constraints)

        # Compara a solução nova com a atual com as soluções da vizinhança
        if solution_check(new_solution, solution):
            print(f"solution['fitness']: {solution['fitness']}")
            print(f"solution['penalty']: {solution['penalty']}")
            print(f"Num PA's: {np.sum(solution['y'])}")
            print(f"solution['y']: {solution['y']}")
            solution = copy.deepcopy(new_solution)
            print(f"new_solution['fitness']: {solution['fitness']}")
            print(f"new_solution['penalty']: {solution['penalty']}")
            print(f"new_solution Num PA's: {np.sum(solution['y'])}")
            print(f"new_solution['y']: {solution['y']}")
            #plot_solution(solution)
            #neighborhood = 1
        #else:
        neighborhood += 1
    
    print("\n----------------------------------------------------------\n")
    return solution, progress