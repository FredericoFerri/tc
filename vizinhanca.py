from libs import *
from construcao import client_active, settle_distance_for_single_pa

def clients_check(solution, previous_solution = None):

    clients = np.sum(solution['x'])

    if clients >= (0.98 * num_clients) and clients <= num_clients:
        pass
    else:
        client_active(solution)

#apta para uso 
def swap_pas(solution):
    new_solution = copy.deepcopy(solution)

    #------------------------------------------------------------------
    # (1) Selecionar aleatoriamente um de três PA's com menor quantidade de clientes
    #------------------------------------------------------------------
    # Calcula o número total de clientes para cada PA, considerando apenas PAs ativos
    total_clients = np.zeros(num_pa_locations)
    for i in range(num_pa_locations):
        if new_solution['y'][i] == 1:  # Verifica se o PA está ativo
            total_clients[i] = np.sum(new_solution['x'][i, :])

    # Filtra apenas os PAs ativos e seus índices
    active_indices = np.where(new_solution['y'] == 1)[0]
    active_total_clients = total_clients[active_indices]

    if len(active_total_clients) >= 3:
        # Encontra os 3 PAs ativos com menor quantidade de clientes
        top_3_least_clients_indices = np.argsort(active_total_clients)[:3]  # Índices dos 3 menores valores entre os ativos
        top_3_active_indices = active_indices[top_3_least_clients_indices]  # Índices dos 3 menores valores no array original de PAs

        # Seleciona aleatoriamente um PA entre os 3
        pa_to_deactivate = np.random.choice(top_3_active_indices)
    else:
        print("Erro! Não há PA's suficientes para operação de SWAP")
        print("Não há PAs inativos disponíveis para ativar.")
        print(f"solution['fitness']: {new_solution['fitness']}")
        print(f"solution['penalty']: {new_solution['penalty']}")
        print(f"solution['y']: {new_solution['y']}")
        exit()
        return solution

    #------------------------------------------------------------------
    # (2) Selecionar um PA inativo aleatório e ativar
    #------------------------------------------------------------------
    # Filtra apenas os PAs inativos e seus índices
    inactive_indices = np.where(new_solution['y'] == 0)[0]

    if len(inactive_indices) > 0:
        # Seleciona aleatoriamente um PA inativo
        pa_to_activate = np.random.choice(inactive_indices)
    else:
        print("Não há PAs inativos disponíveis para ativar.")
        return solution
    

    #------------------------------------------------------------------
    # (3) Ativar e desativar PA's selecionados
    #------------------------------------------------------------------ 
    new_solution['y'][pa_to_deactivate] = 0
    new_solution['x'][pa_to_deactivate, :] = 0
    new_solution['y'][pa_to_activate] = 1 

    #settle_distance_for_single_pa(new_solution, pa_to_activate)  # Descomente se necessário
    client_active(new_solution)  # Atualiza as alocações de clientes

    return new_solution

def add_or_remove_pas(solution):
    # Adição ou Remoção de PAs
    new_solution = copy.deepcopy(solution)  # Criar uma cópia da solução atual

    #------------------------------------------------------------------
    # (1) Selecionar aleatoriamente um de cinco PA's com menor banda utilizada
    #------------------------------------------------------------------
    # Calcula a demanda total para cada PA, considerando apenas PAs ativos
    demanda_total = np.zeros(num_pa_locations)
    for i in range(num_pa_locations):
        if new_solution['y'][i] == 1:  # Verifica se o PA está ativo
            demanda_total[i] = np.sum(new_solution['client_bandwidth'][new_solution['x'][i, :] == 1])

    # Filtra apenas os PAs ativos e seus índices
    ativos_indices = np.where(new_solution['y'] == 1)[0]
    ativos_demanda = demanda_total[ativos_indices]

    # Encontra os 5 PAs com menor demanda entre os ativos
    top_5_less_indices = np.argsort(ativos_demanda)[:5]  # Índices dos 5 menores valores entre os ativos
    top_5_ativos_indices = ativos_indices[top_5_less_indices]  # Índices dos 5 maiores valores no array original de PAs
    top_5_demanda = ativos_demanda[top_5_less_indices]  # Demanda dos 5 PAs com maior demanda

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

    if len(top_3_indices) != 3:
        print(f"new_solution['fitness] = {new_solution['fitness']}")
        print(f"solution['y']: {solution['y']}")
        print(f"distance_to_ativos = {distances_to_ativos}")
        print(f"ativos_indices = {ativos_indices}")
        exit()
    else:
        demanda_banda = np.zeros(3)
        # Calcula a demanda de banda consumida para cada um dos 3 PAs mais próximos
        for idx, pa in enumerate(top_3_indices):
            demanda = np.sum(new_solution['client_bandwidth'][new_solution['x'][pa, :] == 1])
            demanda_banda[idx] = demanda

        pa_menor_demanda_idx = np.argmin(demanda_banda)

        pa2_index = top_3_indices[pa_menor_demanda_idx] 

    #------------------------------------------------------------------
    # (3) Posicionar um PA entre os dois PA's 
    #------------------------------------------------------------------  
    pa1_to_be_removed_coords = new_solution['pa_coordinates'][pa1_index]
    pa2_to_keep_coords = new_solution['pa_coordinates'][pa2_index]

    # direção de movimento do PA com base em ponto médio entre clientes
    new_pa_coords = (pa1_to_be_removed_coords + pa2_to_keep_coords) / 2
    new_pa_coords = np.clip(new_pa_coords, 0, None)
    new_pa_coords = np.round(new_pa_coords / 5) * 5 #arredondamento para grid 5x5

    #------------------------------------------------------------------
    # (4) Adicionar PA entre PA's OU Desativar PA1 e Alterar as distâncias entre clientes e PA na solução 
    #------------------------------------------------------------------  

    distance_between_pas = distances[pa2_index]
    
    new_pa_index = 0
    if distance_between_pas >= pa_coverage:  
    #Adicionar PA entre os dois PA's
        if np.any(new_solution['y'] == 0):
        # Ativa PA inativo e o posiciona 
            # Encontra os índices dos PAs inativos
            inactive_indexes = np.where(new_solution['y'] == 0)[0]
    
            # Calcula a soma das distâncias para cada PA inativo
            sum_distances = np.sum(new_solution['client_pa_distances'][inactive_indexes, :], axis=1)
    
            # Encontra o índice do PA inativo com a maior soma das distâncias
            pa_max_sum_distances = inactive_indexes[np.argmax(sum_distances)]
            new_pa_index = pa_max_sum_distances

            # Ativação de PA
            new_solution['y'][new_pa_index] = 1

        else:
        # Altera posição de PA ativo 
            # Encontra o PA que atende menos clientes
            total_clients = np.zeros(num_pa_locations)
    
            for i in range(num_pa_locations):
                total_clients[i] = np.sum(new_solution['x'][i, :])
            
            # Encontrar o PA ativo com a menor quantidade de clientes
            pa_min_clients_index = np.argmin(total_clients)
            new_pa_index = pa_min_clients_index
  
        # Adicionar PA entre pa1 e pa2
        new_solution['pa_coordinates'][new_pa_index] = new_pa_coords  
        
    else:
    #Remove PA1 e move PA2 para new_pa_coords
        print(f"Quantidade de PA's antes de desligar PA: {np.sum(new_solution['y'])}")
        print(f"fitness antes de desligar PA: {new_solution['fitness']}")
        new_solution['y'][pa1_index] = 0
        new_solution['x'][pa1_index, :] = 0
        new_solution['pa_coordinates'][pa2_index] = new_pa_coords
        new_pa_index = pa2_index

    settle_distance_for_single_pa(new_solution,new_pa_index)
    client_active(new_solution)

    return new_solution

def move_pa_solution(solution):
    new_solution = copy.deepcopy(solution)
    num_pa_locations = len(new_solution['pa_coordinates'])
    
    #------------------------------------------------------------------
    # (1) Selecionar aleatoriamente um PA ativo
    #------------------------------------------------------------------
    # Filtra apenas os PAs ativos e seus índices
    active_indices = np.where(new_solution['y'] == 1)[0]
    
    if len(active_indices) == 0:
        print("Erro! Não há PA's ativos suficientes para movimentação.")
        return solution

    # Seleciona aleatoriamente um PA ativo
    pa_to_move = np.random.choice(active_indices)
    
    #------------------------------------------------------------------
    # (2) Movimentar o PA selecionado sutilmente
    #------------------------------------------------------------------
    # Definir limites de movimentação
    min_move_amount = 6
    max_move_amount = 12
    move_amount = np.random.randint(min_move_amount, max_move_amount + 1)
    
    # Obter as coordenadas atuais do PA
    current_coords = new_solution['pa_coordinates'][pa_to_move]
    
    # Gerar deslocamento aleatório nas direções x e y
    delta_x = np.random.randint(-move_amount, move_amount + 1)*5
    delta_y = np.random.randint(-move_amount, move_amount + 1)*5
    
    # Calcular novas coordenadas
    new_x = np.clip(current_coords[0] + delta_x, 0, 400)
    new_y = np.clip(current_coords[1] + delta_y, 0, 400)
    
    # Atualizar as coordenadas do PA na nova solução
    new_solution['pa_coordinates'][pa_to_move] = [new_x, new_y]
    
    # Opcional: recalcular as distâncias e atualizar alocações de clientes
    settle_distance_for_single_pa(new_solution, pa_to_move)
    client_active(new_solution)
    
    return new_solution

def get_pas_closer(solution):
    # Aproxima PAs com com baixo uso de banda a PA's com alto uso de banda
    new_solution = copy.deepcopy(solution)  # Criar uma cópia da solução atual

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
    # (3) Aproximar PA de menor banda para PA de maior banda
    #------------------------------------------------------------------
    pa1_bigger_bandwidth_coords = new_solution['pa_coordinates'][pa1_index]
    pa2_lower_bandwidth_coords = new_solution['pa_coordinates'][pa2_index]

    # direção de movimento do PA com base em ponto médio entre clientes
    new_pa_coords = (pa1_bigger_bandwidth_coords + pa2_lower_bandwidth_coords) / 3
    new_pa_coords = np.clip(new_pa_coords, 0, None)
    new_pa_coords = np.round(new_pa_coords / 5) * 5 #arredondamento para grid 5x5

    #------------------------------------------------------------------
    # (4) Alterar as coordenadas de PA e distâncias entre clientes e PA na solução 
    #------------------------------------------------------------------
    # Atualizar a posição do PA
    new_solution['pa_coordinates'][pa2_index] = new_pa_coords

    # Atualizar as distâncias de PA a clientes
    settle_distance_for_single_pa(new_solution,pa2_index)

    client_active(new_solution)

    return new_solution
    
def shift_pa_positions(solution):
    # Movimento dos PAs (Shift)
    new_solution = copy.deepcopy(solution)  # Criar uma cópia da solução atual
    num_pa_locations = len(new_solution['pa_coordinates'])  # Definindo o número de PAs a partir das coordenadas
 
    #------------------------------------------------------------------
    # (1) Obter cinco PA's com maior variância de distâncias entre clientes e PA e escolher aleatoriamente um deles
    #------------------------------------------------------------------
    # Calcular a variância das distâncias para cada PA, considerando apenas PAs ativos
    variancia_distancias = np.zeros(num_pa_locations)
    for i in range(num_pa_locations):
        if new_solution['y'][i] == 1:
            pa_clients = new_solution['x'][i, :] == 1
            if np.sum(pa_clients) > 1:  # Verifica se o PA tem mais de um cliente
                variancia_distancias[i] = np.var(new_solution['client_pa_distances'][i, pa_clients])

    # Filtrar apenas os PAs ativos e seus índices
    ativos_indices = np.where(new_solution['y'] == 1)[0]
    ativos_variancia = variancia_distancias[ativos_indices]

    # Encontra os 5 PAs com maior variância entre os ativos
    top_5_variancia_indices = np.argsort(ativos_variancia)[-5:]  # Índices dos 5 maiores valores entre os ativos
    top_5_ativos_indices = ativos_indices[top_5_variancia_indices]  # Índices dos 5 maiores valores no array original de PAs
    #top_5_variancia = ativos_variancia[top_5_variancia_indices]  # Variância dos 5 PAs com maior variância

    # Escolher aleatoriamente um dos 5 PAs com maior variância
    selected_pa = np.random.choice(top_5_ativos_indices)

    #------------------------------------------------------------------
    # (2) Obter os seis clientes mais distantes do PA e os dois mais distantes entre si 
    #------------------------------------------------------------------ 
    # seis clientes mais distantes de PA
    all_pa_clients = np.where(new_solution['x'][selected_pa, :] == 1)[0]
    most_distant_clients_Index = all_pa_clients[np.argsort(-new_solution['client_pa_distances'][selected_pa, all_pa_clients])[:6]]

    # Dois clientes mais próximos entre si
    client1_index = 0
    client2_index = 0
    min_distance = float('inf')
    for i in range(len(most_distant_clients_Index)):
        for j in range(i + 1, len(most_distant_clients_Index)):
            client1_coords = new_solution['client_coordinates'][most_distant_clients_Index[i]]
            client2_coords = new_solution['client_coordinates'][most_distant_clients_Index[j]]
            distance = np.sqrt((client1_coords[0] - client2_coords[0]) ** 2 + (client1_coords[1] - client2_coords[1]) ** 2)
            if distance < min_distance: 
                min_distance = distance
                client1_index = most_distant_clients_Index[i]
                client2_index = most_distant_clients_Index[j]

    #------------------------------------------------------------------
    # (3) Mover o PA em direção ao cliente mais distante com base nos dois clientes escolhidos 
    #------------------------------------------------------------------
    pa_coords = new_solution['pa_coordinates'][selected_pa]

    # direção de movimento do PA com base em ponto médio entre clientes
    mid_point = (new_solution['client_coordinates'][client1_index] + new_solution['client_coordinates'][client2_index]) / 2
    direction = mid_point - pa_coords

    # Normalizar a direção
    direction_norm = np.linalg.norm(direction)
    if direction_norm != 0:
        direction /= direction_norm

    distance_client1 = new_solution['client_pa_distances'][selected_pa, client1_index]
    distance_client2 = new_solution['client_pa_distances'][selected_pa, client2_index]
    move_distance = (distance_client1 + distance_client2) / 3  

    new_pa_coords = pa_coords + direction * (move_distance) 
    new_pa_coords = np.clip(new_pa_coords, 0, None)
    new_pa_coords = np.round(new_pa_coords / 5) * 5 #arredondamento para grid 5x5

    # Verificar se new_pa_coords contém valores válidos
    if np.any(np.isnan(new_pa_coords)) or np.any(np.isinf(new_pa_coords)):
        raise ValueError("Coordenadas inválidas para o novo PA: {}".format(new_pa_coords))

    #------------------------------------------------------------------
    # (4) Alterar as coordenadas de PA e distâncias entre clientes e PA na solução 
    #------------------------------------------------------------------
    # Atualizar a posição do PA
    new_solution['pa_coordinates'][selected_pa] = new_pa_coords

    # Atualizar as distâncias de PA a clientes
    settle_distance_for_single_pa(new_solution,selected_pa)

    client_active(new_solution)

    return new_solution

def neighborhood_change(solution, neighborhood):
  
  #ordem swap_clients_between_pas >> shift_pa_positions >> add_or_remove_pas
  match neighborhood:
    case 1:
        return shift_pa_positions(solution)
    case 2:
        return move_pa_solution(solution)
    case 3:
        return add_or_remove_pas(solution)

#def neighborhood_change(solution, neighborhood):
  
  #ordem swap_clients_between_pas >> shift_pa_positions >> add_or_remove_pas
  #match neighborhood:
    #case 1:
        #return shift_pa_positions(solution) 
    #case 2:
        #return add_or_remove_pas(solution)    