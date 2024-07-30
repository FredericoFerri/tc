from libs import *
from definitions import num_clients, num_pa_locations, pa_capacity, pa_coverage, pa_exposure, exposure_coefficient

# Restrições
def constraint_min_clients_served(solution):
    # Restrição R1: Garantir que o percentual mínimo de clientes seja atendido
    return np.sum(solution['x']) >= (0.98 * num_clients)

def constraint_capacity(solution):
    # Restrição R2: Garantir que a capacidade dos PAs ativos não seja violada
    for i in range(num_pa_locations):
        if solution['y'][i] == 1: 
            for j in range(num_clients):
                if solution['client_bandwidth'][j] > pa_capacity:
                    return False
    return True

def constraint_coverage(solution):
    # Restrição R3: Garantir que PAs ativos só atendam clientes que estejam dentro do seu raio de cobertura
    for i in range(num_pa_locations):
        if solution['y'][i] == 1: 
            for j in range(num_clients):
                if solution['x'][i, j] == 1:
                    if solution['client_pa_distances'][i,j] > pa_coverage:
                        #print("cliente ", j," longe do PA ",i," distancia de ",solution['client_pa_distances'][i,j]," metros")
                        return False
    return True

def constraint_exposure(solution):
    # Restrição R4: Garantir que exposição acumulada de cada cliente à rede de PAs ativos seja no mínimo 5% do coeficiente de exposição
    
    pa_cover = pa_exposure * np.sum(solution['y'])
    
    for j in range(num_clients):
        client_cover = 0
        for i in range(num_pa_locations):
            if solution['y'][i] == 1:
                if solution['client_pa_distances'][i, j] != 0:
                    client_cover += pa_cover / solution['client_pa_distances'][i, j]
        if client_cover < 0.05 * exposure_coefficient:
            return False
    return True

def constraint_unique_assignment(solution):
    # Restrição R5: Garantir que cada cliente seja atribuído a no máximo um PA
    return np.all(np.sum(solution['x'], axis=0) <= 1)

def constraint_max_pas(solution):
    # Restrição R6: Garantir que o número máximo de PAs ativos não seja violado
    return np.sum(solution['y']) <= num_pa_locations

def constraint_binary_variables(solution):
    # Restrições R7 e R8: Definir o domínio das variáveis de otimização do problema
    return np.all(np.logical_or(solution['x'] == 0, solution['x'] == 1)) and np.all(np.logical_or(solution['y'] == 0, solution['y'] == 1))

def constraint_pa_coordinates(solution):
    # Restrição R9: Garantir que as coordenadas dos pontos de acesso sejam múltiplos de 5
    pa_coordinates = solution['pa_coordinates']
    return np.all(pa_coordinates % 5 == 0)


constraints = [constraint_min_clients_served, constraint_capacity, constraint_coverage, constraint_exposure, constraint_unique_assignment, constraint_max_pas, constraint_binary_variables, constraint_pa_coordinates]

constraints_name = ['constraint_min_clients_served', 'constraint_capacity', 'constraint_coverage', 'constraint_exposure', 'constraint_unique_assignment', 'constraint_max_pas', 'constraint_binary_variables', 'constraint_pa_coordinates']