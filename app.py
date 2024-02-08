from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    return render_template('index.html', meses=meses)

@app.route('/processa', methods=['POST'])
def processa():
    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')
        remuneracao_mensal = float(request.form.get('remuneracao_mensal'))
        jornada_mensal = float(request.form.get('jornada_mensal'))

        entradas = request.form.getlist('entrada')
        saidas = request.form.getlist('saida')
        folgas = request.form.getlist('folga')

        valor_hora = remuneracao_mensal / jornada_mensal

        total_horas_normais = 0
        total_horas_extras = 0

        for entrada, saida, folga in zip(entradas, saidas, folgas):
            if not folga and entrada and saida:
                entrada_timestamp = datetime.strptime(entrada, "%H:%M").timestamp()
                saida_timestamp = datetime.strptime(saida, "%H:%M").timestamp()
                diferenca = (saida_timestamp - entrada_timestamp - 3600) / 3600  # 1 hora = 3600 segundos

                if diferenca > jornada_mensal:
                    total_horas_normais += jornada_mensal
                    total_horas_extras += diferenca - jornada_mensal
                else:
                    total_horas_normais += diferenca

        salario = (total_horas_normais + total_horas_extras) * valor_hora

        return f"Horas Normais: {total_horas_normais:.2f} horas<br>" \
               f"Horas Extras: {total_horas_extras:.2f} horas<br>" \
               f"Salário Total: R$ {salario:.2f}"

if __name__ == '__main__':
    app.run(debug=True)
