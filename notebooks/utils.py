import pandas as pd
import re
import calendar
from datetime import datetime

def aproximar_limite_valido(data_str):
    # Se for nulo, ignora
    if pd.isna(data_str):
        return pd.NaT

    # Extrai os números (Ano, Mês, Dia, Hora, Minuto, Segundo)
    match = re.match(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', str(data_str).strip())
    
    # Se a string for muito bizarra e não tiver esse formato, tenta o padrão do Pandas
    if not match:
        return pd.to_datetime(data_str, errors='coerce')

    ano, mes, dia, hora, minuto, segundo = map(int, match.groups())

    # --- LÓGICA DE APROXIMAÇÃO (CLAMPING) ---
    
    # 1. Aproxima o Mês (limites: 1 a 12)
    mes_valido = max(1, min(mes, 12))

    # 2. Aproxima o Dia (descobre o último dia válido daquele mês específico e trava nele)
    ultimo_dia_mes = calendar.monthrange(ano, mes_valido)[1]
    dia_valido = max(1, min(dia, ultimo_dia_mes))

    # 3. Aproxima a Hora (limites: 0 a 23)
    hora_valida = max(0, min(hora, 23))

    # 4. Aproxima o Minuto (limites: 0 a 59)
    minuto_valido = max(0, min(minuto, 59))

    # 5. Aproxima o Segundo (limites: 0 a 59)
    segundo_valido = max(0, min(segundo, 59))

    # Monta a data validada
    return datetime(ano, mes_valido, dia_valido, hora_valida, minuto_valido, segundo_valido)