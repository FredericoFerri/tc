from libs import *
import constraints
from plot import plot_solution

# Carrega os dados dos clientes do arquivo CSV
def get_clients():
  clients = np.genfromtxt('clientes.csv', delimiter=',')
  return clients

# Função para gerar uma solução qualquer
def generate_solution(clients_data, constructor_heuristic=True):
    print("Gerar solucao")
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

    # Extrai as coordenadas dos clientes do array
    client_coordinates = clients_data[:, :2]
    solution['client_coordinates'] = client_coordinates

    # Extrai a largura de banda dos clientes do array
    solution['client_bandwidth'] = clients_data[:, 2]

    if constructor_heuristic:
      return initial_solution2(clients_data, solution)

    # CÓDIGO SERA EXECUTADO SE: constructor_heuristic=False
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

    # Calcula a distancia entre todos os PAs
    for i in range(num_pa_locations):
      pa_x, pa_y = pa_coordinates[i]
      for j in range(num_pa_locations):
        paj_x, paj_y = pa_coordinates[j]
        distance = np.sqrt((pa_x - paj_x) ** 2 + (pa_y - paj_y) ** 2)
        solution['pas_distances'][i, j] = distance

    return solution

def initial_solution2(clients_data, solution):
    print("SOLUÇÃO INICIAL2")

    # Criar um DataFrame com as coordenadas
    coordenadas = pd.DataFrame(solution['client_coordinates'], columns=['x', 'y'])

    # Normalizar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(coordenadas)

    # Aplicar K-means com 30 clusters
    kmeans_30 = KMeans(n_clusters=30, random_state=random.randint(0, 10000))
    clusters_30 = kmeans_30.fit_predict(X_scaled)
    coordenadas['cluster_30'] = clusters_30 

    centroides = kmeans_30.cluster_centers_
    centroides_originais = scaler.inverse_transform(centroides) # Reverter a normalização para obter as coordenadas originais   

    # Aplicar a função a cada elemento do array
    centroides_originais = np.vectorize(round_to_nearest_5)(centroides_originais)
    #print(centroides_originais)

    solution['pa_coordinates'] = centroides_originais

    # Ativar todos os PA's 
    solution['y'].fill(1)

    # Atribuir clientes aos PA's
    client_active(solution)

    return solution

# Função para arredondar para o múltiplo de 5 mais próximo
def round_to_nearest_5(x):
    return 5 * round(x / 5)

def settle_distances_client_to_pa(solution):

    # Calcula a distancia entre cada cliente e cada PA ativo
    for i in range(num_pa_locations):
      pa_x, pa_y = solution['pa_coordinates'][i]
      for j in range(num_clients):
        client_x, client_y = solution['client_coordinates'][j]
        distance = np.sqrt((pa_x - client_x) ** 2 + (pa_y - client_y) ** 2)
        solution['client_pa_distances'][i, j] = distance

# Função para manejo de clientes entre PA's
def client_active(solution):
    
    client_coordinates = solution['client_coordinates']
    active_pa_indices = []

    # Coletar coordenadas dos PAs ativos e seus índices originais
    for i in range(num_pa_locations):
        if solution['y'][i] == 1:
            active_pa_indices.append(i)
        if solution['y'][i] == 0:
           solution['x'][i] = np.zeros(num_clients)

    # Verificar se há PAs ativos
    if len(active_pa_indices) == 0:
        print("Nenhum PA ativo.")
        return

    # Inicializar a matriz de alocação
    solution['x'] = np.zeros((num_pa_locations, num_clients))

    settle_distances_client_to_pa(solution) #calcula as distancias entre cliente e PA's (será importante para estruturas de vizinhança)

    # Atribuir cada cliente ao PA ATIVO mais próximo
    for j in range(num_clients):
        distance_to_all_pa = solution['client_pa_distances'][:, j]

        # Inicializar a menor distância e o índice do PA mais próximo
        closest_active_pa_distance = float('inf')
        closest_active_pa_index = -1
        # Iterar sobre todas as distâncias e encontrar a menor distância para um PA ativo
        for i in range(num_pa_locations):
            if solution['y'][i] == 1:  # Verifica se o PA é ativo
                if distance_to_all_pa[i] < closest_active_pa_distance:
                    closest_active_pa_distance = distance_to_all_pa[i]
                    closest_active_pa_index = i

        if(closest_active_pa_distance <= pa_coverage):
            solution['x'][closest_active_pa_index, j] = 1 


generate_solution(get_clients())
         
