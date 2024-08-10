from libs import *

criterios = ["Quantidade", "Distância", "Variação Posição", "Aumento consumo"]
pesos_criterios = np.array([
    [ 1 , 3/1, 5/1, 3/1],
    [1/3,  1 , 7/1, 3/1],
    [1/5, 1/7,  1 , 1/5],
    [1/3, 1/3, 5/1,  1 ]
])
'''
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
'''

def ahp(criterios, pesos_criterios):
    
    # Normalização da matriz
    pesos_normalizados = pesos_criterios / pesos_criterios.sum(axis=0)
    vetor_prioridades = pesos_normalizados.mean(axis=1)

    # Cálculo de consistência
    # Calculate the eigenvalue and eigenvector
    eig_val, eig_vec = np.linalg.eig(pesos_normalizados)
    max_eig_val = np.max(eig_val)
    IC = (max_eig_val - len(criterios)) / (len(criterios) - 1)
    ICA = [0, 0, 0.52, 0.89, 1.11, 1.25, 1.35, 1.40, 1.45, 1.49]  # ICAs em função da ordem da matriz - Colin (2007)
    QC = IC / ICA[len(criterios)]
    
    if QC > 0.1:
        print("Inconsistência nos julgamentos")   
    return vetor_prioridades

print(ahp(criterios, pesos_criterios))
def Gx(c1, c2, criterio=0, p=0, q=0, sigma=0):
     match criterio:
        case 0: #Critério usual
            if c1 - c2 <= 0:
               return 0
            else:
                return 1 
        
        case 1: #Critério linear
            if c1 - c2 <= 0:
               return 0
            elif c1 - c2 <= p:
                return (c1 - c2)/p
            else:
                return 1 
        case 2: #Critério degrau
            if c1 - c2 <= q:
               return 0
            elif c1 - c2 <= p:
                return 0.5
            else:
                return 1 
        case 3: #Critério trapezoidal
            if c1 - c2 <= q:
               return 0
            elif c1 - c2 <= p:
                return ((c1 - c2)- q)/(p-q)
            else:
                return 1 
        case 4: #Critério Gaussiano
            if c1 - c2 <= 0:
               return 0
            else:
                return 1 - np.exp(-(c1 - c2)**2 / (2 * sigma**2))


def promethee(criterios, pesos_criterios, solucoes):
    num_criterios = len(criterios)
    num_solucoes = len(solucoes)
    
    Preferencias = np.zeros(num_criterios, num_solucoes, num_solucoes)
    
    #Critério 1: Quantidade
    for i in range(num_solucoes):
        for j in range(num_solucoes):
            if i != j:
                c1 = np.sum(solucoes[i]['y'])
                c2 = np.sum(solucoes[j]['y'])
                Preferencias[0, i, j] = Gx(c1, c2, 1, 5) #A partir de diferença de 5 PAs, preferência total
    
    #Criterio 2: Distâncias
    for i in range(num_solucoes):
        for j in range(num_solucoes):
            if i != j:
                c1 = np.sum(np.multiply(solucoes[i]['x'], solucoes[i]['client_pa_distances']))
                c2 = np.sum(np.multiply(solucoes[j]['x'], solucoes[j]['client_pa_distances']))
                Preferencias[1, i, j] = Gx(c1, c2, 4, 0, 0, 1000)

    #Criterio 3: Variação Posição (somar as distâncias entre o cliente e o raio do seu PA caso ele desloque 5 metros para longe do PA)
    for i in range(num_solucoes):
        for j in range(num_solucoes):
            if i != j:
                ForaAlcance_i = np.multiply(solucoes[i]['x'], solucoes[i]['client_pa_distances']) + 5 - 85
                ForaAlcance_i[ForaAlcance_i < 0] = 0
                c1 = np.sum(ForaAlcance_i)
                ForaAlcance_j = np.multiply(solucoes[j]['x'], solucoes[j]['client_pa_distances']) + 5 - 85
                ForaAlcance_j[ForaAlcance_j < 0] = 0
                c2 = np.sum(ForaAlcance_j)
                Preferencias[2, i, j] = Gx(c1, c2, 1, 400) #A partir de diferença de 400m, preferência total

    #Criterio 4: Aumento Consumo em 20%
    for i in range(num_solucoes):
        for j in range(num_solucoes):
            if i != j:
                ConsumoExcesso_i = np.multiply(1.2, np.multiply(solucoes[i]['x'], solucoes[i]['client_bandwidth'])) - 54
                ConsumoExcesso_i[ConsumoExcesso_i < 0] = 0
                c1 = np.sum(ConsumoExcesso_i)
                ConsumoExcesso_j = np.multiply(1.2, np.multiply(solucoes[i]['x'], solucoes[i]['client_bandwidth'])) - 54
                ConsumoExcesso_j[ConsumoExcesso_j < 0] = 0
                c2 = np.sum(ConsumoExcesso_j)
                Preferencias[3, i, j] = Gx(c1, c2, 1, 100) #A partir de diferença de 100Mbps, preferência total

    #Calcular a soma ponderada das preferências
    PreferenciasTotal = np.zeros(num_solucoes, num_solucoes)
    for i in range(num_solucoes):
        for j in range(num_solucoes):
            SomaPreferencias = np.sum(Preferencias[:, i, j] * pesos_criterios)
            PreferenciasTotal[i, j] = SomaPreferencias / np.sum(pesos_criterios)
    
    #Calcular o fluxo de preferências
    Classificacao = np.zeros(num_solucoes)
    for i in range(num_solucoes):
        fluxo = np.sum(PreferenciasTotal[i, :]) - np.sum(PreferenciasTotal[:, i])
        Classificacao[i] = fluxo
    

    MelhorAlternativa = np.argmax(Classificacao)
    return solucoes[MelhorAlternativa]