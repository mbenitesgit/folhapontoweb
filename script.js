function calcularHoras() {
    const nomeFuncionario = document.getElementById('funcionarioNome').value;
    const mesAno = document.getElementById('mesAno').value;

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
