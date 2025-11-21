from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Configuración Supabase desde variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Crear app FastAPI
app = FastAPI()

# Página de inicio
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Mi Página de Finanzas Personales</h1>
    <p>Bienvenido a tu app de finanzas</p>
    <p>Visita <a href="/gastos">/gastos</a> para ver tus gastos</p>
    """

# Ruta para mostrar gastos
@app.get("/gastos", response_class=HTMLResponse)
def mostrar_gastos():
    # Traer datos de Supabase
    response = supabase.table("gastos").select("*").execute()
    data = response.data

    if not data:
        return "<h2>No hay gastos registrados</h2>"

    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # -------------------------------
    # TABLA HTML
    # -------------------------------
    tabla_html = df.to_html(index=False)

    # -------------------------------
    # GRÁFICO 1: Plotly - Gastos por categoría
    # -------------------------------
    resumen = df.groupby("categoria")["monto"].sum().reset_index()
    fig_plotly = px.bar(resumen, x="categoria", y="monto", title="Gastos por Categoría")
    grafico_plotly_html = pio.to_html(fig_plotly, full_html=False)

    # -------------------------------
    # GRÁFICO 2: Matplotlib - Distribución de gastos
    # -------------------------------
    plt.figure(figsize=(6,4))
    plt.pie(resumen['monto'], labels=resumen['categoria'], autopct='%1.1f%%', startangle=90)
    plt.title("Distribución de Gastos por Categoría")
    
    # Guardar figura en memoria y codificar en base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    grafico_matplotlib = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    # HTML para Matplotlib
    grafico_matplotlib_html = f'<img src="data:image/png;base64,{grafico_matplotlib}" alt="Gráfico Matplotlib">'

    # -------------------------------
    # Retornar página completa
    # -------------------------------
    return f"""
    <h1>Gastos</h1>
    <h2>Tabla de Gastos</h2>
    {tabla_html}
    <h2>Gráfico Interactivo (Plotly)</h2>
    {grafico_plotly_html}
    <h2>Gráfico Circular (Matplotlib)</h2>
    {grafico_matplotlib_html}
    """
