function criarCampoData(mesAno) {
    const [ano, mes] = mesAno.split("-");
    const diasNoMes = new Date(ano, mes, 0).getDate();

    const pontoBody = document.getElementById('pontoBody');
    pontoBody.innerHTML = ""; // Limpa os campos existentes antes de adicionar novos

    for (let dia = 1; dia <= diasNoMes; dia++) {
        const data = `${ano}-${mes.toString().padStart(2, '0')}-${dia.toString().padStart(2, '0')}`;
        const tr = document.createElement('tr');

        const tdData = document.createElement('td');
        tdData.textContent = data;
        tr.appendChild(tdData);

        const tdEntrada = document.createElement('td');
        const inputEntrada = document.createElement('input');
        inputEntrada.type = 'time';
        tdEntrada.appendChild(inputEntrada);
        tr.appendChild(tdEntrada);

        const tdSaida = document.createElement('td');
        const inputSaida = document.createElement('input');
        inputSaida.type = 'time';
        tdSaida.appendChild(inputSaida);
        tr.appendChild(tdSaida);

        pontoBody.appendChild(tr);
    }
}

function calcularHoras() {
    const nomeFuncionario = document.getElementById('funcionarioNome').value;
    const mesAno = document.getElementById('mesAno').value;

    // Verifica se o mês/ano foi selecionado
    if (!mesAno) {
        alert('Selecione o mês/ano antes de calcular as horas.');
        return;
    }

    criarCampoData(mesAno);

    const pontoBody = document.getElementById('pontoBody');
    const linhas = pontoBody.getElementsByTagName('tr');

    // Loop para percorrer as linhas da tabela
    for (let i = 0; i < linhas.length; i++) {
        const data = linhas[i].querySelector('td:nth-child(1)').innerText;
        const entrada = linhas[i].querySelector('td:nth-child(2) input').value;
        const saida = linhas[i].querySelector('td:nth-child(3) input').value;

        // Aqui você pode calcular as horas trabalhadas para cada dia (entrada e saída)
        // e fazer o que for necessário com essas informações
        console.log(`Data: ${data}, Entrada: ${entrada}, Saída: ${saida}`);
    }
}
