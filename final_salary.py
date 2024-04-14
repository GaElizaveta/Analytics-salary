import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go


st.title('Анализ зарплат в России')
sidebar = st.sidebar

inflation_choice = sidebar.radio("Данные о каких зарплатах Вы хотите посмотреть?", ('Без учета уровня инфляции (номинальная зарплата)', 'С учетом уровня инфляции (реальная зарплата)'))
st.text(' ')
show_inflation = sidebar.checkbox("Показать влияние инфляции на изменение зарплаты по сравнению с предыдущем годом", value=False)
show_inflation_salary = sidebar.checkbox("Показать динамику изменения номинальных зарплат и уровня инфляции", value=False)
show_unemployment = sidebar.checkbox("Показать динамику изменения реальных зарплат и уровня безработицы", value=False)


salary_inflation = st.cache_data(pd.read_excel)('salary_inflation.xlsx')
salary_inflation.set_index('Год',inplace = True)
salary_inflation.index = salary_inflation.index.astype(str)

salary = st.cache_data(pd.read_excel)('salary.xlsx')
salary.set_index('Год', inplace = True)
salary.index = salary.index.astype(str)

inflation = st.cache_data(pd.read_excel)('Инфляция.xlsx')
inflation.index = inflation.index.astype(str)

unemployment = st.cache_data(pd.read_excel)('Безработица.xlsx')
unemployment.index = unemployment.index.astype(str)

if inflation_choice == 'Без учета уровня инфляции (номинальная зарплата)':
    st.subheader("Зарплата без учета уровня инфляции (номинальная)", anchor=None)
    if st.checkbox('Показать таблицу номинальных зарплат'):
        st.dataframe(salary)
    salary = st.cache_data(pd.read_excel)('salary.xlsx')
    salary.set_index('Год',inplace = True)
    salary.index = salary.index.astype(str)

    selected_years = st.slider('Выберите года за которые Вы хотите посмотреть динамику изменения номинальных зарплат', min_value=2000, max_value=2023, value = (2000,2023), key = "slider")
    selected_activities = st.multiselect('Выберите вид(ы) экономической деятельности', salary.columns[0:].to_list(), key ='multiset')

    filtered_data = salary.loc[(salary.index.astype(int) >= selected_years[0]) & (salary.index.astype(int) <= selected_years[1]), selected_activities]
    fig_line1 = px.line(filtered_data, labels={"variable": "Вид(ы) экономической деятельности"})
    fig_line1.update_yaxes(title_text="Зарплата")
    fig_line1.update_layout(title_text="Динамика номинальных зарплат по видам экономической деятельности", title_x=0.15, title_y=1)

    fig_bar1 = px.bar(filtered_data, barmode='group', labels={"variable": "Вид(ы) экономической деятельности"})
    fig_bar1.update_yaxes(title_text="Зарплата")

    fig_box1 = px.box(filtered_data, labels={"variable": "Вид(ы) экономической деятельности"})
    fig_box1.update_yaxes(title_text="Зарплата")

    st.plotly_chart(fig_line1)
    st.plotly_chart(fig_bar1)
    st.plotly_chart(fig_box1)

if inflation_choice == 'С учетом уровня инфляции (реальная зарплата)':

    st.subheader("Зарплата с учетом уровня инфляции (реальная)")
    if st.checkbox('Показать таблицу реальных зарплат'):
        st.dataframe(salary_inflation)

    selected_years1 = st.slider('Выберите года, за которые Вы хотите посмотреть динамику изменения реальных зарплат', min_value=2000, max_value=2023, value = (2000,2023), key = "slider1")
    selected_activities1 = st.multiselect('Выберите вид(ы) экономической деятельности', salary_inflation.columns[0:].to_list(), key ='multiset1')
    filtered_data1 = salary_inflation.loc[(salary_inflation.index.astype(int) >= selected_years1[0]) & (salary_inflation.index.astype(int) <= selected_years1[1]), selected_activities1]

    fig_line2 = px.line(filtered_data1, labels={"variable": "Вид(ы) экономической деятельности"})
    fig_line2.update_yaxes(title_text="Зарплата")
    fig_line2.update_layout(title_text="Динамика реальных зарплат по видам экономической деятельности", title_x=0.15, title_y=1)
    st.plotly_chart(fig_line2, use_container_width=True, width=1000, height=400)

if show_inflation:
    infl_effect = pd.DataFrame()

    for col in salary_inflation.columns[0:]:
        diff_col = col
        infl_effect[diff_col] = salary_inflation[col].diff()

    infl_effect = infl_effect.dropna()
    st.subheader("Влияние инфляции на изменение зарплаты по сравнению с предыдущем годом")
    if st.checkbox('Показать таблицу изменения реальных зарплат по сравнению с предыдущим годом'):
        st.dataframe(infl_effect)

    selected_years2 = st.slider('Выберите года, за которые Вы хотите посмотреть изменение зарплат по сравнению с предыдущим годом', min_value=2001, max_value=2023, value=(2000, 2023), key="slider2")

    filtered_data2 = infl_effect.loc[(infl_effect.index.astype(int) >= selected_years2[0]) & (
                infl_effect.index.astype(int) <= selected_years2[1])]

    fig_eff = px.bar(filtered_data2, barmode='group', labels={"variable": "Вид(ы) экономической деятельности"})
    fig_eff.update_yaxes(title_text="Изменение реальной зарплаты по сравнению с предыдущим годом")
    st.plotly_chart(fig_eff)

if show_inflation_salary:

    fig = go.Figure()
    st.subheader("Динамика изменения номинальных зарплат и уровня инфляции")
    show_matrix = st.checkbox('Показать матрицу корреляции между уровнем инфляцией и номинальными зарплатами')

    for column in salary.columns[0:]:
        fig.add_trace(go.Scatter(x = salary.index, y=salary[column], mode='lines', name=column))

    fig.add_trace(go.Scatter(x=inflation['Год'], y=inflation['Инфляция'], name='Инфляция', yaxis='y2'))

    fig.update_layout(yaxis=dict(title='Зарплата', range=[0, 70000], showgrid=False),
                      yaxis2=dict(title='Инфляция (%)', overlaying='y', side='right', range=[0, 25], showgrid=False), legend=dict(x=0.58, y=1, traceorder='normal', orientation='v'))
    st.plotly_chart(fig)

    if show_matrix:
        inflation.index = inflation.index.astype(int)
        salary.index = salary.index.astype(int)
        merged_infl_sal = pd.merge(inflation, salary, on='Год', how='inner')
        merged_infl_sal = merged_infl_sal.drop(columns='Год')
        corr_matrix = merged_infl_sal.corr()

        fig = px.imshow(corr_matrix, labels=dict(color="Корреляция"), x=corr_matrix.columns, y=corr_matrix.columns,
                    width=800, height=600, zmin=-1, zmax=1)

        fig.update_layout(title='Матрица корреляции между уровнем инфляции и номинальными зарплатами', title_x=0.1, title_y=1)

        st.plotly_chart(fig)

if show_unemployment:
    st.subheader("Динамика изменения реальных зарплат и уровня безработицы")
    show_matrix2 = st.checkbox('Показать матрицу корреляции между уровнем безработицы и реальными зарплатами')
    fig = go.Figure()

    for column in salary_inflation.columns[0:]:
        fig.add_trace(go.Scatter(x = salary_inflation.index, y=salary_inflation[column], mode='lines', name=column))

    fig.add_trace(go.Scatter(x=unemployment['Год'], y=unemployment['Уровень безработицы по РФ, %'], name='Уровень безработицы по РФ, %', yaxis='y2'))

    fig.update_layout(yaxis=dict(title='Зарплата', range=[0, 70000], showgrid=False),
                      yaxis2=dict(title='Безработица (%)', overlaying='y', side='right', range=[0, 12], showgrid=False), legend=dict(x=0.5, y=1, traceorder='normal', orientation='v'))

    st.plotly_chart(fig)

    if show_matrix2:
        unemployment.index = inflation.index.astype(int)
        salary_inflation.index = salary.index.astype(int)
        merged_unemp_sal = pd.merge(unemployment, salary_inflation, on='Год', how='inner')
        merged_unemp_sal = merged_unemp_sal.drop(columns='Год')
        corr_matrix = merged_unemp_sal.corr()

        fig = px.imshow(corr_matrix, labels=dict(color="Корреляция"), x=corr_matrix.columns, y=corr_matrix.columns,
                    width=800, height=600, zmin=-1, zmax=1)

        fig.update_layout(title='Матрица корреляции между уровнем безработицы и реальными зарплатами', title_x=0.15, title_y=1)

        st.plotly_chart(fig)
