document.addEventListener('DOMContentLoaded', function () {
    carregarAnos();
    carregarMeses();
});

function carregarAnos() {
    const selectAno = document.getElementById('year');
    const anoAtual = new Date().getFullYear();

    for (let ano = anoAtual; ano >= anoAtual - 5; ano--) {
        const option = document.createElement('option');
        option.value = ano;
        option.text = ano;
        selectAno.add(option);
    }
}

function carregarMeses() {
    const selectMes = document.getElementById('month');
    const meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ];

    for (let i = 0; i < meses.length; i++) {
        const option = document.createElement('option');
        option.value = i + 1; // Mês é indexado de 1 a 12
        option.text = meses[i];
        selectMes.add(option);
    }
}

function carregarHorarios() {
    const anoSelecionado = document.getElementById('year').value;
    const mesSelecionado = document.getElementById('month').value;

    // Simulando dados de exemplo
    const horarios = [
        { data: '2024-02-01', entrada: '08:00', saida: '17:00' },
        { data: '2024-02-02', entrada: '09:00', saida: '18:00' },
        // Adicione mais horários conforme necessário
    ];

    exibirHorarios(horarios);
}

function inserirHorario() {
    const anoSelecionado = document.getElementById('year').value;
    const mesSelecionado = document.getElementById('month').value;
    const entrada = document.getElementById('entrada').value;
    const saida = document.getElementById('saida').value;

    // Validar entrada e saída conforme necessário

    const dataInicio = new Date(anoSelecionado, mesSelecionado - 1, 1); // Meses são indexados de 0 a 11
    const ultimoDia = new Date(anoSelecionado, mesSelecionado, 0).getDate();

    const horarios = [];

    for (let dia = 1; dia <= ultimoDia; dia++) {
        const data = new Date(anoSelecionado, mesSelecionado - 1, dia);
        const horario = {
            data: formatarData(data),
            entrada: entrada,
            saida: saida
        };
        horarios.push(horario);
    }

    exibirHorarios(horarios);
}

function formatarData(data) {
    const ano = data.getFullYear();
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const dia = String(data.getDate()).padStart(2, '0');
    return `${ano}-${mes}-${dia}`;
}

function exibirHorarios(horarios) {
    const tabela = document.getElementById('horariosTable');
    const tbody = document.getElementById('horariosBody');

    // Limpar tabela antes de adicionar novos dados
    tbody.innerHTML = '';

    horarios.forEach(horario => {
        const row = tbody.insertRow();
        const dataCell = row.insertCell(0);
        const entradaCell = row.insertCell(1);
        const saidaCell = row.insertCell(2);

        dataCell.textContent = horario.data;
        entradaCell.textContent = horario.entrada;
        saidaCell.textContent = horario.saida;
    });
}
