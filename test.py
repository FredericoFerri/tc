import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Carregar os dados
data = pd.read_csv('clientes.csv', header=None)
data.columns = ['x', 'y', 'consumo']

# Selecionar as colunas 'x' e 'y' para a clusterização
X = data[['x', 'y']]

# Normalizar os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar K-means com 10 clusters
kmeans_10 = KMeans(n_clusters=10, random_state=0)
clusters_10 = kmeans_10.fit_predict(X_scaled)

# Adicionar os clusters aos dados originais
data['cluster_10'] = clusters_10

# Plotar os clusters para 10 clusters
plt.figure(figsize=(8, 6))
plt.scatter(data['x'], data['y'], c=data['cluster_10'], cmap='tab10')
plt.title('K-means com 10 Clusters')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# Obter as coordenadas das centróides
centroides = kmeans_10.cluster_centers_

# Reverter a normalização para obter as coordenadas originais
centroides_originais = scaler.inverse_transform(centroides)

# Mostrar as coordenadas das centróides
print(centroides_originais)