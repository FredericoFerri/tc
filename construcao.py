from libs import *
from definitions import num_clients, num_pa_locations, pa_capacity, pa_coverage, pa_exposure, exposure_coefficient

### A heuristica construtiva da solucao inicial será utilizar um numero de clusters definido pelo minimo de pontos de acesso (PA) 
### necessarios para atender a banda de consumo de todos os clientes (C)

def initial_solution(clients_data, solution):

    # Extrai as coordenadas dos clientes do array
    client_coordinates = clients_data[:, :2]
    solution['client_coordinates'] = client_coordinates

    # Extrai a largura de banda dos clientes do array
    solution['client_bandwidth'] = clients_data[:, 2]

    # Verifica o numero minimo de PAs necessários para atender todos os clientes
    pa_min = round(np.sum(solution['client_bandwidth']) / pa_capacity)
    
    coord_kmeans= pd.DataFrame(solution['client_coordinates'], columns=['x', 'y'])
   
    # Normalizar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(coord_kmeans)

    # Aplicar K-means para formar os clusters
    kmeans = KMeans(n_clusters=pa_min, random_state=0)
    clusters = kmeans.fit_predict(X_scaled)
   
    solution['pa_coordinates'] = kmeans.cluster_centers_

    solution['pa_coordinates'] = scaler.inverse_transform(solution['pa_coordinates']) # Reverter a normalização para obter as coordenadas originais   

    solution['pa_coordinates'] = round_to_nearest_5(solution['pa_coordinates'])

    # Gerar coordenadas aleatorias para os outros PAs com resolução de 5 metros
    pa_coordinates = np.random.randint(0, 80, size=((num_pa_locations - pa_min), 2)) * 5  # 80 é o tamanho do grid

    # Adicionar as coordenadas aleatórias com as dos centroides do k-means aos PAs  
    solution['pa_coordinates'] = np.vstack((solution['pa_coordinates'],pa_coordinates))
    pa_coordinates = solution['pa_coordinates']

    # Ativa todos os PAs gerados pelo k-means
    # Coletar coordenadas dos PAs ativos e seus índices originais
    for i in range(num_pa_locations):
        if i < pa_min:
            solution['y'][i] = 1
        else:
            solution['y'][i] = 0

    # Calcula a distancia entre cada cliente e cada PA
    for i in range(num_pa_locations):
      pa_x, pa_y = solution['pa_coordinates'][i]
      for j in range(num_clients):
          client_x, client_y = client_coordinates[j]
          distance = np.sqrt((pa_x - client_x) ** 2 + (pa_y - client_y) ** 2)
          solution['client_pa_distances'][i, j] = distance

    # Calcula a distancia entre todos os PAs
    for i in range(num_pa_locations):
      pa_x, pa_y = pa_coordinates[i]
      for j in range(num_pa_locations):
        paj_x, paj_y = pa_coordinates[j]
        distance = np.sqrt((pa_x - paj_x) ** 2 + (pa_y - paj_y) ** 2)
        solution['pas_distances'][i, j] = distance
   
    # Atribuir cada cliente ao PA mais próximo
    for j in range(num_clients):
        pa_distance = []
        for i in range(pa_min):          
            pa_distance.append(solution['client_pa_distances'][i,j])
            closest_pa_index = np.argmin(pa_distance)   
        solution['x'][closest_pa_index, j] = 1

    return solution


# Função para gerar uma solução qualquer
def generate_solution(clients_data, constructor_heuristic=True):
    # Inicialize as variáveis de decisão
    solution = {
        'x': np.zeros((num_pa_locations, num_clients)),  # Variáveis de decisão para atribuição de clientes a PAs
        'y': np.zeros(num_pa_locations),  # Variáveis de decisão para ativação de PAs
        'client_coordinates': np.zeros((num_clients, num_clients)),  # Armazena as posições (x,y) de cada cliente
        'client_pa_distances': np.zeros((num_pa_locations, num_clients)),  # Armazena a distancia entre cliente e PA
        'client_bandwidth': np.zeros(num_clients), # Armazena a largura de banda necessária de cada cliente
        'penalty': np.zeros(0), # Armazena a penalidade da solução
        'fitness': np.zeros(0), # Armazena o ajuste da solução
        'penalty_fitness': np.zeros(0), # Armazena o ajuste somado a penalidade da solução
        'pas_distances': np.zeros((num_pa_locations, num_pa_locations))
    }

    if constructor_heuristic:
      return initial_solution(clients_data, solution)
    
    # Extrai as coordenadas dos clientes do array
    client_coordinates = clients_data[:, :2]
    solution['client_coordinates'] = client_coordinates

    # Extrai a largura de banda dos clientes do array
    solution['client_bandwidth'] = clients_data[:, 2]

    # Gerar coordenadas aleatorias para os PAs com resolução de 5 metros
    pa_coordinates = np.random.randint(0, 80, size=(num_pa_locations, 2)) * 5  # 80 é o tamanho do grid
    solution['pa_coordinates'] = pa_coordinates

    # Ativa aleatoriamente um número máximo de PAs
    num_active_pas = np.random.randint(1, num_pa_locations + 1)
    active_pas_indices = np.random.choice(num_pa_locations, num_active_pas, replace=False)
    solution['y'][active_pas_indices] = 1

    # Atribui cada cliente a um PA aleatoriamente e deixa ativo
    for j in range(num_clients):
        i = np.random.randint(num_pa_locations)  # Seleciona um PA aleatório
        solution['x'][i, j] = 1  # Atribui o cliente j ao PA i

    # Calcula a distancia entre cada cliente e cada PA ativo
    for i in range(num_pa_locations):
      pa_x, pa_y = pa_coordinates[i]
      for j in range(num_clients):
        client_x, client_y = client_coordinates[j]
        distance = np.sqrt((pa_x - client_x) ** 2 + (pa_y - client_y) ** 2)
        solution['client_pa_distances'][i, j] = distance

    return solution