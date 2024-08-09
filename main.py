from libs import *
import metodo
from constraints import constraints
from metodo import objective_function_1,objective_function_2

# Chamar o algoritmo de Penalidade para otimizar cada função objetivo individualmente
result = []
progress = {}
best_solution = {}

for i in range(5): #ALTERAR RANGE 1 PARA 5
    best_solution[i], progress[i] = metodo.bvns_method(objective_function_2, constraints)
    print("FITNESS: ", best_solution[i]['fitness'])
    print("PENALIDADE: ",best_solution[i]['penalty'])
    print("FIT+PEN: ",best_solution[i]['penalty_fitness'])
    result.append(best_solution[i]['penalty_fitness'])
    print("num PAs: ", i, np.sum(best_solution[i]['y']))
    plot_solution(best_solution[i])
    #print("PAs coord: ", i, best_solution['pa_coordinates'])

print('\n--- MELHOR SOLUÇÃO de f1 ENCONTRADA ---\n')
print('O valor MIN encontrado foi:', np.min(result))
print('O valor STD encontrado foi:', np.std(result))
print('O valor MAX encontrado foi:', np.max(result))

# Plotar a solução da função objetivo 1
plot_progress(progress,5)

