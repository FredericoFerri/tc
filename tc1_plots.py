from libs import *

import matplotlib.pyplot as plt
import random

# Graficos para visualização das soluções

# Função para plotar os PAs e os clientes em um grid
def plot_progress(progress, i):
    # Criar uma nova figura
    plt.figure(figsize=(12, 5))

    # Plotar resultados
    for i in range(i):
      plt.plot(progress[0]['fitness'], label='Fitness 1')
      plt.plot(progress[1]['fitness'], label='Fitness 2')
      plt.plot(progress[2]['fitness'], label='Fitness 3')
      plt.plot(progress[3]['fitness'], label='Fitness 4')
      plt.plot(progress[4]['fitness'], label='Fitness 5')
      # plt.scatter(client_coordinates[:, 0], client_coordinates[:, 1], marker='o', color='blue', label='Clientes')

    # Adicionar legendas e título
    plt.xlabel('Iterações')
    plt.ylabel('Numero de PAs')
    plt.title('Convergência das soluções')
    #plt.legend()

    # Mostrar o gráfico
    plt.show()

def cor_vibrante():
    # Gerar valores RGB mais vibrantes
    r = random.randint(180, 255)  # Valor de vermelho entre 180 e 255
    g = random.randint(0, 255)    # Valor de verde entre 0 e 255
    b = random.randint(0, 255)    # Valor de azul entre 0 e 255

    # Converter para formato hexadecimal
    cor_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return cor_hex


# Função para plotar os PAs e os clientes em um grid
def plot_solution(solution, client_coordinates):
    # Criar uma nova figura
    plt.figure(figsize=(8, 8))

    # Plotar o grid
    plt.grid(True, linestyle='--', color='gray', alpha=0.5)

    # Definindo as cores RGB para os 30 pontos de acesso
    cores_acesso = [cor_vibrante() for _ in range(30)]

    # Plotar os PAs
    pa_coordinates = solution['pa_coordinates']
    posicao_cliente = solution['client_coordinates']

    tot = 0
    sem = 0
    for i in range(num_pa_locations):
      if solution['y'][i] == 1:
        tot += np.sum(solution['x'][i])
      else:
         sem += np.sum(solution['x'][i])

    print("CLIENTES CONECTADOS", tot)
    print("CLIENTES SEM CONEXÃO", sem)

    # Plotar os clientes
    for i in range(num_pa_locations):
      if solution['y'][i] == 1:
        plt.scatter(pa_coordinates[i, 0], pa_coordinates[i, 1], marker='s', c='black', label='Pontos de Acesso')        
        for j in range(num_clients):
          if solution['x'][i, j] == 1:
            plt.scatter(posicao_cliente[j, 0], posicao_cliente[j, 1], marker='o', label='Clientes')
            plt.plot([pa_coordinates[i, 0], posicao_cliente[j, 0]], [pa_coordinates[i, 1], posicao_cliente[j, 1]], 'gray')

    # Definir o raio do círculo
    raio_circulo = pa_coverage

    # Plotar círculos ao redor dos pontos de acesso
    for i in range(num_pa_locations):
      if solution['y'][i] == 1:
          pa_x = pa_coordinates[i, 0]
          pa_y = pa_coordinates[i, 1]
          circulo = plt.Circle((pa_x, pa_y), raio_circulo, color='blue', alpha=0.3)
          plt.gca().add_patch(circulo)

    # Adicionar legendas e título
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Pontos de Acesso e Clientes')


    #plt.legend()

    # Mostrar o gráfico
    plt.show()

