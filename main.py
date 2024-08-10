from libs import *
import metodo
from constraints import constraints,multiconstraints
from metodo import objective_function_1,objective_function_2,objective_function_weighted_sum
import multiobjetivo
import globals

def minimos_maximos (solution_1, solution_2):
    globals.min_val1 = np.sum(solution_1['y']) #Mínimo função objetivo 1
    globals.max_val1 = np.sum(solution_2['y']) #Máximo função objetivo 1
    globals.min_val2 = np.sum(np.multiply(solution_2['client_pa_distances'], solution_2['x'])) #Mínimo resultado função objetivo 2
    globals.max_val2 = np.sum(np.multiply(solution_1['client_pa_distances'], solution_1['x'])) #Máximo resultado função objetivo 2


def change_alpha (new_alpha):
    globals.alpha = new_alpha

# Chamar o algoritmo de Penalidade para otimizar cada função objetivo individualmente
result_1 = []
progress_1 = {}
best_solution_1 = {}


for i in range(5): #ALTERAR RANGE 1 PARA 5
    best_solution_1[i], progress_1[i] = metodo.bvns_method(objective_function_1, constraints)
    print("FITNESS: ", best_solution_1[i]['fitness'])
    print("PENALIDADE: ",best_solution_1[i]['penalty'])
    print("FIT+PEN: ",best_solution_1[i]['penalty_fitness'])
    result_1.append(best_solution_1[i]['penalty_fitness'])
    print("num PAs: ", i, np.sum(best_solution_1[i]['y']))
    #plot_solution(best_solution_1[i])
    #print("PAs coord: ", i, best_solution['pa_coordinates'])

print('\n--- MELHOR SOLUÇÃO de f1 ENCONTRADA ---\n')
print('O valor MIN encontrado foi:', np.min(result_1))
print('O valor STD encontrado foi:', np.std(result_1))
print('O valor MAX encontrado foi:', np.max(result_1))

# Plotar a solução da função objetivo 1
plot_progress(progress_1,5)


result_2 = []
progress_2 = {}
best_solution_2 = {}

for i in range(5): #ALTERAR RANGE 2 PARA 5
    best_solution_2[i], progress_2[i] = metodo.bvns_method(objective_function_2, constraints)
    print("FITNESS: ", best_solution_2[i]['fitness'])
    print("PENALIDADE: ",best_solution_2[i]['penalty'])
    print("FIT+PEN: ",best_solution_2[i]['penalty_fitness'])
    result_2.append(best_solution_2[i]['penalty_fitness'])
    print("num PAs: ", i, np.sum(best_solution_2[i]['y']))
    plot_solution(best_solution_2[i])
    #print("PAs coord: ", i, best_solution['pa_coordinates'])

print('\n--- MELHOR SOLUÇÃO de f2 ENCONTRADA ---\n')
print('O valor MIN encontrado foi:', np.min(result_2))
print('O valor STD encontrado foi:', np.std(result_2))
print('O valor MAX encontrado foi:', np.max(result_2))

# Plotar a solução da função objetivo 2
plot_progress(progress_2,5)

#OTIMIZACAO MULTIOBJETIVO 
best_solution_1_final = best_solution_1[np.argmin(result_1)]
best_solution_2_final = best_solution_2[np.argmin(result_2)]

minimos_maximos(best_solution_1_final, best_solution_2_final)


result_w = []
progress_w = {}
best_solution_w = {}

# SOMA PONDERADA 
new_alpha = 0.1
for i in range(5): 
    change_alpha(new_alpha)
    best_solution_w[i], progress_w[i] = metodo.bvns_method(objective_function_weighted_sum, constraints)
    new_alpha = new_alpha + 0.2
    result_w.append(best_solution_w[i]['penalty_fitness'])
    print("num PAs: ", i, np.sum(best_solution_w[i]['y']))
    #plot_solution(best_solution_w[i])


result_e = []
progress_e = {}
best_solution_e = {}

# e-Restrito
new_alpha = 0.1
for i in range(5): 
    change_alpha(new_alpha)
    best_solution_e[i], progress_e[i] = metodo.bvns_method(objective_function_2, multiconstraints)
    new_alpha = new_alpha + 0.2
    result_e.append(best_solution_e[i]['penalty_fitness'])
    print("num PAs: ", i, np.sum(best_solution_e[i]['y']))
    #plot_solution(best_solution_e[i])


# PLOT DE FRONTEIRAS PARETO
pareto_fronts_weighted_sum = []  # Armazena as 5 fronteiras de Pareto de soma ponderada
pareto_fronts_e_restrito = []  # Armazena as 5 fronteiras de Pareto de e-restrito  

for i in range(0,5):
    # Adiciona todas as tuplas diretamente à lista principal
    print("\n--------------------------------")
    print(f"{i}\nbest_solution_e['fitness']: {best_solution_e[i]['fitness']}")
    print(f"Num PA's: {np.sum(best_solution_e[i]['y'])}")
    print(f"best_solution_e['distance']: {best_solution_e[i]['distances']}")
    print(f"best_solution_e['penalty']: {best_solution_e[i]['penalty']}")

for i in range(0,5):
    # Adiciona todas as tuplas diretamente à lista principal
    pareto_fronts_e_restrito.append((np.sum(best_solution_e[i]['y']), best_solution_e[i]['distances']))
    #pareto_fronts_weighted_sum.append((np.sum(best_solution_w[i]['y']), best_solution_w[i]['distances']))

# Plotar as fronteiras de Pareto
plot_pareto_fronts(pareto_fronts_weighted_sum, "Fronteiras de Pareto - Soma Ponderada")
plot_pareto_fronts([pareto_fronts_e_restrito], "Fronteiras de Pareto - e-Restrito")
