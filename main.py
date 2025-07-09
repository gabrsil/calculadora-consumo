from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_conta(consumo_m3):
    tarifa_fixa = 11.18

    # Faixas de consumo (volume da faixa, preço por m³)
    faixas = [
        (7, 4.13),
        (6, 4.96),
        (7, 9.82),
        (10, 14.25),
        (15, 21.37),
        (float('inf'), 27.77)  # Acima de 45 m³
    ]

    total = tarifa_fixa
    restante = consumo_m3

    for volume, preco in faixas:
        if restante <= 0:
            break
        consumo_faixa = min(restante, volume)
        total += consumo_faixa * preco
        restante -= consumo_faixa

    return round(total, 2)


def calcular_economia(consumo_antes, consumo_depois):
    valor_antes = calcular_conta(consumo_antes)
    valor_depois = calcular_conta(consumo_depois)
    economia = valor_antes - valor_depois

    return {
        "valor_antes": valor_antes,
        "valor_depois": valor_depois,
        "economia_reais": round(economia, 2)
    }
 
@app.route("/", methods=["GET", "POST", "PUT"])
def main():
    selecionType = "initial"
    consumo_antes = ""
    consumo_depois = ""
    diferenca_consumo = 0
    valor_antes = 0
    valor_depois = 0
    economia = 0
    valorKwh = 0

    if request.method == "POST":
        if "water" in request.form:
            selecionType = "water"
        elif "energy" in request.form:
            selecionType = "energy"
        if "calculate_water" in request.form:
            selecionType = "calculate_water"
        elif "calculate_energy" in request.form:
            selecionType = "calculate_energy"
        if "result_water" in request.form:
            consumo_antes = request.form["consumo_antes"]
            consumo_depois = request.form["consumo_depois"]
            diferenca_consumo = float(consumo_antes) - float(consumo_depois)
            valor_antes = calcular_conta(float(consumo_antes))
            valor_depois = calcular_conta(float(consumo_depois))
            economia = valor_antes - valor_depois
            selecionType = "result_water"
        elif "result_energy" in request.form:
            consumo_antes = request.form["consumo_antes"]
            consumo_depois = request.form["consumo_depois"]
            valorKwh = request.form["valor_kwh"]
            valorKwh = valorKwh.replace(",", ".")
            valor_antes = float(consumo_antes) * float(valorKwh)
            valor_depois = float(consumo_depois) * float(valorKwh)
            diferenca_consumo = float(consumo_antes) - float(consumo_depois)

            economia = diferenca_consumo * float(valorKwh)
            selecionType = "result_energy"

    if selecionType == "calculate_water":
         return render_template('calculate_water.html', type=selecionType)
    elif selecionType == "calculate_energy":
         return render_template('calculate_energy.html', type=selecionType)
    if selecionType == "result_water":
        return render_template('result_water.html', valor_antes=valor_antes, valor_depois=valor_depois, economia=economia, diferenca_consumo=diferenca_consumo)
    elif selecionType == "result_energy":
        return render_template('result_energy.html', valor_antes=valor_antes, valor_depois=valor_depois, economia=economia, diferenca_consumo=diferenca_consumo)
    else:         
        return render_template('index.html', type=selecionType)
 
if __name__ == '__main__':
	app.run(debug=True)