# Funções auxiliares para formatar dados, logs e validações
import datetime


def formatar_data_iso(data: str) -> str:
    """Formata uma data ISO para exibição (YYYY-MM-DD)"""
    try:
        return data.split("T")[0]
    except Exception:
        return data


def formatar_data_hora(timestamp: str) -> str:
    """Formata um timestamp para exibição (DD/MM/YYYY HH:MM)"""
    try:
        if not timestamp:
            return ""

        # Se for uma string de data ISO
        if isinstance(timestamp, str) and "T" in timestamp:
            dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        # Se for um timestamp Unix
        elif isinstance(timestamp, (int, float)):
            dt = datetime.datetime.fromtimestamp(timestamp)
        # Se for uma string de data padrão
        else:
            dt = datetime.datetime.fromisoformat(str(timestamp))

        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(timestamp)


def truncar_texto(texto: str, max_len: int = 50) -> str:
    """Trunca um texto longo adicionando reticências"""
    if not texto:
        return ""
    if len(texto) <= max_len:
        return texto
    return texto[:max_len] + "..."
