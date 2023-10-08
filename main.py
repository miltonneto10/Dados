import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine

#Configurando a conexão com o banco de dados MySQL
mysql_password = os.environ.get("MYSQL_PASSWORD")
engine = create_engine(f"mysql://milton:{mysql_password}@localhost:3306/desafio_dados")

#Lendo o arquivo Excel
colunas = ['Funcionário', 'Especialidade', 'Custo do afastamento', 'Departamento', 'Motivo', 'Líder', 'Data do Atestado', 'Código']

df = pd.read_excel("dados.xlsx", usecols=colunas)

#Removendo todas as linhas com valores nulos
df = df.dropna()

#Limpeza e transformação dos dados
df["Custo do afastamento"] = df["Custo do afastamento"].str.replace(',', '.').astype(float)

#Carregando dados para o banco de dados MySQL
df.to_sql(name="dados_desafio", con=engine, if_exists="replace", index=False)

#Consulta SQL 1: Qual departamento gastou mais em afastamentos?
query1 = """
SELECT Departamento, SUM(`Custo do afastamento`) AS `Custo total`
FROM dados_desafio
GROUP BY Departamento
ORDER BY `Custo total` DESC
LIMIT 1;
"""

result1 = pd.read_sql(query1, engine)
print("Qual departamento gastou mais em afastamentos?")
print(result1)


#Consulta SQL 2: Quem é o líder do departamento que mais gastou?
query2="""
SELECT Lider
FROM dados_desafio
WHERE Departamento = (SELECT Departamento FROM (SELECT Departamento, SUM(`Custo do afastamento`) AS `Custo total`
                    FROM dados_desafio
                    GROUP BY Departamento
                    ORDER BY `Custo total` DESC
                    LIMIT 1) AS dept_gastou_mais);
"""

result2 = pd.read_sql(query2, engine)
print("\nQuem é o líder do departamento que mais gastou?")
print(result2)

#Consulta SQL 3: Tabela de ocorrências por dia da semana
query3 = """
SELECT DAYNAME(`Data de início do afastamento`) AS `Dia da semana`, COUNT(*) AS `Número de ocorrências`
FROM dados_desafio
GROUP BY `Dia da semana`
ORDER BY FIELD(`Dia da semana`, 'Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado');
"""

result3 = pd.read_sql(query3, engine)
print("\nTabela de ocorrências por dia da semana")
print(result3)

#Consulta SQL 4: Número de atestados acumulados ao longo do tempo(mês)
query4= """
SELECT DATE_FORMAT(`Data de início do atestado`, '%m/%y) AS `Mês`
COUNT(*) AS `Número de atestados`,
SUM(COUNT(*)) OVER (ORDER BY `Mês`) AS `Acumulado`
FROM dados_desafio
GROUP BY `Mês`
ORDER BY `Mês`;
"""

result4 = pd.read_sql(query4, engine)
print("\nNúmero de atestados acumulados ao longo do tempo (mês)")
print(result4)