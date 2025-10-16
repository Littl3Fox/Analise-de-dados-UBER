# %% [markdown]
# # Análise de dados da UBER
# 
# ## O objetivo dessa análise é responder a 5 perguntas:
# 
# 1. Qual a porcentagem de corridas canceladas por motoristas, clientes, corridas completas, corridas incompletas e de motoristas não encontrados?
# 2. Quais os  motivos para motoristas cancelarem a corrida?
# 3. Quais os  motivos para clientes cancelarem a corrida?
# 4. Quais são os top 3 locais cujo maior motivo de cancelamento é "passageiros de mais"?
# 5. Qual o preço médio das tarifas das viagens completas por tipo de veículo?
# 
# ### Para responder às perguntas, alguns passos serão implemetados:
# 
# 1. Descrever o dataset
# 2. Carregar, tratar e limpar o dataset
# 3. Explorar o dataset(análise gráfica)
# 4. Preparar a modelagem
# 

# %% [markdown]
# ### Bibliotecas usadas:
# 1. pandas
# 2. matplotlib
# 3. seaborn
# 

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ### Carregar o dataset

# %%
df = pd.read_csv("archive/ncr_ride_bookings.csv")
df.head()

# %%
df.info()

# %%
df.describe()

# %% [markdown]
# Verifico se existem dados duplicados

# %%
df[df.duplicated()]

# %% [markdown]
# No caso abaixo é verificado quais são os casos em que nenhum valor é estipulado para a viagem.

# %%
df2 = df[df["Booking Value"].isna()]
df2["Booking Status"].unique()



# %% [markdown]
# ## Colunas 

# %%
for key in df.keys():
    print(key)

# %% [markdown]
# ## Data Transformation
# ### Para responder às perguntas, são necessárias as seguintes colunas:
# 
# 1. Booking Status - Status da reserva (Concluída, Cancelada pelo Cliente, Cancelada pelo Motorista etc.)  
# 2. Reason for cancelling by Customer - Motivo do cancelamento pelo cliente  
# 3. Driver Cancellation Reason - Motivo do cancelamento pelo motorista  
# 4. Pickup Location - Local de início da corrida  
# 5. Booking Value - Valor da tarifa cobrada pela Uber  
# 6. Vehicle Type - Tipo de veículo (Go Mini, Go Sedan, Auto, eBike/Bike, UberXL, Premier Sedan)  
# 
# 
# 
# #### 1º Passo: Analisar as colunas
# 
# Apesar de as colunas *Reason for cancelling by Customer*, *Driver Cancellation Reason* e *Booking Value* terem valores vazios, não é necessário remover essas linhas, pois o fato de estarem vazias indica que as viagens foram completas ou canceladas por algum motivo. Logo, esses valores vazios têm significado.
# 
# #### 2º Passo: Plano de ataque para transformar os dados e deixá-los pronto para análise
# 
# Tendo em mente a análise das colunas foi definido o seguinte plano:
# 
# 1. Descartar as colunas que não serão usadas.
# 

# %% [markdown]
# ### Descatar as colunas que não serão usadas

# %%
colunas_usadas = ['Booking Status','Reason for cancelling by Customer',               
                  'Driver Cancellation Reason','Pickup Location',
                  'Booking Value','Vehicle Type']

data = df[colunas_usadas]

data.info()

# %% [markdown]
# ## Análise Gráfica e Respondendo às perguntas
# 

# %% [markdown]
# ### Qual a porcentagem de corridas canceladas por motoristas, clientes, corridas completas, corridas incompletas e de motoristas não encontrados?

# %%
data["Booking Status"].unique()


# %%
contagem = data["Booking Status"].value_counts()
cores = ['#FF6188',  '#A9DC76',  '#FFD866',  '#78DCE8',  '#AB9DF2',  '#8c564b']
explode = [0.1,0,0,0,0]


# gera uma figura com dois gráficos(uma linha e duas colunas, cada coluna(axes) representa um gráfico)
#o figsize(altura,largura) em polegadas
fig, axes = plt.subplots(1, 2, figsize=(16, 6))


axes[0].pie(
    contagem,                     
    labels=contagem.index,        
    autopct='%1.1f%%',                 
    colors= cores,
    explode= explode,
    shadow= True


    
)

axes[0].set_title("Distribuição das Corridas(%)")

barras = axes[1].bar(
    contagem.index,
    contagem.values,
    color=cores
)

axes[1].set_title("Distribuição das Corridas (Contagem)")
axes[1].set_ylabel("Quantidade de Corridas")
axes[1].tick_params(axis='x', rotation=35)

#Percorre cada Barra e pega a altura e forma esse texto como título da barra(bar.get_height())
axes[1].bar_label(barras, fmt='%d', padding=4)
# ajusta automaticamente o layout da figura
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Quais os motivos para motoristas cancelarem as viagens?
# 
# 

# %%
data["Driver Cancellation Reason"].unique()

# %%
contagem = data["Driver Cancellation Reason"].value_counts()
cores = ['#FF6188',  '#A9DC76',  '#FFD866',  '#78DCE8']
print(contagem)

barras = plt.bar(
    contagem.index,
    contagem.values,
    color= cores
)

plt.title("Motivos para motoristas cancelarem as corridas")
plt.ylabel("Quantidade de Cancelamentos")
plt.xticks(rotation=35, ha='right')


plt.bar_label(barras, fmt='%d', padding=3)

plt.show()

# %% [markdown]
# ### Quais os  motivos para clientes cancelarem a corrida?

# %%
data["Reason for cancelling by Customer"].unique()

# %%
contagem = data["Reason for cancelling by Customer"].value_counts()
cores = ['#FF6188',  '#A9DC76',  '#FFD866',  '#78DCE8']
print(contagem)

barras = plt.bar(
    contagem.index,
    contagem.values,
    color= cores
)

plt.title("Motivos para Clientes cancelarem as corridas")
plt.ylabel("Quantidade de Cancelamentos")
plt.xticks(rotation=35, ha='right')

plt.bar_label(barras, fmt='%d', padding=3)

plt.show()

# %% [markdown]
# ### Quais são os top 3 locais que tem como o maior motivo de cancelamento terem passageiros de mais?
# 
# 

# %%
# O loc seleciona linhas com os valores específicos de uma linha e com o nome de uma coluna específica
#data.loc[linha,coluna]
#data["Driver Cancellation Reason"] == "x", me retorna as linhas do data set onde naquela coluna a linha seja igual a x
#A coluna no loc(segundo parametro) vai me retornar os locais onde a linha é igual a x.
contagem = data.loc[data["Driver Cancellation Reason"]== "More than permitted people in there","Pickup Location"].value_counts().head(5)
cores = ["#33006D",  "#51208AFF",  "#51208AFF",  "#B78EE6FF","#B78EE6FF"]

grafico = plt.barh(
    contagem.index,
    contagem.values,
    color = cores
)

plt.title("Tops locais cancelados por terrem passageiros de mais")
plt.xlabel("Quantidade de cancelamentos")
plt.ylabel("Locais")
#Pega o eixo atual do grafico(x e y) e inverto y(maior para o menor)
plt.gca().invert_yaxis()

plt.bar_label(grafico, fmt='%d', padding=3)

plt.show()

# %% [markdown]
# ### Qual o preço médio das tarifas das viagens completas por tipo de veículo?

# %%
data2 = data[data["Booking Status"] == "Completed"]

contagem = data2["Vehicle Type"].value_counts()

data2 = data2.groupby("Vehicle Type")

media = data2["Booking Value"].mean()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))


barras0 = axes[0].bar(
    media.index,                     
    media.values        
)

axes[0].set_title("Preço médio da tarifa por tipo de veículo")
axes[0].set_ylabel("Preço médio da tarifa")
axes[0].tick_params(axis='x', rotation=45)
axes[0].bar_label(barras0, fmt = "%d", padding = 3)

barras = axes[1].bar(
    contagem.index,
    contagem.values,
)

axes[1].set_title("Quantidade de corridas por tipo de veículo")
axes[1].set_ylabel("Quantidade de Corridas")
axes[1].tick_params(axis='x', rotation=45)

axes[1].bar_label(barras, fmt = "%d", padding = 3)

# ajusta automaticamente o layout da figura
plt.tight_layout()
plt.show()



# %% [markdown]
# # Checando por possíveis Outliers nas tarifas

# %% [markdown]
# #### Achei estranho o tipo de veículo não alterar tanto o preço da tarifa, decidi testar usando a distância da viagem e retirar os outliers das tarifas.

# %%
#desagrupo data2 e coloco só corridas completas
data2 = data[data["Booking Status"] == "Completed"]

sns.boxplot(
    x='Vehicle Type',
    y='Booking Value',
    data=data2,
)

# %%
data2 = df[df["Booking Status"] == "Completed"]

# Calcular os quartirs
Q1 = data2['Booking Value'].quantile(0.25)
Q3 = data2['Booking Value'].quantile(0.75)
IQR = Q3 - Q1


limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.1 * IQR

outliers = data2[
    (data2['Booking Value'] < limite_inferior) | 
    (data2['Booking Value'] > limite_superior)
]

plt.figure(figsize=(10, 6))

# Plotar todos os pontos
sns.scatterplot(
    x='Ride Distance', 
    y='Booking Value', 
    data=data2, 
    color='blue',  
    label='Todos os Dados'
)

# Plotar os outliers em uma cor diferente 
sns.scatterplot(
    x='Ride Distance', 
    y='Booking Value', 
    data=outliers, 
    color='red', 
    label='Outliers'
)

plt.title('Distribuição dos Outliers de Preço da tarifa em Relação à Distância')
plt.xlabel('Distância da Corrida')
plt.ylabel('Preço da tarifa da Viagem')
plt.legend()
plt.show()


# %% [markdown]
# # Tirando os outliers

# %%
data2.info()

# %%
#desagrupo data2 e coloco só corridas completas
data2 = df[df["Booking Status"] == "Completed"]
data2 = data2[(data2['Booking Value'] >= limite_inferior) & (data2['Booking Value']<= limite_superior)]
data2.info()

# %%
sns.boxplot(
    x='Vehicle Type',
    y='Booking Value',
    data=data2,
)

# %%


plt.figure(figsize=(10, 6))

# Plotar todos os pontos
sns.scatterplot(
    x='Ride Distance', 
    y='Booking Value', 
    data=data2, 
    color='blue', 
    alpha=0.1, 
    label='Todos os Dados'
)

plt.title('Distribuição de Preço da tarifa em Relação à Distância')
plt.xlabel('Distância da Corrida')
plt.ylabel('Preço da Viagem')
plt.legend()
plt.show()

# %% [markdown]
# #### Agora sem outliers nas tarifas, decidi testar se houve diferença da tarifa por tipo de veículo

# %%
contagem = data2["Vehicle Type"].value_counts()

data2 = data2.groupby("Vehicle Type")

media = data2["Booking Value"].mean()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))


barras0 = axes[0].bar(
    media.index,                     
    media.values        
)

axes[0].set_title("Preço médio da tarifa por tipo de veículo")
axes[0].set_ylabel("Preço médio")
axes[0].tick_params(axis='x', rotation=35)
axes[0].bar_label(barras0, fmt = "%d", padding = 4)

barras = axes[1].bar(
    contagem.index,
    contagem.values,
)

axes[1].set_title("Quantidade de corridas por tipo de veículo")
axes[1].set_ylabel("Quantidade de Corridas")
axes[1].tick_params(axis='x', rotation=35)

axes[1].bar_label(barras, fmt = "%d", padding = 4)

# ajusta automaticamente o layout da figura
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Interpretações Obtida
# 
# 1. Qual a porcentagem de corridas canceladas por motoristas, clientes, corridas completas, corridas incompletas e de motoristas não encontrados?
# 
#     **62% da corridas foram bem sucedidas** e **38% das corridas falharam**.  
#     Desses 38%, ** os motoristas foram responsáveis pelo cancelamento em 47% dos casos**.  
# 
# 2. Quais os  motivos para motoristas cancelarem a corrida?
# 
#     O principal motivo está relacionado aos clientes: problemas com o cliente (~25%), cliente doente (~25%) ou transporte que não comportava a quantidade de pessoas (~25%).   
#     Os outros 25% se devem a mau funcionamento do carro ou motivos pessoais do motorista.  
# 
# 3. Quais os  motivos para clientes cancelarem a corrida?  
# 
#     Responsáveis por **18% dos cancelamentos**, geralmente devido a problemas com o motorista, local incorreto ou problemas com o carro.  
# 
# 4. Top 3 locais com cancelamento por excesso de passageiros:    
#  
#         1. Nehru Place  
#         2. Saket  
#         3. Tilak Nagar  
# 
#     Talvez implantar mais veículos **Uber XL** nesses locais seja interessante para reduzir esse problema.  
# 
# 5. Qual o preço médio das tarifas das viagens completas por veículo?
#     
#     O preço da tarifa não varia só pelo tipo de veículo, mas, também, como especificado pela própria UBER, eles aplicam uma "taxa dinâmica" que varia de acordo com a demanda. 
# 
#     Quando plotei os gráficos, achei muito estranho as tarifas terem preços médios tão parecidos, então resolvi ver se a tarifa tinha relação com a distância, mas não tinha tanta relação, então decidi procurar e retirar outliers, mas o preço médio continuou parecido. Isso aconteceu porque as taxas são calculadas levando também a demanda por veículos.
#       
# 

# %% [markdown]
# 
# ### Guia
# 
# MUKHIYA, Suresh Kumar; AHMED, Usman. Hands-On Exploratory Data Analysis with Python. [S.l.]: Packt, 2020.
# Suresh Kumar Mukhiya,Usman Ahmed - 2020 - Hands-On Exploratory Data Analysis with Python  
# 
# FACCIANI, Juliano. Entendendo e Interpretando Boxplots com Python. Asimov Academy. [S. l.], [2024]. Disponível em: https://hub.asimov.academy/tutorial/entendendo-e-interpretando-boxplots-com-python/. Acesso em: 15 set. 2025.

# %% [markdown]
# ### DATASET
# 
# https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard


