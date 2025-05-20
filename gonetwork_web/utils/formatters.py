import datetime
from typing import Any, Union


def formatar_data_iso(data: str) -> str:
    """Formata uma data ISO para exibição (YYYY-MM-DD)"""
    try:
        return data.split("T")[0]
    except Exception:
        return str(data)


def formatar_data_hora(timestamp: Union[str, int, float, datetime.datetime]) -> str:
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
        # Se já for um objeto datetime
        elif isinstance(timestamp, datetime.datetime):
            dt = timestamp
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


def formatar_status(status: str) -> str:
    """Formata o status para exibição com ícones"""
    status_map = {
        "concluido": "✅ Concluído",
        "concluído": "✅ Concluído",
        "em_andamento": "🔄 Em Andamento",
        "em andamento": "🔄 Em Andamento",
        "pendente": "⏳ Pendente",
        "atrasado": "⚠️ Atrasado",
        "cancelado": "❌ Cancelado",
    }

    # Normaliza o status para comparação
    status_norm = str(status).lower().replace(" ", "_")

    # Retorna o status formatado ou o original se não encontrado
    return status_map.get(status_norm, str(status))


def formatar_dinheiro(valor: Union[float, int, str]) -> str:
    """Formata um valor numérico como moeda (R$)"""
    try:
        if isinstance(valor, str):
            valor = float(
                valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
            )
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(valor)


def calcular_duracao(inicio: Any, fim: Any) -> str:
    """Calcula e formata a duração entre dois timestamps"""
    try:
        # Converter para datetime se necessário
        if isinstance(inicio, str) and "T" in inicio:
            inicio_dt = datetime.datetime.fromisoformat(inicio.replace("Z", "+00:00"))
        elif isinstance(inicio, (int, float)):
            inicio_dt = datetime.datetime.fromtimestamp(inicio)
        elif isinstance(inicio, datetime.datetime):
            inicio_dt = inicio
        else:
            inicio_dt = datetime.datetime.fromisoformat(str(inicio))

        if isinstance(fim, str) and "T" in fim:
            fim_dt = datetime.datetime.fromisoformat(fim.replace("Z", "+00:00"))
        elif isinstance(fim, (int, float)):
            fim_dt = datetime.datetime.fromtimestamp(fim)
        elif isinstance(fim, datetime.datetime):
            fim_dt = fim
        else:
            fim_dt = datetime.datetime.fromisoformat(str(fim))

        # Calcular duração
        duracao = fim_dt - inicio_dt

        # Formatar duração
        horas, resto = divmod(duracao.seconds, 3600)
        minutos, segundos = divmod(resto, 60)

        if duracao.days > 0:
            return f"{duracao.days}d {horas:02d}:{minutos:02d}"
        else:
            return f"{horas:02d}:{minutos:02d}"
    except Exception:
        return "Duração indisponível"
