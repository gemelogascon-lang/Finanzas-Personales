from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Mi Página de Finanzas Personales</h1>
    <p>¡Bienvenido a mi app!</p>
    """
