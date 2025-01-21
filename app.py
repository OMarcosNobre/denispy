from flask import Flask, render_template, request
import plotly.graph_objects as go
import json
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    value = 270  # Valor inicial
    gauge_max = 500  # Range inicial
    delta = 260  # Delta inicial

    if request.method == "POST":
        try:
            value = int(request.form.get("value", 270))
            gauge_max = int(request.form.get("gauge_max", 500))
            delta = int(request.form.get("delta", 260))
        except ValueError:
            pass  # Valores inválidos ficam no padrão

    # Criar um range de 50 em 50 até o valor máximo
    #tick_vals = list(range(0, int(gauge_max) + 50, 50))
    tick_increment = int(gauge_max / 10)  # Divide o máximo por 10
    tick_vals = list(range(0, int(gauge_max) + tick_increment, tick_increment))  # Gera os ticks


    # Criar o gráfico
    fig = go.Figure(go.Indicator(
        mode="gauge+delta", # Caso queira mostrar o número de municipios com casos no gráfico basta adicionar o number ex.: mode="gauge+number+delta"
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta = {'reference': delta, 'increasing': {'color': 'red'}, 'decreasing': {'color': 'green'}},
        gauge={
            'axis': {
                'range': [None, gauge_max], 
                'tickvals': tick_vals, 
                'tickfont': {'size': 20, 'color': 'black'},
                },
            'bar': {'color': "orange"}  # Exemplo de customização
        }
    ))
    
    fig.update_layout(
        width=600,  # Define a largura máxima da imagem
        margin=dict(t=50, b=0),  # Aumenta a margem superior para criar espaço
        title={
            'y': 0.9,  # Define a posição vertical do título (1 é no topo do gráfico)
            'x': 0.5,  # Centraliza o título horizontalmente
            'xanchor': 'center',
            'yanchor': 'top',
            'text': f"<b>{value}</b> cidades com clima favorável para transmissão",  # Título
            'font': {'size': 24}  # Tamanho da fonte do título
        }
    )

    # Converter o gráfico em JSON
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)

    return render_template("index.html", graph_json=graph_json, value=value, gauge_max=gauge_max, delta=delta)

if __name__ == "__main__":
    app.run(debug=True)
