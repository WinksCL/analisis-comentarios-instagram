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
