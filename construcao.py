from libs import *
import constraints
from plot import plot_solution

# Carrega os dados dos clientes do arquivo CSV
def get_clients():
  clients = np.genfromtxt('clientes.csv', delimiter=',')
  return clients

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

    # Criar um DataFrame com as coordenadas
    coordenadas = pd.DataFrame(solution['client_coordinates'], columns=['x', 'y'])

    # Normalizar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(coordenadas)

    # Aplicar K-means com 10 clusters
    kmeans_10 = KMeans(n_clusters=30, random_state=0)
    clusters_10 = kmeans_10.fit_predict(X_scaled)
    coordenadas['cluster_10'] = clusters_10 

    centroides = kmeans_10.cluster_centers_
    centroides_originais = scaler.inverse_transform(centroides) # Reverter a normalização para obter as coordenadas originais   

    # Aplicar a função a cada elemento do array
    centroides_originais = np.vectorize(round_to_nearest_5)(centroides_originais)
    #print(centroides_originais)

    # Popular solução com PA's
    all_coordinates = []
    for coord in centroides_originais:
        all_coordinates.append(coord.tolist())  # Coordenada original
        #all_coordinates.extend(generate_additional_coordinates(coord))  # Coordenadas adicionais
        x, y = coord
        left = max(0, x - 20)
        right = min(400, x + 20)
        all_coordinates.extend([[left, y], [right, y]])

    solution['pa_coordinates'] = np.vstack(all_coordinates)

    print(solution['pa_coordinates'])

    # Ativar PA's que são centróides 
    for i in range(num_pa_locations):
       if i%3 == 0:
          solution['y'][i] = 1

    # Atribuir clientes aos PA's
    client_active(solution)

    if not constraints.constraint_min_clients_served(solution):
       print('erro!')

    #plot_solution(solution)

    return solution

# Função para arredondar para o múltiplo de 5 mais próximo
def round_to_nearest_5(x):
    return 5 * round(x / 5)

# Função para manejo de clientes entre PA's
def client_active(solution):
    
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

    # Inicializar a matriz de alocação
    num_pas = len(solution['pa_coordinates'])
    solution['x'] = np.zeros((num_pas, num_clients))

    # Atribuir cada cliente ao PA mais próximo
    for j in range(num_clients):
        client_x, client_y = client_coordinates[j] # coordenadas de cliente
        distances_to_pas = np.sqrt(np.sum((active_pa_coordinates - np.array([client_x, client_y]))**2, axis=1)) # distância de cliente a PA's
        closest_pa_index = np.argmin(distances_to_pas)
        closest_pa_distance = np.amin(distances_to_pas)
        if(closest_pa_distance < pa_coverage):
            original_pa_index = active_pa_indices[closest_pa_index]
            solution['x'][original_pa_index, j] = 1 


generate_solution(get_clients())
         
