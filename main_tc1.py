from libs import *


# Chamar o algoritmo de Penalidade para otimizar cada função objetivo individualmente
# Para a função objetivo 1
result = []
progress = {}
best_solution = {}
for i in range(5):
    best_solution[i], progress[i] = bvns_method(objective_function_1, constraints)
    print("FITNESS: ", best_solution[i]['fitness'])
    print("PENALIDADE: ",best_solution[i]['penalty'])
    print("FIT+PEN: ",best_solution[i]['penalty_fitness'])
    result.append(best_solution[i]['penalty_fitness'])
    print("num PAs: ", i, np.sum(best_solution[i]['y']))
    #print("PAs coord: ", i, best_solution['pa_coordinates'])

print('\n--- MELHOR SOLUÇÃO de f1 ENCONTRADA ---\n')
print('O valor MIN encontrado foi:', np.min(result))
print('O valor STD encontrado foi:', np.std(result))
print('O valor MAX encontrado foi:', np.max(result))
# Plotar curva de convergencia
#plot_progress(progress,1000)


# Carrega os dados dos clientes do arquivo CSV
clients_data = get_clients()

# Extrai as coordenadas dos clientes do array
client_coordinates = clients_data[:, :2]

# Plotar a solução da função objetivo 1
for i in range(5):
   plot_solution(best_solution[i], client_coordinates)