import streamlit as st
import pandas as pd
import os
from data_scraping import get_instagram_comments_from_profile, save_comments_to_csv
from sentiment_analysis import analyze_sentiments, categorize_sentiments
from visualization import plot_sentiment_distribution, plot_sentiment_over_time

st.title('Análisis de Sentimientos en Instagram')

# Campo de texto para el nombre de usuario del perfil de Instagram
profile_username = st.text_input('Ingrese el nombre de usuario del perfil de Instagram')
username = st.text_input('Ingrese su nombre de usuario de Instagram')
password = st.text_input('Ingrese su contraseña de Instagram', type='password')
num_posts = st.number_input('Número de publicaciones a analizar', min_value=1, max_value=10, value=5)

if st.button('Obtener Comentarios'):
    if profile_username and username and password:
        print(f"Obteniendo comentarios del perfil: {profile_username}")
        comments, dates = get_instagram_comments_from_profile(profile_username, username, password, num_posts)
        if comments:
            # Crear la carpeta 'data' si no existe
            if not os.path.exists('data'):
                os.makedirs('data')
                print("Carpeta 'data' creada.")

            save_comments_to_csv(comments, dates, 'data/comments.csv')
            st.success('Comentarios obtenidos y guardados exitosamente')
            
            # Mostrar los comentarios en la interfaz
            comments_df = pd.DataFrame({'comment': comments, 'date': dates})
            st.write(comments_df)
        else:
            st.error('No se pudieron obtener los comentarios')
            print("No se obtuvieron comentarios.")
    else:
        st.error('Por favor, ingrese un nombre de usuario de perfil, nombre de usuario y contraseña válidos')
        print("Datos inválidos.")

if st.button('Analizar Sentimientos'):
    # Verificar si el archivo 'comments.csv' existe
    if os.path.exists('data/comments.csv'):
        comments_df = pd.read_csv('data/comments.csv', parse_dates=['date'])
        sentiment_df = analyze_sentiments(comments_df['comment'])
        sentiment_df['date'] = comments_df['date']
        sentiment_df = categorize_sentiments(sentiment_df)
        sentiment_df.to_csv('data/sentiments.csv', index=False)
        st.success('Sentimientos analizados y guardados exitosamente')

        plot_sentiment_distribution(sentiment_df)
        plot_sentiment_over_time(sentiment_df)
    else:
        st.error('El archivo comments.csv no existe. Primero obtén los comentarios.')
        print("El archivo comments.csv no existe.")
