<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Folha de Ponto</title>
    <link rel="stylesheet" href="styles.css"> <!-- Adicione um arquivo CSS para personalizar o layout -->
</head>
<body>

    <div class="container">
        <h2>Calculadora de Folha de Ponto</h2>

        <form action="processa.php" method="post">
            <label for="mes">Selecione o mês:</label>
            <select name="mes" id="mes">
                <?php
                $meses = [
                    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
                ];
                foreach ($meses as $key => $mes) {
                    echo "<option value='".($key+1)."'>$mes</option>";
                }
                ?>
            </select>

            <label for="ano">Ano:</label>
            <input type="number" name="ano" id="ano" value="2024" min="2024" max="2100">

            <label for="remuneracao_mensal">Remuneração Mensal:</label>
            <input type="number" name="remuneracao_mensal" id="remuneracao_mensal" step="0.01" placeholder="Digite a remuneração mensal" required>

            <label for="jornada_mensal">Jornada Mensal (horas):</label>
            <input type="number" name="jornada_mensal" id="jornada_mensal" placeholder="Digite a jornada mensal" required>

            <label for="horarios">Horários:</label>
            <table>
                <tr>
                    <th>Dia</th>
                    <th>Entrada</th>
                    <th>Saída</th>
                    <th>Folga</th>
                </tr>
                <?php
                for ($dia = 1; $dia <= 31; $dia++) {
                    echo "<tr>
                            <td>$dia</td>
                            <td><input type='time' name='entrada[$dia]' required></td>
                            <td><input type='time' name='saida[$dia]' required></td>
                            <td><input type='checkbox' name='folga[$dia]'></td>
                        </tr>";
                }
                ?>
            </table>

            <input type="submit" value="Calcular">
        </form>
    </div>

</body>
</html>
