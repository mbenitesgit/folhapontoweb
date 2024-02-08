<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mes = $_POST["mes"];
    $ano = $_POST["ano"];
    $remuneracao_mensal = $_POST["remuneracao_mensal"];
    $jornada_mensal = $_POST["jornada_mensal"];
    $entradas = $_POST["entrada"];
    $saidas = $_POST["saida"];
    $folgas = isset($_POST["folga"]) ? $_POST["folga"] : [];

    // Lógica para calcular horas normais e extras com 1 hora de intervalo
    $valorHora = $remuneracao_mensal / $jornada_mensal; // Valor da hora

    $totalHorasNormais = 0;
    $totalHorasExtras = 0;

    foreach ($entradas as $dia => $entrada) {
        $saida = $saidas[$dia];

        // Verificar se é um dia de folga
        if (isset($folgas[$dia]) && $folgas[$dia] == 'on') {
            continue; // Ignorar dias de folga
        }

        if (!empty($entrada) && !empty($saida)) {
            $entradaTimestamp = strtotime($entrada);
            $saidaTimestamp = strtotime($saida);

            // Subtrai 1 hora para o intervalo
            $diferenca = $saidaTimestamp - $entradaTimestamp - 3600; // 1 hora = 3600 segundos

            $horasTrabalhadas = $diferenca / 3600; // 1 hora = 3600 segundos

            if ($horasTrabalhadas > 8) {
                $totalHorasNormais += 8; // Considera as primeiras 8 horas como normais
                $totalHorasExtras += $horasTrabalhadas - 8;
            } else {
                $totalHorasNormais += $horasTrabalhadas;
            }
        }
    }

    // Exibindo a quantidade de horas trabalhadas e horas extras
    echo "Horas Normais: " . number_format($totalHorasNormais, 2) . " horas<br>";
    echo "Horas Extras: " . number_format($totalHorasExtras, 2) . " horas<br>";

    // Cálculos adicionais, se necessário

    // Exemplo: Cálculo do salário
    $salario = $totalHorasNormais * $valorHora + $totalHorasExtras * ($valorHora * 1.5); // Exemplo com hora extra 50%

    // Exibindo o salário
    echo "Salário Total: R$ " . number_format($salario, 2, ',', '.');
}
?>
