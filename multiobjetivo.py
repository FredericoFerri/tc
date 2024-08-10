from libs import *
from metodo import *


'''
escolha uma das funções para ser otimizada (A), com a outra como restrição (B)
main_e-restrito:
    Pegar o melhor resultado de cada otimização mono-objetiva
    MinimosMaximos (solution_1, solution_2)
    for rep in range(5):
        for i in range(10):
            multi_constraints = constraints + constraint_function_B
            (alpha variando de 0.05 a 0.95, intervalos de 0.1: dez resultados)
            realizar a otimização da função A, com as restrições de multi_constraints
    Serão geradas 5 fronteiras de 10 pontos, plotar elas sobre uma mesma figura
'''