from libs import *

# Estruturas de Vizinhança
def swap_clients_between_pas(solution):
    # Troca de Clientes entre PAs (Swap)
    new_solution = update_solution(solution)  # Criar uma cópia da solução atual
    old_solution = update_solution(solution) # Criar uma cópia da solução atual

    active_pas = np.sum(new_solution['y'])

    client_coordinates = new_solution['client_coordinates']
    active_pa_coordinates = []
    active_pa_indices = []

    # Coletar coordenadas dos PAs ativos e seus índices originais
    for i in range(num_pa_locations):
        if solution['y'][i] == 1:
            active_pa_coordinates.append(solution['pa_coordinates'][i])
            active_pa_indices.append(i)        
        if solution['y'][i] == 0:
           solution['x'][i] = np.zeros(num_clients)



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


       

    # Selecionar aleatoriamente dois PAs ativos diferentes    
    pa_indices = np.random.choice(np.arange(active_pas.astype(int)), size=2, replace=False)
    pa1_index, pa2_index = pa_indices

    # Selecionar aleatoriamente um cliente atribuído ao PA1 e outro ao PA2
    client_indices_pa1 = np.where(new_solution['x'][pa1_index] == 1)[0]
    client_indices_pa2 = np.where(new_solution['x'][pa2_index] == 1)[0]

    if len(client_indices_pa1) > 0 and len(client_indices_pa2) > 0:
        client_index_pa1 = np.random.choice(client_indices_pa1)
        client_index_pa2 = np.random.choice(client_indices_pa2)

        # Realizar a troca dos clientes entre os PAs
        new_solution['x'][pa1_index, client_index_pa1] = 0
        new_solution['x'][pa2_index, client_index_pa2] = 0
        new_solution['x'][pa1_index, client_index_pa2] = 1
        new_solution['x'][pa2_index, client_index_pa1] = 1

    new_solution = feasibility(new_solution, old_solution)

    return new_solution

def add_or_remove_pas(solution):
    # Adição ou Remoção de PAs
    new_solution = update_solution(solution)  # Criar uma cópia da solução atual
    old_solution = update_solution(solution) # Criar uma cópia da solução atual

    # Selecionar aleatoriamente um número de PAs a adicionar ou remover
    num_pas_to_add_or_remove = np.random.randint(1, num_pa_locations + 1)

    # Selecionar aleatoriamente quais PAs adicionar ou remover
    pa_indices = np.random.choice(np.arange(num_pa_locations), size=num_pas_to_add_or_remove, replace=False)

    # Ativar ou desativar os PAs selecionados
    for pa_index in pa_indices:
        new_solution['y'][pa_index] = 1 - new_solution['y'][pa_index]
    
    new_solution = feasibility(new_solution, old_solution)

    return new_solution

def shift_pa_positions(solution):
    # Movimento dos PAs (Shift)
    new_solution = update_solution(solution)  # Criar uma cópia da solução atual
    old_solution = update_solution(solution) # Criar uma cópia da solução atual

    # MUDAR GERAÇÃO DE NOVA POSIÇÃO
    # Gerar uma nova posição para cada PA

    client_coordinates = new_solution['client_coordinates']
    pa_coordinates = new_solution['pa_coordinates']

                   


    #active_pas = np.sum(new_solution['y'])
    
    
    #pa_sobra = int((active_pas - num_pa_locations) / active_pas)
    #if ((active_pas - num_pa_locations) % active_pas) > 0: 
    #    pa_extra = ((active_pas - num_pa_locations) % active_pas)


    print(pa_coordinates)
    

      


    #new_pa_coordinates = np.random.randint(0, 80, size=(num_pa_locations, 2)) * 5  # 80 é o tamanho do grid em metros

    # Atualizar as coordenadas dos PAs na solução
    new_solution['pa_coordinates'] = pa_coordinates

    # Recalcular as distâncias entre os clientes e os PAs com as novas posições
    for i in range(num_pa_locations):
        pa_x, pa_y = pa_coordinates[i]
        for j in range(num_clients):
            client_x, client_y = new_solution['client_coordinates'][j]
            distance = np.sqrt(((pa_x - client_x) + (pa_y - client_y))**2, axis=1)
            new_solution['client_pa_distances'][i, j] = distance

    new_solution = feasibility(new_solution, old_solution)

    return new_solution

def add_new_pa(solution):
    # Adição de um PA novo
    new_solution = update_solution(solution)  # Criar uma cópia da solução atual
    old_solution = update_solution(solution) # Criar uma cópia da solução atual

    new_solution = kmeans(new_solution)
        
    new_solution = feasibility(new_solution, old_solution)

    return new_solution


def neighborhood_change(solution, neighborhood):

  #print(type(solution['fitness']))

  match neighborhood:
    case 1:
      return add_new_pa(solution)
    #case 2:
    #  return swap_clients_between_pas(solution)
    #case 3:
      #return add_or_remove_pas(solution)
    #case 2:
      #print("ALGO ERRADO 4ª Vizinhaça")
      #return shift_pa_positions(solution)
    case _:
        return solution