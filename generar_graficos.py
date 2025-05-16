# generar_graficos.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def generar_todos_los_graficos(output_path):
    
    df_total = pd.read_csv('csv\\04 share-electricity-renewables.csv')
    df_wind = pd.read_csv('csv\\11 share-electricity-wind.csv')
    df_solar = pd.read_csv('csv\\15 share-electricity-solar.csv')
    df_hydro = pd.read_csv('csv\\07 share-electricity-hydro.csv')

    # Asegurar consistencia de columnas
    df_total = df_total.rename(columns={df_total.columns[-1]: 'Renewables'})
    df_wind = df_wind.rename(columns={df_wind.columns[-1]: 'Wind'})
    df_solar = df_solar.rename(columns={df_solar.columns[-1]: 'Solar'})
    df_hydro = df_hydro.rename(columns={df_hydro.columns[-1]: 'Hydro'})

    # Años comunes
    years = sorted(set(df_total['Year']) & set(df_wind['Year']) & set(df_solar['Year']) & set(df_hydro['Year']))
    years = [y for y in years if 1990 <= y <= 2022]  # rango de años animado

    # Inicializar gráfico
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis('equal')
    title = ax.text(0, 1.1, '', ha='center', va='center', fontsize=14)

    def get_avg(df, year, col):
        return df[df['Year'] == year][col].mean()

    def update(year):
        ax.clear()
        ax.axis('equal')
        wind = get_avg(df_wind, year, 'Wind')
        solar = get_avg(df_solar, year, 'Solar')
        hydro = get_avg(df_hydro, year, 'Hydro')
        total = get_avg(df_total, year, 'Renewables')
        others = max(0, total - (wind + solar + hydro))

        values = [wind, solar, hydro, others]
        labels = ['Eólica', 'Solar', 'Hidro', 'Otras']
        colors = ['#4f99ff', '#ffc107', '#00c49a', '#8884d8']
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
        title.set_text(f'Participación de Energías Renovables ({year})')
        fig.suptitle(f"Año: {year}", fontsize=12)

    ani = FuncAnimation(fig, update, frames=years, repeat=False, interval=700)
    ani.save( output_path + 'grafico_torta_renovables.gif', writer='pillow')
