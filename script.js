function adicionarHorarios() {
    var table = document.getElementById("horariosTable");
    var newRow = table.insertRow(table.rows.length);

    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);
    var cell3 = newRow.insertCell(2);
    var cell4 = newRow.insertCell(3);

    var day = table.rows.length - 1;

    cell1.innerHTML = day;
    cell2.innerHTML = '<input type="time" id="entrada' + day + '" required>';
    cell3.innerHTML = '<input type="time" id="saida' + day + '" required>';
    cell4.innerHTML = '<input type="checkbox" id="folga' + day + '">';
}

function calcularFolha() {
    var mes = document.getElementById("mes").value;
    var ano = document.getElementById("ano").value;
    var remuneracao_mensal = parseFloat(document.getElementById("remuneracao_mensal").value);
    var jornada_mensal = parseFloat(document.getElementById("jornada_mensal").value);
    
    var totalHorasNormais = 0;
    var totalHorasExtras = 0;

    for (var day = 1; day <= 31; day++) {
        var entrada = document.getElementById("entrada" + day).value;
        var saida = document.getElementById("saida" + day).value;
        var folga = document.getElementById("folga" + day).checked;

        if (!folga && entrada && saida) {
            var entradaTimestamp = new Date('2000-01-01 ' + entrada).getTime();
            var saidaTimestamp = new Date('2000-01-01 ' + saida).getTime();
            var diferenca = (saidaTimestamp - entradaTimestamp - 3600000) / 3600000; // 1 hora = 3600 segundos

            if (diferenca > jornada_mensal) {
                totalHorasNormais += jornada_mensal;
                totalHorasExtras += diferenca - jornada_mensal;
            } else {
                totalHorasNormais += diferenca;
            }
        }
    }

    var resultadoDiv = document.getElementById("resultado");
    resultadoDiv.innerHTML = "Horas Normais: " + totalHorasNormais.toFixed(2) + " horas<br>";
    resultadoDiv.innerHTML += "Horas Extras: " + totalHorasExtras.toFixed(2) + " horas<br>";

    // Cálculos adicionais, se necessário

    // Exemplo: Cálculo do salário
    var valorHora = remuneracao_mensal / jornada_mensal;
    var salario = (totalHoras
