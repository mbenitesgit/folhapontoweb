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
            <td><input type="time" id="entrada-${dia}" required></td>
            <td><input type="time" id="saida-${dia}" required></td>
            <td><input type="checkbox" id="folga-${dia}"></td>
        `;
        tabelaDias.appendChild(tr);
    }
}

// Inicializar a tabela quando a página carregar
atualizarTabela();
