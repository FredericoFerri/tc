from libs import *
from fobj import objective_function_1, objective_function_2
from utils import update_solution

# certifica que todos os clientes estão vincluados a um PA ativo

def feasibility(nova, old = None):

    solution = update_solution(nova)
    previous_solution = update_solution(old)

    clients = np.sum(solution['x'])
    
    if clients < (0.98 * num_clients) or clients > num_clients or (lambda i,j: (solution['client_pa_distances'][i,j] > 85) for i in range(num_pa_locations) for j in range(num_clients)):        
        client_active_check(solution)  
    
    solution = objective_function_1(solution, constraints)
    
    if solution['fitness'] >=  previous_solution['fitness'] and solution['penalty_fitness'] > previous_solution['penalty_fitness']:
        return previous_solution
    
    return solution
    
def solution_check(new_solution, solution, neighborhood):

    nova = update_solution(new_solution)
    antiga = update_solution(solution)
    
    # Atualizar a melhor solução encontrada e altera a vizinhança se necessário
    if (nova['penalty'] < antiga['penalty']):
        neighborhood = 1
        return nova, neighborhood
    elif (nova['fitness'] < antiga['fitness'] and nova['penalty'] == antiga['penalty']):
        neighborhood = 1
        return nova, neighborhood
    else:
        neighborhood += 1
        return antiga, neighborhood

def client_active_check(solution):
    
    client_coordinates = solution['client_coordinates']
    active_pa_coordinates = []
    active_pa_indices = []

    # Coletar coordenadas dos PAs ativos e seus índices originais
    for i in range(num_pa_locations):
        if solution['y'][i] == 1:
            active_pa_coordinates.append(solution['pa_coordinates'][i])
            active_pa_indices.append(i)        
        if solution['y'][i] == 0:
           solution['x'][i] = np.zeros(num_clients)

    # Convertendo a lista para um array numpy para cálculos de distância
    active_pa_coordinates = np.array(active_pa_coordinates)

    # Verificar se há PAs ativos
    if len(active_pa_coordinates) == 0:
        print("Nenhum PA ativo.")
        return

    # Atribuir cada cliente ao PA ativo mais próximo
    for j in range(num_clients):
        client_x, client_y = client_coordinates[j]
        distances_to_pas = np.sqrt(np.sum((active_pa_coordinates - np.array([client_x, client_y]))**2, axis=1))
        closest_pa_index = np.argmin(distances_to_pas)
        original_pa_index = active_pa_indices[closest_pa_index]        

        if distances_to_pas[closest_pa_index] > pa_coverage:         
            distances_to_pas = np.delete(distances_to_pas, closest_pa_index)   
            closest_pa_index = np.argmin(distances_to_pas)
            original_pa_index = active_pa_indices[closest_pa_index]

        solution['x'][original_pa_index, j] = 1
        
