import os

import pandas as pd
import plotly.express as px
import streamlit as st

# Page config
st.set_page_config(
    page_title='Dashboard RH',
    #    page_icon='',
    layout='wide',
)

st.title('Dashboard RH')
df = pd.read_csv('../data/DatasetRHTratado.csv')

df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce')

# sidebar
st.sidebar.header('Filtre por idade')

idade_min, idade_max = st.sidebar.slider(
    label='Filtre por idade',
    min_value=df['Idade'].min(),
    max_value=df['Idade'].max(),
    value=(df['Idade'].min(), df['Idade'].max()),
)

df_selecionado = df.query('Idade >= @idade_min & Idade <= @idade_max')

# Total de funcionarios
total_funcionario = df_selecionado.shape[0]

# Tempo medio de experiencia
media_exp = int(round(df_selecionado['Anos_Experiencia'].mean(), 0))

# Total e percentual de Funcionarios Feminino
df_feminino = df_selecionado[df_selecionado['Genero'] == 'Feminino']
total_feminino = df_feminino.shape[0]
percentual_feminino = total_feminino / total_funcionario * 100
percentual_feminino = round(percentual_feminino, 2)

# Total e percentual de funcionario Masculino
df_masculino = df_selecionado[df_selecionado['Genero'] == 'Masculino']
total_masculino = df_masculino.shape[0]
percentual_masculino = total_masculino / total_funcionario * 100
percentual_masculino = round(percentual_masculino, 2)

# Media Salarial
media_sal_mensal = df_selecionado['Salario_Mensal'].mean()
media_sal_mensal = round(media_sal_mensal, 2)

col1, col2, col3 = st.columns(3, gap='medium')


with col1:
    st.metric('Total de Funcionarios', total_funcionario)
    st.divider()
    st.metric('Tempo Medio Experiencia', media_exp)
with col2:
    st.metric('Total Feminino', total_feminino)
    st.divider()
    st.metric('Percentual Feminino', f'{percentual_feminino}%')

with col3:
    st.metric('Total Masculino', total_masculino)
    st.divider()
    st.metric('Percentual Masculino', percentual_masculino)

# Funcionarios por funcao
func_por_funcao = df_selecionado.groupby('Funcao').size().reset_index()

func_por_funcao.columns = ['Funcao', 'Total_Funcionarios']

func_por_funcao_sorted = func_por_funcao.sort_values(
    by='Total_Funcionarios', ascending=True
)

grafico5 = px.bar(
    func_por_funcao_sorted,
    y='Funcao',
    x='Total_Funcionarios',
    title='Total Funcionário Por Função',
    orientation='h',
    text='Total_Funcionarios',
    template='plotly_white',
)

# Disponibilidade para hora extras
df_horas_extra = (
    df_selecionado.groupby('Disponivel_Hora_Extra').size().reset_index()
)
df_horas_extra.columns = ['Disponibilidade', 'Total Funcionarios']

df_horas_extra.loc[
    df_horas_extra['Disponibilidade'] == 'S', 'Disponibilidade'
] = 'Disponivel'
df_horas_extra.loc[
    df_horas_extra['Disponibilidade'] == 'N', 'Disponibilidade'
] = 'Nao Disponivel'

gf_pizza_disponilidade = px.pie(
    df_horas_extra,
    values='Total Funcionarios',
    names='Disponibilidade',
    title='Disponibilidade Horas Extra',
)

# Envolvimento do Funcionario na empresa
df_envolvimento = df_selecionado.groupby('envolvimento').size().reset_index()

df_envolvimento.columns = ['envolvimento', 'total_funcionarios']

df_envolvimento = df_envolvimento.sort_values(
    by='total_funcionarios', ascending=False
)

graf_envolvimento = px.pie(
    df_envolvimento,
    values='total_funcionarios',
    names='envolvimento',
    title='Envolvimento Dos Funcionarios',
)

# Configurando os graficos
grafico5.update_layout(width=400, height=400)

gf_pizza_disponilidade.update_layout(width=400, height=400)

graf_envolvimento.update_layout(width=400, height=400)


st.divider()
col1, col2, col3 = st.columns(3, gap='large')

with col1:
    st.plotly_chart(grafico5)

with col2:
    st.plotly_chart(gf_pizza_disponilidade)

with col3:
    st.plotly_chart(graf_envolvimento)
  