import numpy as np
import copy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd

# # Define os parâmetros do problema
num_clients = 495
num_pa_locations = 30
pa_capacity = 54  # Capacidade de cada PA
pa_coverage = 85  # Raio de cobertura de cada PA
pa_exposure = 1  # Exposição nominal do PA
exposure_coefficient = 1  # Coeficiente de exposição