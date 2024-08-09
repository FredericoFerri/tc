from libs import *
import constraints
from plot import plot_solution

# Carrega os dados dos clientes do arquivo CSV
def get_clients():
  clients = np.genfromtxt('clientes.csv', delimiter=',')
  return clients

# Função para gerar uma solução qualquer
def generate_solution(clients_data,obj_function,constructor_heuristic=True):
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
        if obj_function == 1:
            return initial_solution1(solution)
        elif obj_function == 2:
            return initial_solution2(solution)
    else:
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

def initial_solution1(solution):
    print("SOLUÇÃO INICIAL1")

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

    solution['pa_coordinates'] = np.round(centroides_originais / 5) * 5 #arredondamento para grid 5x5 centroides_originais

    settle_distances_client_to_pa(solution)

    # Ativa 15 PA's aleatoriamente
    num_active_pas = np.random.randint(10, 16)
    active_indices = np.random.choice(num_pa_locations, num_active_pas, replace=False)

    # Ative os PAs correspondentes aos índices gerados
    solution['y'][active_indices] = 1

    # Atribuir clientes aos PA's
    client_active(solution)

    plot_solution(solution)

    return solution

def initial_solution2(solution):
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

    settle_distances_client_to_pa(solution)

    # Atribuir clientes aos PA's
    client_active(solution)

    plot_solution(solution)

    return solution

# Função para arredondar para o múltiplo de 5 mais próximo
def round_to_nearest_5(x):
    return 5 * np.round(x / 5)

def settle_distance_for_single_pa(solution, pa_index):
   pa_x, pa_y = solution['pa_coordinates'][pa_index]
   for j in range(num_clients):
        client_x, client_y = solution['client_coordinates'][j]
        distance = np.sqrt((pa_x - client_x) ** 2 + (pa_y - client_y) ** 2)
        solution['client_pa_distances'][pa_index, j] = distance

def settle_distances_client_to_pa(solution):
    # Calcula a distancia entre cada cliente e cada PA
    for i in range(num_pa_locations):
      settle_distance_for_single_pa(solution,i)

# Função para manejo de clientes entre PA's
def client_active(solution):
    # Coletar coordenadas dos PAs ativos e seus índices originais
    active_pa_indices = []
    active_pa_indices = np.where(solution['y'] == 1)[0]

    # Verificar se há PAs ativos
    if len(active_pa_indices) == 0:
        print("Nenhum PA ativo.")
        exit()

    # Inicializar a matriz de alocação
    solution['x'] = np.zeros((num_pa_locations, num_clients))

    settle_distances_client_to_pa(solution) #calcula as distancias entre cliente e PA's (será importante para estruturas de vizinhança)

    # Atribuir cada cliente ao PA ATIVO mais próximo
    for j in range(num_clients):
        # Verificar se o cliente já está atribuído a um PA
        if np.sum(solution['x'][:, j]) > 0:
            continue  # Cliente já atribuído, pula para o próximo cliente

        distance_to_all_pa = solution['client_pa_distances'][:, j]

        active_pa_distances = distance_to_all_pa[active_pa_indices]

        # Index e valor de distância mínimo de PA ativo
        min_distance_index = np.argmin(active_pa_distances)
        closest_active_pa_distance = active_pa_distances[min_distance_index]

        # Converter o índice filtrado de volta para o índice original em `solution['y']`
        closest_active_pa_index = active_pa_indices[min_distance_index]

        # Verifica se a distância mais próxima está dentro do limite de cobertura
        if closest_active_pa_distance <= pa_coverage:
                solution['x'][closest_active_pa_index, j] = 1

         
