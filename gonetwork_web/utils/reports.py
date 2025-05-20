import base64
import io
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def generate_csv_download_link(df, filename="dados_gonetwork.csv"):
    """
    Gera um link para download de um DataFrame como arquivo CSV

    Args:
        df: DataFrame pandas
        filename: Nome do arquivo

    Returns:
        str: HTML para o link de download
    """
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    b64 = base64.b64encode(csv.encode()).decode()
    href = (
        f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    )
    return href


def generate_excel_download_link(df, filename="dados_gonetwork.xlsx"):
    """
    Gera um link para download de um DataFrame como arquivo Excel

    Args:
        df: DataFrame pandas
        filename: Nome do arquivo

    Returns:
        str: HTML para o link de download
    """
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")
        writer.save()

    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel</a>'
    return href


def generate_status_chart(data, title="Status dos Projetos"):
    """
    Gera um gráfico de barras ou pizza para dados de status

    Args:
        data: Dicionário com contagens {status: quantidade}
        title: Título do gráfico

    Returns:
        fig: Figura do Plotly
    """
    # Converter para DataFrame
    df = pd.DataFrame(list(data.items()), columns=["Status", "Quantidade"])

    # Gerar gráfico de barras
    fig = px.bar(
        df, x="Status", y="Quantidade", title=title, color="Status", text="Quantidade"
    )

    # Adicionar layout personalizado
    fig.update_layout(
        xaxis_title="Status",
        yaxis_title="Quantidade",
        legend_title="Status",
        plot_bgcolor="rgba(0,0,0,0.05)",
        title_font_size=20,
        font=dict(size=14),
    )

    return fig


def generate_timeline_graph(
    df, start_col="start", end_col="end", task_col="task", person_col=None
):
    """
    Gera um gráfico de timeline para tarefas

    Args:
        df: DataFrame com dados de timeline
        start_col: Nome da coluna com data/hora de início
        end_col: Nome da coluna com data/hora de término
        task_col: Nome da coluna com descrição da tarefa
        person_col: Nome da coluna com responsável (opcional)

    Returns:
        fig: Figura do Plotly
    """
    if df.empty:
        # Se não houver dados, retorna um gráfico vazio
        fig = go.Figure()
        fig.add_annotation(
            text="Nenhum dado disponível para gerar timeline",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16),
        )
        return fig

    # Converter para datetime se necessário
    for col in [start_col, end_col]:
        if df[col].dtype != "datetime64[ns]":
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                st.warning(
                    f"Não foi possível converter a coluna {col} para formato de data/hora"
                )
                return None

    # Criar cores por pessoa se a coluna de pessoa existir
    if person_col and person_col in df.columns:
        colors = px.colors.qualitative.Plotly
        persons = df[person_col].unique()
        color_map = {p: colors[i % len(colors)] for i, p in enumerate(persons)}
    else:
        color_map = None

    fig = go.Figure()

    for i, row in df.iterrows():
        if person_col and color_map:
            color = color_map.get(row[person_col], "gray")
            hover_text = f"{row[task_col]}<br>Responsável: {row[person_col]}"
        else:
            color = "blue"
            hover_text = row[task_col]

        fig.add_trace(
            go.Bar(
                x=[row[end_col] - row[start_col]],
                y=[i],
                orientation="h",
                marker_color=color,
                base=row[start_col],
                hovertext=hover_text,
                hoverinfo="text",
                name=row[task_col],
            )
        )

    fig.update_layout(
        title="Cronograma de Atividades",
        xaxis=dict(title="Data/Hora", tickformat="%d/%m/%Y %H:%M"),
        yaxis=dict(
            title="Atividade",
            ticktext=df[task_col],
            tickvals=list(range(len(df))),
            autorange="reversed",
        ),
        height=400 + (20 * len(df)),
        plot_bgcolor="rgba(0,0,0,0.05)",
        barmode="overlay",
    )

    return fig
