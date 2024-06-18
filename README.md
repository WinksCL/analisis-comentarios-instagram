# Análisis de sentimientos en Instagram

## Descripción del Proyecto

El "Análisis de sentimientos en Instagram" es una aplicación diseñada para obtener y analizar los comentarios de las publicaciones más recientes de un perfil de Instagram. Proporciona un análisis de sentimientos para determinar la percepción de la marca y muestra gráficos interactivos para visualizar los resultados.

## Integrantes del Equipo

- **Benjamin Valdivia**
- **Stefania Gonzalez**
- **Belen Zapata**

## Funcionalidades

- Obtener comentarios de las publicaciones más recientes de un perfil de Instagram.
- Analizar los sentimientos de los comentarios (positivos, negativos, neutros).
- Generar gráficos interactivos para visualizar la distribución de sentimientos y su evolución a lo largo del tiempo.

## Requisitos

- Python 3.x
- Biblioteca `pandas`
- Biblioteca `plotly`
- Biblioteca `nltk`
- Biblioteca `instaloader`
- Biblioteca `streamlit`

## Instalación

1. Clona este repositorio en tu máquina local.

    ```sh
    git clone https://github.com/WinksCL/analisis-comentarios-instagram.git
    ```

2. Navega al directorio del proyecto.
3. Crea y activa un entorno virtual.

    ```sh
    python -m venv venv
    source venv/bin/activate # Para Linux/Mac
    venv\Scripts\activate # Para Windows
    ```

4. Instala las dependencias del proyecto.

    ```sh
    pip install -r requirements.txt
    ```

## Estructura del Proyecto

```css
analisis_comentarios_instagram/
│
├── data/
│
├── scripts/
│ ├── __init__.py
│ ├── app.py
│ ├── data_scraping.py
│ ├── sentiment_analysis.py
│ ├── visualization.py
│
├── venv/
│
├── .gitignore
├── README.md
├── requirements.txt
└── main.py
```

- **`scripts/__init__.py`**: Archivo de inicialización del paquete.
- **`scripts/app.py`**: Archivo principal de la aplicación Streamlit que gestiona la interfaz de usuario.

```python
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
```

- **`scripts/data_scraping.py`**: Contiene las funciones para obtener comentarios de un perfil de Instagram y guardarlos en un archivo CSV.

```python
import instaloader
import pandas as pd

def get_instagram_comments_from_profile(profile_username, username, password, num_posts=5):
    """Obtiene comentarios de las publicaciones más recientes de un perfil de Instagram."""
    L = instaloader.Instaloader()
    
    # Iniciar sesión
    try:
        L.login(username, password)
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return []

    # Cargar el perfil de Instagram
    try:
        profile = instaloader.Profile.from_username(L.context, profile_username)
    except Exception as e:
        print(f"Error al cargar el perfil: {e}")
        return []

    comments = []
    dates = []
    post_count = 0
    for post in profile.get_posts():
        if post_count >= num_posts:
            break
        post_count += 1
        for comment in post.get_comments():
            comments.append(comment.text)
            dates.append(comment.created_at_utc)
    
    return comments, dates

def save_comments_to_csv(comments, dates, filepath):
    """Guarda los comentarios y las fechas en un archivo CSV."""
    if not comments:
        print("No hay comentarios para guardar.")
        return
    df = pd.DataFrame({'comment': comments, 'date': dates})
    df.to_csv(filepath, index=False)
    print(f"Comentarios guardados en {filepath}")
```

`scripts/sentiment_analysis.py` Contiene las funciones para analizar los sentimientos de los comentarios.

```python
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

# Descargar el lexicón de VADER si aún no está descargado
nltk.download('vader_lexicon')

def analyze_sentiments(comments):
    """Analiza los sentimientos de una lista de comentarios."""
    sia = SentimentIntensityAnalyzer()
    results = []
    for comment in comments:
        # Asegurarse de que cada comentario sea una cadena de texto
        if not isinstance(comment, str):
            comment = str(comment)
        sentiment = sia.polarity_scores(comment)
        results.append({
            'comment': comment,
            'positive': sentiment['pos'],
            'neutral': sentiment['neu'],
            'negative': sentiment['neg'],
            'compound': sentiment['compound']
        })
    return pd.DataFrame(results)

def categorize_sentiments(df):
    """Categoriza los comentarios en positivos, neutros y negativos."""
    df['sentiment'] = df['compound'].apply(lambda c: 'positive' if c > 0.05 else ('negative' if c < -0.05 else 'neutral'))
    return df
```

- **`scripts/visualization.py`**: Contiene las funciones para generar gráficos de visualización de datos.

```python
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
```

## Uso

1. Ejecuta el script principal `main.py`.

    ```sh
    python main.py
    ```

2. Ingresa el nombre de usuario del perfil de Instagram y tus credenciales de Instagram.
3. Selecciona el número de publicaciones a analizar.
4. Haz clic en "Obtener Comentarios" para recopilar los comentarios.
5. Haz clic en "Analizar Sentimientos" para realizar el análisis de sentimientos y visualizar los resultados.
