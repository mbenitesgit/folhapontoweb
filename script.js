document.getElementById('calcular').addEventListener('click', function() {
    const mes = document.getElementById('mes').value;
    const ano = document.getElementById('ano').value;
    const diasDoMes = new Date(ano, mes, 0).getDate();

    let horasNormaisTotal = 0;
    let horasExtrasTotal = 0;

    for (let dia = 1; dia <= diasDoMes; dia++) {
        const entrada = document.getElementById(`entrada-${dia}`).value;
        const saida = document.getElementById(`saida-${dia}`).value;
        const folga = document.getElementById(`folga-${dia}`).checked;

        const horasNormais = calcularHorasNormais(entrada, saida, folga);
        const horasExtras = calcularHorasExtras(horasNormais);

        horasNormaisTotal += horasNormais;
        horasExtrasTotal += horasExtras;
    }

    const resultado = `Horas Normais Total: ${horasNormaisTotal}h | Horas Extras Total: ${horasExtrasTotal}h`;
    document.getElementById('resultado').innerHTML = resultado;
});

function calcularHorasNormais(entrada, saida, folga) {
    if (folga) {
        return 8; // Se folga, considerar 8 horas
    }

    const entradaHoraMinuto = entrada.split(':').map(Number);
    const saidaHoraMinuto = saida.split(':').map(Number);

    const entradaDate = new Date(2024, 0, 1, entradaHoraMinuto[0], entradaHoraMinuto[1]);
    const saidaDate = new Date(2024, 0, 1, saidaHoraMinuto[0], saidaHoraMinuto[1]);
    
    const diferenca = (saidaDate - entradaDate) / 1000 / 60 / 60;

    return diferenca < 8 ? 8 : diferenca;
}

function calcularHorasExtras(horasNormais) {
    return horasNormais > 8 ? horasNormais - 8 : 0;
}

document.getElementById('formulario').addEventListener('change', function(event) {
    if (event.target && event.target.matches('select#mes, input#ano')) {
        atualizarTabela();
    }
});

function atualizarTabela() {
    const mes = document.getElementById('mes').value;
    const ano = document.getElementById('ano').value;
    const diasDoMes = new Date(ano, mes, 0).getDate();

    const tabelaDias = document.getElementById('tabela-dias');
    tabelaDias.innerHTML = ''; // Limpar a tabela antes de atualizar

    for (let dia = 1; dia <= diasDoMes; dia++) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${dia}</td>
            <td><input type="text" id="entrada-${dia}" class="flatpickr-input" required></td>
            <td><input type="text" id="saida-${dia}" class="flatpickr-input" required></td>
            <td><input type="checkbox" id="folga-${dia}"></td>
        `;
        tabelaDias.appendChild(tr);
    }
}

// Inicializar a tabela quando a página carregar
atualizarTabela();
