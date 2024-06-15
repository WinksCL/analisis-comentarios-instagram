import pandas as pd
import plotly.express as px
import streamlit as st

def plot_sentiment_distribution(df):
    """Genera un gráfico de distribución de sentimientos."""
    fig = px.histogram(df, x='sentiment', title='Distribución de Sentimientos')
    st.plotly_chart(fig)

def plot_sentiment_over_time(df):
    """Genera un gráfico de sentimientos a lo largo del tiempo."""
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        fig = px.line(df, x='date', y='compound', title='Sentimientos a lo Largo del Tiempo')
        st.plotly_chart(fig)
    else:
        st.warning('No hay datos de fecha disponibles para mostrar sentimientos a lo largo del tiempo.')
