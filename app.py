import streamlit as st
import pandas as pd
import io
from calculadora_horas import classify_hours, read_pdf_espelho, read_template_csv, read_template_excel, export_to_excel, normalize_date

st.title("Calculadora de Horas Extras — CCT x RH")

st.write("Faça upload do seu espelho ponto (PDF ou CSV) e, opcionalmente, informe salário para cálculo de valores.")

salario = st.number_input("Salário mensal (opcional, R$)", min_value=0.0, value=0.0, step=100.0)
base_segsex = st.time_input("Base diária Seg–Sex", value=pd.to_datetime("08:00").time())

feriados_file = st.file_uploader("CSV de feriados (opcional)", type=["csv"])
ponto_file = st.file_uploader("Espelho ponto (PDF ou CSV)", type=["pdf","csv","xlsx"])

if st.button("Calcular", type="primary") and ponto_file:
    feriados_list = []
    if feriados_file:
        feriados_df = pd.read_csv(feriados_file)
        for v in feriados_df["data"].tolist():
            d = normalize_date(str(v)) or pd.to_datetime(str(v)).date()
            feriados_list.append(d)

    if ponto_file.name.lower().endswith(".pdf"):
        df_work = read_pdf_espelho(ponto_file)
    elif ponto_file.name.lower().endswith(".csv"):
        df_work = read_template_csv(ponto_file)
    else:
        df_work = read_template_excel(ponto_file)

    base_diaria = {0:480,1:480,2:480,3:480,4:480,5:0,6:0}

    df_det, df_resumo = classify_hours(
        df_work,
        feriados=feriados_list,
        base_diaria_minutos=base_diaria,
        salario_mensal=salario if salario > 0 else None
    )

    buffer = io.BytesIO()
    export_to_excel(df_det, df_resumo, buffer)
    buffer.seek(0)

    st.success("Cálculo concluído!")
    st.dataframe(df_resumo)
    st.download_button("Baixar relatório (Excel)", data=buffer,
                       file_name="relatorio_horas.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
