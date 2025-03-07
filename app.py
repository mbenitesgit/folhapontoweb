from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Função para calcular a diferença entre dois horários
def calcular_diferenca_hora(entrada, saida):
    entrada = datetime.strptime(entrada, "%H:%M")
    saida = datetime.strptime(saida, "%H:%M")
    if saida < entrada:
        saida += timedelta(days=1)
    return (saida - entrada).seconds / 3600  # Retorna em horas

# Função para calcular horas trabalhadas (descontando intervalo)
def calcular_horas_trabalhadas(hora_entrada, hora_saida, hora_intervalo_entrada, hora_intervalo_saida):
    horas_trabalhadas = calcular_diferenca_hora(hora_entrada, hora_saida)
    horas_intervalo = calcular_diferenca_hora(hora_intervalo_entrada, hora_intervalo_saida)
    return horas_trabalhadas - horas_intervalo

# Função para calcular horas extras
def calcular_horas_extras(horas_trabalhadas, escala_trabalho, dia_feriado, dia_folga, domingo_extra):
    horas_normais = 0
    horas_extra_75 = 0
    horas_extra_100 = 0
    if escala_trabalho == "7h20":
        jornada_diaria = 7 + 20/60  # 7h20
    elif escala_trabalho == "8h+4h":
        jornada_diaria = 8  # Considera 8h diárias e 4h aos finais de semana

    if dia_feriado:
        horas_extra_100 = horas_trabalhadas
        return horas_normais, horas_extra_75, horas_extra_100

    if dia_folga:
        return 0, 0, 0

    if domingo_extra:
        horas_extra_100 = horas_trabalhadas
        return horas_normais, horas_extra_75, horas_extra_100

    if horas_trabalhadas > jornada_diaria:
        if horas_trabalhadas <= jornada_diaria + 2:
            horas_extra_75 = horas_trabalhadas - jornada_diaria
        else:
            horas_extra_75 = 2
            horas_extra_100 = horas_trabalhadas - (jornada_diaria + 2)
        horas_normais = jornada_diaria
    else:
        horas_normais = horas_trabalhadas

    return horas_normais, horas_extra_75, horas_extra_100

def calcular_valor_horas_extras(salario, horas_extra_75, horas_extra_100):
    valor_hora = salario / (44 * 4)
    valor_hora_extra_75 = valor_hora * 1.75
    valor_hora_extra_100 = valor_hora * 2

    valor_extra_75 = horas_extra_75 * valor_hora_extra_75
    valor_extra_100 = horas_extra_100 * valor_hora_extra_100

    return valor_extra_75, valor_extra_100

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    mes = request.form.get('mes')
    escala = request.form.get('escala')
    salario = float(request.form.get('salario'))
    dados_dias = {}  # Você precisa definir isso com base nas entradas dos usuários

    # Exemplo de dados de dias para cálculo
    dados_dias[1] = {
        'hora_entrada': '08:00',
        'hora_saida': '17:00',
        'hora_intervalo_entrada': '12:00',
        'hora_intervalo_saida': '13:00',
        'feriado': False,
        'folga': False,
        'domingo_extra': False
    }

    resultado = calcular_folha_ponto(mes, 2025, escala, salario, dados_dias)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
