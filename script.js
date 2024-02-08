document.getElementById('calcular').addEventListener('click', function() {
    // Obter os valores dos campos
    const entrada = document.getElementById('entrada').value;
    const saida = document.getElementById('saida').value;
    const folga = document.getElementById('folga').checked;

    // Calcular horas normais e extras
    const horasNormais = calcularHorasNormais(entrada, saida, folga);
    const horasExtras = calcularHorasExtras(horasNormais);

    // Exibir resultado
    const resultado = `Horas Normais: ${horasNormais}h | Horas Extras: ${horasExtras}h`;
    document.getElementById('resultado').innerHTML = resultado;
});

function calcularHorasNormais(entrada, saida, folga) {
    const entradaDate = new Date(`2024-01-01T${entrada}`);
    const saidaDate = new Date(`2024-01-01T${saida}`);
    
    // Se folga, considerar 8 horas
    if (folga) {
        return 8;
    }

    // Calcular diferença em horas
    const diferenca = (saidaDate - entradaDate) / 1000 / 60 / 60;

    // Se menos de 8 horas, considerar 8 horas
    return diferenca < 8 ? 8 : diferenca;
}

function calcularHorasExtras(horasNormais) {
    // Se mais de 8 horas, considerar como horas extras
    return horasNormais > 8 ? horasNormais - 8 : 0;
}
