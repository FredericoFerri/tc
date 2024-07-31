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
def swap_clients_between_pas(solution): 
    # Troca de Clientes entre PAs (Swap)
    
    new_solution = solution.copy() 

    #------------------------------------------------------------------
    # (1) Selecionar aleatoriamente um de cinco PA's com maior banda utilizada
    #------------------------------------------------------------------
    # Calcula a demanda total para cada PA, considerando apenas PAs ativos
    demanda_total = np.zeros(num_pa_locations)
    for i in range(num_pa_locations):
        if new_solution['y'][i] == 1:  # Verifica se o PA está ativo
            demanda_total[i] = np.sum(new_solution['client_bandwidth'][new_solution['x'][i, :] == 1])

    # Filtra apenas os PAs ativos e seus índices
    ativos_indices = np.where(new_solution['y'] == 1)[0]
    ativos_demanda = demanda_total[ativos_indices]

    # Encontra os 5 PAs com maior demanda entre os ativos
    top_5_indices = np.argsort(ativos_demanda)[-5:]  # Índices dos 5 maiores valores entre os ativos
    top_5_ativos_indices = ativos_indices[top_5_indices]  # Índices dos 5 maiores valores no array original de PAs
    top_5_demanda = ativos_demanda[top_5_indices]  # Demanda dos 5 PAs com maior demanda

    pa1_index = np.random.choice(top_5_ativos_indices) 

    #------------------------------------------------------------------
    # (2) Selecionar o PA com menor demanda dentre os três mais próximos de pa1_index
    #------------------------------------------------------------------
    distances = np.sqrt(np.sum((new_solution['pa_coordinates'] - new_solution['pa_coordinates'][pa1_index]) ** 2, axis=1))

    ativos_indices = ativos_indices[ativos_indices != pa1_index]

    # Calcula as distâncias para os PAs ativos excluindo o PA selecionado
    distances_to_ativos = distances[ativos_indices]

    # Encontra os índices dos três PAs ativos mais próximos
    top_3_indices = np.argsort(distances_to_ativos)[:3] 

    demanda_banda = np.zeros(3)
    # Calcula a demanda de banda consumida para cada um dos 3 PAs mais próximos
    for idx, pa in enumerate(top_3_indices):
        demanda = np.sum(new_solution['client_bandwidth'][new_solution['x'][pa, :] == 1])
        demanda_banda[idx] = demanda

    pa_menor_demanda_idx = np.argmin(demanda_banda)

    pa2_index = top_3_indices[pa_menor_demanda_idx] 
    
    #------------------------------------------------------------------
    # (3) escolher três clientes de pa1_index e passar para pa2_index
    #------------------------------------------------------------------
    clients_pa1 = np.where(new_solution['x'][pa1_index, :] == 1)[0]

    # encontra os índices relativos dos três clientes
    clients_to_pa2_relative = np.argsort(new_solution['client_pa_distances'][pa2_index, clients_pa1])[:3]

    #encontra os índices dos três clientes de pa1 mais próximos de pa2
    clients_to_pa2 = clients_pa1[clients_to_pa2_relative]
    
    #swap de clientes
    new_solution['x'][pa1_index, clients_to_pa2] = 0
    new_solution['x'][pa2_index, clients_to_pa2] = 1

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
        return swap_clients_between_pas(solution)
    case 2:
        return add_or_remove_pas(solution)
    #case 3:
        #return shift_pa_positions(solution)
        #return swap_clients_between_pas(solution)