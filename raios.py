import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Caminho para CSV
file_path = "C:/Users/Midian/Documents/Midian/Trabalho de Extensão - Estácio/BIG DATA PYTHON/dados python/lightning-data.csv"


# Lendo o arquivo CSV
df = pd.read_csv(file_path, header=0)  # header=0 se o CSV tiver cabeçalho

# Convertendo a coluna de nuvem/solo para booleano
df.iloc[:, 4] = df.iloc[:, 4].astype(str).str.lower().map({'true': True, 'false': False})

# Contando raios que ficam na nuvem e tocam o solo
cloud_strikes_count = df[df.iloc[:, 4] == True].shape[0]
ground_strikes_count = df[df.iloc[:, 4] == False].shape[0]

# Filtrando os dados para incluir apenas os raios que tocaram o solo (quinta coluna == False)
ground_strikes = df[df.iloc[:, 4] == False]

# Contando raios positivos e negativos
positive_strikes_count = ground_strikes[ground_strikes.iloc[:, 3] > 0].shape[0]
negative_strikes_count = ground_strikes[ground_strikes.iloc[:, 3] < 0].shape[0]

# Filtrando os raios negativos
negative_strikes = ground_strikes[ground_strikes.iloc[:, 3] < 0]

# Convertendo a coluna de tempo para datetime
negative_strikes.iloc[:, 0] = pd.to_datetime(negative_strikes.iloc[:, 0])

# Ordenando por data e hora
negative_strikes = negative_strikes.sort_values(by=negative_strikes.columns[0])

# Inicializando listas para armazenar as primeiras descargas e as descargas subsequentes
first_strikes = []
subsequent_strikes = []

# Iterando sobre as linhas do DataFrame para identificar descargas
previous_time = None

for index, row in negative_strikes.iterrows():
    current_time = row[negative_strikes.columns[0]]
    
    if previous_time is None or (current_time - previous_time) > timedelta(seconds=1):
        # É uma primeira descarga
        first_strikes.append(row)
    else:
        # É uma descarga de retorno subsequente
        subsequent_strikes.append(row)
    
    previous_time = current_time

# Convertendo listas de volta para DataFrames
first_strikes_df = pd.DataFrame(first_strikes)
subsequent_strikes_df = pd.DataFrame(subsequent_strikes)

# Contando as descargas
first_strikes_count = len(first_strikes_df)
subsequent_strikes_count = len(subsequent_strikes_df)

# Calculando a média dos picos de correntes
first_strikes_mean_current = first_strikes_df.iloc[:, 3].mean()
subsequent_strikes_mean_current = subsequent_strikes_df.iloc[:, 3].mean()

# Exibindo os resultados
print(f'Quantidade de raios Intranuvem: {cloud_strikes_count}')
print(f'Quantidade de raios Nuvem-Solo: {ground_strikes_count}')
print(f'Quantidade de raios Nuvem-Solo Positivos: {positive_strikes_count}')
print(f'Quantidade de raios Nuvem-Solo Negativos: {negative_strikes_count}')
print(f'Quantidade de primeiras descargas (raios negativos): {first_strikes_count}')
print(f'Quantidade de descargas de retorno subsequentes (raios negativos): {subsequent_strikes_count}')
print(f'Média dos picos de correntes das primeiras descargas (raios negativos): {first_strikes_mean_current}')
print(f'Média dos picos de correntes das descargas de retorno subsequentes (raios negativos): {subsequent_strikes_mean_current}')

# Plotando gráficos de pizza para porcentagens
plt.figure(figsize=(18, 18))

# Gráfico de pizza para raios que ficam na nuvem
plt.subplot(3, 1, 1)
plt.pie([cloud_strikes_count, ground_strikes_count], autopct='%1.1f%%', colors=['gold', 'lightcoral'])
plt.title('Porcentagem de Raios Intranuvem e Nuvem-Solo')
plt.legend([f'Intranuvem (N={cloud_strikes_count})', f'Nuvem-Solo (N={ground_strikes_count})'], loc='upper left')

# Gráfico de pizza para raios Nuvem-Solo divididos pela polaridade
plt.subplot(3, 1, 2)
plt.pie([positive_strikes_count, negative_strikes_count], autopct='%1.1f%%', colors=['red', 'lightblue'])
plt.title('Porcentagem de Raios Nuvem-Solo por Polaridade')
plt.legend([f'Positivos (N={positive_strikes_count})', f'Negativos (N={negative_strikes_count})'], loc='upper left')

# Gráfico de pizza para primeiras descargas vs. descargas subsequentes
plt.subplot(3, 1, 3)
plt.pie([first_strikes_count, subsequent_strikes_count], autopct='%1.1f%%', colors=['orange', 'lightgreen'])
plt.title('Porcentagem de Primeiras Descargas vs. Descargas Subsequentes')
plt.legend([f'Primeiras Descargas (N={first_strikes_count})', f'Descargas Subsequentes (N={subsequent_strikes_count})'], loc='upper left')

plt.tight_layout()
plt.savefig('graficos_pizza_quadrados.jpg', dpi=300)
plt.show()

# Plotando os histogramas
plt.figure(figsize=(14, 6))

# Histograma das primeiras descargas
plt.subplot(1, 2, 1)
plt.hist(first_strikes_df.iloc[:, 3], bins=30, color='blue', edgecolor='black')
plt.axvline(first_strikes_mean_current, color='red', linestyle='dashed', linewidth=1)
plt.title('Histograma das Primeiras Descargas de Retorno')
plt.xlabel('Picos de Corrente (kA)')
plt.ylabel('Frequência')
plt.text(0.25, 0.95, f'N={first_strikes_count}\nMA={first_strikes_mean_current:.2f}',
         verticalalignment='top', horizontalalignment='right',
         transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.5, boxstyle='round,pad=0.5'))

# Histograma das descargas de retorno subsequentes
plt.subplot(1, 2, 2)
plt.hist(subsequent_strikes_df.iloc[:, 3], bins=30, color='green', edgecolor='black')
plt.axvline(subsequent_strikes_mean_current, color='red', linestyle='dashed', linewidth=1)
plt.title('Histograma das Descargas de Retorno Subsequentes')
plt.xlabel('Picos de Corrente (kA)')
plt.ylabel('Frequência')
plt.text(0.25, 0.95, f'N={subsequent_strikes_count}\nMA={subsequent_strikes_mean_current:.2f}',
         verticalalignment='top', horizontalalignment='right',
         transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.5, boxstyle='round,pad=0.5'))

plt.tight_layout()
plt.savefig('histogramas_descargas.jpg', dpi=300)
plt.show()
