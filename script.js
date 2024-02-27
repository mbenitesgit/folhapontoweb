function adicionarLinhaTabela() {
    const tabela = document.getElementById('tabelaHorarios');
    const novaLinha = document.createElement('tr');
    novaLinha.innerHTML = `
        <td><input type="date" class="data"></td>
        <td><input type="time" class="entrada"></td>
        <td><input type="time" class="saida"></td>
    `;
    tabela.appendChild(novaLinha);
}

function calcularFolhaPonto() {
    const cargaHoraria = parseFloat(document.getElementById('cargaHoraria').value);
    const salarioPorHora = parseFloat(document.getElementById('salario').value);
    const tabela = document.getElementById('tabelaHorarios').getElementsByTagName('tr');
    let totalHorasNormais = 0;
    let totalHorasExtras = 0;

    for (let i = 1; i < tabela.length; i++) {
        const data = tabela[i].querySelector('.data').value;
        const entrada = tabela[i].querySelector('.entrada').value;
        const saida = tabela[i].querySelector('.saida').value;

        // Implemente a lógica para calcular as horas normais e extras com base nos horários inseridos
        const horasTrabalhadas = calcularDiferencaHoras(entrada, saida);
        
        // Atualizar os totais
        totalHorasNormais += horasTrabalhadas;
    }

    // Lógica para calcular horas extras
    // ...

    // Atualizar os resultados na interface
    document.getElementById('totalHorasNormais').innerText = totalHorasNormais.toFixed(2);
    document.getElementById('totalHorasExtras').innerText = totalHorasExtras.toFixed(2);
}

function calcularDiferencaHoras(entrada, saida) {
    const horaEntrada = new Date(`2000-01-01T${entrada}`);
    const horaSaida = new Date(`2000-01-01T${saida}`);
    const diferencaMilissegundos = horaSaida - horaEntrada;
    const diferencaHoras = diferencaMilissegundos / (1000 * 60 * 60);
    return diferencaHoras;
}
