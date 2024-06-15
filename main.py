def main():
    print("Para ejecutar la aplicación, use los siguientes comandos:")
    print("python -m venv venv")
    print("Set-ExecutionPolicy RemoteSigned -Scope CurrentUser")
    print("venv\Scripts\Activate.ps1")
    print("pip install -r requirements.txt")
    print("streamlit run scripts/app.py")

if __name__ == "__main__":
    main()
