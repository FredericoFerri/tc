from libs import *

# Construção da heuristica da solução inicial


### A heuristica construtiva da solucao inicial será utilizar um numero de clusters definido pelo minimo de pontos de acesso (PA) 
### necessarios para atender a banda de consumo de todos os clientes (C)


# Normalizar os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar K-means com 10 clusters
kmeans_10 = KMeans(n_clusters=10, random_state=0)
clusters_10 = kmeans_10.fit_predict(X_scaled)
