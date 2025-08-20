import re
import math
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
import pandas as pd
import fitz  # PyMuPDF
import openpyxl

# ========= Utilidades de tempo =========
def to_minutes(hhmm: str) -> int:
    hh, mm = hhmm.split(":")
    return int(hh) * 60 + int(mm)

def minutes_to_hhmm(m: float) -> str:
    total = int(round(m))
    hh = total // 60
    mm = total % 60
    return f"{hh:02d}:{mm:02d}"

def sum_intervals_to_minutes(pairs: List[Tuple[str, str]]) -> int:
    total = 0
    for ini, fim in pairs:
        try:
            total += max(0, to_minutes(fim) - to_minutes(ini))
        except Exception:
            continue
    return total

def is_weekend(d: date) -> bool:
    return d.weekday() >= 5

# ========= Leitura de PDF =========
DATE_PAT = re.compile(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})')
TIME_PAT = re.compile(r'([01]?\d|2[0-3]):[0-5]\d')

def normalize_date(s: str) -> Optional[date]:
    s = s.replace("\", "/").replace("-", "/")
    parts = s.split("/")
    if len(parts) != 3:
        return None
    d, m, y = parts
    if len(y) == 2:
        y = "20" + y
    try:
        return datetime(int(y), int(m), int(d)).date()
    except ValueError:
        return None

def extract_work_pairs_from_line(line: str) -> List[Tuple[str, str]]:
    times = [m.group(0) for m in TIME_PAT.finditer(line)]
    pairs = []
    for i in range(0, len(times) - 1, 2):
        ini = times[i]
        fim = times[i + 1]
        if to_minutes(fim) > to_minutes(ini):
            pairs.append((ini, fim))
    return pairs

def read_pdf_espelho(file) -> pd.DataFrame:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    rows: Dict[date, List[Tuple[str, str]]] = {}
    for page in doc:
        text = page.get_text("text")
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            date_matches = DATE_PAT.findall(line)
            d_obj = None
            for dm in date_matches:
                d_obj = normalize_date(dm)
                if d_obj:
                    break
            if not d_obj:
                continue
            pairs = extract_work_pairs_from_line(line)
            if d_obj not in rows:
                rows[d_obj] = []
            rows[d_obj].extend(pairs)
    data, intervalos, minutos = [], [], []
    for d_obj, pairs in sorted(rows.items()):
        total_min = sum_intervals_to_minutes(pairs)
        interval_str = ", ".join([f"{a}-{b}" for a, b in pairs])
        data.append(d_obj)
        intervalos.append(interval_str)
        minutos.append(total_min)
    df = pd.DataFrame({"data": data, "intervalos": intervalos, "minutos_trabalhados": minutos})
    return df

# ========= Leitura de CSV/Excel =========
def read_template_csv(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    return normalize_template_df(df)

def read_template_excel(file) -> pd.DataFrame:
    df = pd.read_excel(file, engine="openpyxl")
    return normalize_template_df(df)

def normalize_template_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    def parse_date_any(x):
        if pd.isna(x):
            return None
        if isinstance(x, (datetime, pd.Timestamp)):
            return x.date()
        s = str(x).strip()
        d = normalize_date(s)
        if d:
            return d
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return None
    df["data"] = df["data"].map(parse_date_any)
    def parse_pairs(cell):
        if pd.isna(cell):
            return []
        s = str(cell)
        parts = re.split(r'[;,]\s*', s)
        pairs = []
        for p in parts:
            if "-" in p:
                a, b = p.split("-", 1)
                a = a.strip()
                b = b.strip()
                if TIME_PAT.match(a) and TIME_PAT.match(b):
                    if to_minutes(b) > to_minutes(a):
                        pairs.append((a, b))
        return pairs
    df["pairs"] = df["intervalos"].map(parse_pairs)
    df["minutos_trabalhados"] = df["pairs"].map(sum_intervals_to_minutes)
    out = df[["data", "intervalos", "minutos_trabalhados"]].dropna(subset=["data"]).sort_values("data")
    return out.reset_index(drop=True)

# ========= Cálculo =========
def classify_hours(df_work, feriados=None, base_diaria_minutos=None, salario_mensal=None, horas_mensais_base=200.0):
    if base_diaria_minutos is None:
        base_diaria_minutos = {0:480, 1:480, 2:480, 3:480, 4:480, 5:0, 6:0}
    feriados_set = set(feriados or [])
    rows = []
    for _, r in df_work.iterrows():
        d = r["data"]
        wk = d.weekday()
        is_feriado = d in feriados_set
        base_min = base_diaria_minutos.get(wk, 0)
        worked_min = int(r["minutos_trabalhados"] or 0)
        if is_feriado or wk >= 5:
            he100_cct_min = worked_min
            he75_cct_min = 0
        else:
            extra_min = max(0, worked_min - base_min)
            he75_cct_min = min(extra_min, 120)
            he100_cct_min = max(0, extra_min - 120)
        he75_rh_min = he75_cct_min + 2 * he100_cct_min
        he100_rh_min = 0
        row = {
            "data": d,
            "dia_semana": ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"][wk],
            "feriado": is_feriado,
            "intervalos": r.get("intervalos", ""),
            "trabalhadas_hhmm": minutes_to_hhmm(worked_min),
            "base_hhmm": minutes_to_hhmm(base_min),
            "HE75_CCT_hhmm": minutes_to_hhmm(he75_cct_min),
            "HE100_CCT_hhmm": minutes_to_hhmm(he100_cct_min),
            "HE75_RH_hhmm": minutes_to_hhmm(he75_rh_min),
            "HE100_RH_hhmm": minutes_to_hhmm(he100_rh_min),
            "ΔHE75_hhmm": minutes_to_hhmm(he75_rh_min - he75_cct_min),
            "ΔHE100_hhmm": minutes_to_hhmm(he100_rh_min - he100_cct_min),
        }
        if salario_mensal is not None and horas_mensais_base > 0:
            hora_base = salario_mensal / horas_mensais_base
            he75_cct_h = he75_cct_min / 60.0
            he100_cct_h = he100_cct_min / 60.0
            he75_rh_h = he75_rh_min / 60.0
            he100_rh_h = he100_rh_min / 60.0
            valor_cct = he75_cct_h * 1.75 * hora_base + he100_cct_h * 2.00 * hora_base
            valor_rh  = he75_rh_h  * 1.75 * hora_base + he100_rh_h  * 2.00 * hora_base
            row.update({
                "valor_correto_R$": round(valor_cct, 2),
                "valor_RH_R$": round(valor_rh, 2),
                "Δvalor_R$": round(valor_rh - valor_cct, 2),
            })
        rows.append(row)
    df_det = pd.DataFrame(rows)
    resumo = {
        "HE75_CCT_total": minutes_to_hhmm(sum([to_minutes(x) for x in df_det["HE75_CCT_hhmm"]])),
        "HE100_CCT_total": minutes_to_hhmm(sum([to_minutes(x) for x in df_det["HE100_CCT_hhmm"]])),
        "HE75_RH_total": minutes_to_hhmm(sum([to_minutes(x) for x in df_det["HE75_RH_hhmm"]])),
        "HE100_RH_total": minutes_to_hhmm(sum([to_minutes(x) for x in df_det["HE100_RH_hhmm"]])),
        "ΔHE75_total": minutes_to_hhmm(sum([to_minutes(x) for x in df_det["ΔHE75_hhmm"]])),
        "ΔHE100_total": minutes_to_hhmm(sum([to_minutes(x) for x in df_det["ΔHE100_hhmm"]])),
    }
    if "valor_correto_R$" in df_det.columns:
        resumo.update({
            "valor_correto_total_R$": round(df_det["valor_correto_R$"].sum(), 2),
            "valor_RH_total_R$": round(df_det["valor_RH_R$"].sum(), 2),
            "Δvalor_total_R$": round(df_det["Δvalor_R$"].sum(), 2),
        })
    df_resumo = pd.DataFrame([resumo])
    return df_det, df_resumo

# ========= Exportação =========
def export_to_excel(df_det: pd.DataFrame, df_resumo: pd.DataFrame, buffer) -> None:
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_det.to_excel(writer, index=False, sheet_name="Detalhado")
        df_resumo.to_excel(writer, index=False, sheet_name="Resumo")
