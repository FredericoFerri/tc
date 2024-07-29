from libs import *
from construcao import client_active

def clients_check(solution, previous_solution = None):

    clients = np.sum(solution['x'])

    #if solution['fitness'] != np.sum(solution['y']):
    #    previous_solution['y'] = solution['y'].copy()
    
    if clients >= (0.98 * num_clients) and clients <= num_clients:
        pass
    else:
        client_active(solution)

# Estruturas de Vizinhança
def swap_clients_between_pas(solution): # ESTRUTURA DE VIZINHANÇA DESABILITADA A PRINCIPIO 
    # Troca de Clientes entre PAs (Swap)
    new_solution = solution.copy()  # Criar uma cópia da solução atual

    # Selecionar aleatoriamente dois PAs diferentes
    pa_indices = np.random.choice(np.arange(num_pa_locations), size=2, replace=False)
    pa1_index, pa2_index = pa_indices

    # Selecionar aleatoriamente um cliente atribuído ao PA1 e outro ao PA2
    client_indices_pa1 = np.where(solution['x'][pa1_index] == 1)[0]
    client_indices_pa2 = np.where(solution['x'][pa2_index] == 1)[0]

    if len(client_indices_pa1) > 0 and len(client_indices_pa2) > 0:
        client_index_pa1 = np.random.choice(client_indices_pa1)
        client_index_pa2 = np.random.choice(client_indices_pa2)

        # Realizar a troca dos clientes entre os PAs
        new_solution['x'][pa1_index, client_index_pa1] = 0
        new_solution['x'][pa2_index, client_index_pa2] = 0
        new_solution['x'][pa1_index, client_index_pa2] = 1
        new_solution['x'][pa2_index, client_index_pa1] = 1

    return new_solution

def add_or_remove_pas(solution):
    # Adição ou Remoção de PAs
    new_solution = solution.copy()  # Criar uma cópia da solução atual

    # Selecionar aleatoriamente um número de PAs a adicionar ou remover
    num_pas_to_add_or_remove = 1#np.random.randint(1, num_pa_locations + 1)

    # Selecionar aleatoriamente quais PAs adicionar ou remover
    pa_indices = np.random.choice(np.arange(num_pa_locations), size=num_pas_to_add_or_remove, replace=False)

    # ESCOLHER CINCO PA's menos importantes 
    for i in range(num_pa_locations):
        np.sum(solution['x'][i] * solution['client_bandwidth'])
        
        
    # REMOVER PA's com menor quantidade de clientes 
    # REMOVER PA's com menor uso da banda

    # ESCOLHER CINCO PA'S COM ALTA DEMANDA E ADICIONAR PA PERTO 
    # TRAÇAR SEGMENTO DE RETA ENTRE DOIS PA's  

    # Ativar ou desativar os PAs selecionados
    for pa_index in pa_indices:
        new_solution['y'][pa_index] = 1 - new_solution['y'][pa_index]
    
    client_active(solution)

    return new_solution

def shift_pa_positions(solution):
    # Movimento dos PAs (Shift)
    new_solution = solution.copy()  # Criar uma cópia da solução atual

    # MUDAR GERAÇÃO DE NOVA POSIÇÃO
    # Gerar uma nova posição para cada PA
    #---------------------------------------------
    # alterar essa movimentação dos PA's
    #---------------------------------------------
    new_pa_coordinates = np.random.randint(0, 80, size=(num_pa_locations, 2)) * 5  # 80 é o tamanho do grid em metros

    # Atualizar as coordenadas dos PAs na solução
    new_solution['pa_coordinates'] = new_pa_coordinates

    client_active(solution)

    return new_solution

def neighborhood_change(solution, neighborhood):

  match neighborhood:
    case 1:
        return shift_pa_positions(solution)
    case 2:
        return add_or_remove_pas(solution)
    #case 3:
        #return shift_pa_positions(solution)
        #return swap_clients_between_pas(solution)