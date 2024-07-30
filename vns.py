from libs import *

# Algoritmo para otimizar cada função objetivo individualmente
def bvns_method(objective_function, constraints, construct_heuristc=False, max_iter=100, neighborhood_max = 3):

    progress = {
        'fitness': np.zeros(max_iter),
        'penalty': np.zeros(max_iter),
        'penalty_fitness': np.zeros(max_iter)
    }

    # Atribui os dados dos clientes
    clients_data = get_clients()

    # Gerar uma solução aleatória viável
    solution = generate_solution(clients_data)
    solution = objective_function(solution, constraints)


    for i in range(max_iter):

      #print(f"iteração {i}:\n")
      neighborhood = 1

      progress['fitness'][i] = solution['fitness']
      progress['penalty'][i] = solution['penalty']
      
      while neighborhood <= neighborhood_max:

        solution = update_solution(solution)

        new_solution = neighborhood_change(solution, neighborhood)
        
        # Calcula a função objetivo da solução gerada        
        new_solution = objective_function(new_solution, constraints)

        # Compara o fitness da solução nova com a atual com as soluções da vizinhança
        solution, neighborhood = solution_check(new_solution, solution, neighborhood)


    print("\nFIM DE EXECUÇÃO\n")

    solution = update_solution(solution)

    print("SOLUÇÃO FINAL")
    print("FIT   : ", solution['fitness'])
    print("SOMA Y: ", np.sum(solution['y']))
    tot = 0
    for i in range(num_pa_locations):
       if solution['y'][i] == 1:
          tot += np.sum(solution['x'][i])
    
    print("TOTAL CLIENTES", np.sum(tot))

    print("\n----------------------------------------------------------\n")
    return solution, progress