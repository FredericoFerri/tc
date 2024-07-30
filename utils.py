from libs import *

def update_solution(new_solution):
   return copy.deepcopy(new_solution)

def round_to_nearest_5(x):
    return 5 * np.round(x / 5)

# Carrega os dados dos clientes do arquivo CSV
def get_clients():
  clients = np.genfromtxt('clientes.csv', delimiter=',')
  return clients


def kmeans(solution, num_pas=None):

  num_pas = np.sum(solution['y'])
  coord_kmeans= pd.DataFrame(solution['client_coordinates'], columns=['x', 'y'])

  if num_pas < num_pa_locations:
    
    num_pas += 1

    # Normalizar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(coord_kmeans)

    # Aplicar K-means para formar os clusters
    kmeans = KMeans(n_clusters=int(num_pas), random_state=0)
    clusters = kmeans.fit_predict(X_scaled)
  
    solution['pa_coordinates'] = kmeans.cluster_centers_

    solution['pa_coordinates'] = scaler.inverse_transform(solution['pa_coordinates']) # Reverter a normalização para obter as coordenadas originais   

    solution['pa_coordinates'] = round_to_nearest_5(solution['pa_coordinates'])

    for i in range(num_pa_locations):
      if i < num_pas:
          solution['y'][i] = 1
      else:
          solution['y'][i] = 0
    
    return solution
  
  print("Numero de PAs Exedido")

  return

    

      
    
