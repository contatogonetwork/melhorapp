"""
Utilitários para exportação de dados
"""

import datetime
import json
import os


class CommentExporter:
    """Classe para exportar comentários em diferentes formatos"""

    @staticmethod
    def export_to_json(comments, filename, metadata=None):
        """
        Exporta comentários para arquivo JSON

        Args:
            comments: Lista de objetos Comment
            filename: Nome do arquivo de saída
            metadata: Dicionário com metadados adicionais

        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            # Converter comentários para dicionários
            comments_data = []
            for comment in comments:
                if hasattr(comment, "to_dict"):
                    comment_dict = comment.to_dict()
                else:
                    # Se não for um objeto Comment com método to_dict
                    comment_dict = {
                        "id": getattr(comment, "id", ""),
                        "text": getattr(comment, "text", ""),
                        "author": getattr(comment, "author", ""),
                        "timestamp": getattr(comment, "timestamp", ""),
                        "video_timestamp": getattr(comment, "video_timestamp", 0),
                        "is_resolved": getattr(comment, "is_resolved", False),
                    }

                # Adicionar timestamp formatado
                if "video_timestamp" in comment_dict:
                    seconds = comment_dict["video_timestamp"] // 1000
                    minutes = seconds // 60
                    seconds = seconds % 60
                    comment_dict["formatted_timestamp"] = f"{minutes:02d}:{seconds:02d}"

                comments_data.append(comment_dict)

            # Estrutura do arquivo
            data = {
                "metadata": metadata or {},
                "export_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "comments": comments_data,
                "total_comments": len(comments_data),
                "resolved_comments": sum(
                    1 for c in comments_data if c.get("is_resolved", False)
                ),
            }

            # Criar diretório se não existir
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # Salvar arquivo
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return True
        except Exception as e:
            print(f"Erro ao exportar comentários para JSON: {str(e)}")
            return False

    @staticmethod
    def export_to_pdf(comments, filename, title="Comentários", metadata=None):
        """
        Exporta comentários para arquivo PDF

        Args:
            comments: Lista de objetos Comment
            filename: Nome do arquivo de saída
            title: Título do documento
            metadata: Dicionário com metadados adicionais

        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            # Verificar se ReportLab está disponível
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import letter
                from reportlab.lib.styles import (
                    ParagraphStyle,
                    getSampleStyleSheet,
                )
                from reportlab.platypus import (
                    Paragraph,
                    SimpleDocTemplate,
                    Spacer,
                    Table,
                    TableStyle,
                )
            except ImportError:
                print(
                    "ReportLab não está instalado. Use 'pip install reportlab' para instalar."
                )
                return False

            # Criar diretório se não existir
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # Criar documento
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            title_style = styles["Title"]
            normal_style = styles["Normal"]
            subtitle_style = ParagraphStyle(
                "Subtitle",
                parent=styles["Heading2"],
                fontSize=14,
                spaceAfter=12,
            )

            # Elementos do PDF
            elements = []

            # Título
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))

            # Metadados
            if metadata:
                info_text = ""
                for key, value in metadata.items():
                    info_text += f"<b>{key}:</b> {value}<br/>"
                elements.append(Paragraph(info_text, normal_style))
                elements.append(Spacer(1, 15))

            # Estatísticas
            resolved_count = sum(
                1 for c in comments if getattr(c, "is_resolved", False)
            )
            elements.append(
                Paragraph(
                    f"<b>Total de comentários:</b> {len(comments)}<br/>"
                    f"<b>Comentários resolvidos:</b> {resolved_count}",
                    normal_style,
                )
            )
            elements.append(Spacer(1, 20))

            # Subtítulo para tabela
            elements.append(Paragraph("Lista de Comentários", subtitle_style))
            elements.append(Spacer(1, 10))

            # Tabela de comentários
            data = [["Autor", "Tempo", "Status", "Comentário"]]

            for comment in comments:
                # Formatação do timestamp
                ts = getattr(comment, "video_timestamp", 0)
                seconds = ts // 1000
                minutes = seconds // 60
                seconds = seconds % 60
                formatted_time = f"{minutes:02d}:{seconds:02d}"

                # Status de resolução
                status = (
                    "Resolvido"
                    if getattr(comment, "is_resolved", False)
                    else "Pendente"
                )

                # Texto do comentário (limitado para tabela)
                text = getattr(comment, "text", "")
                if len(text) > 80:
                    text = text[:77] + "..."

                data.append(
                    [
                        getattr(comment, "author", ""),
                        formatted_time,
                        status,
                        text,
                    ]
                )

            # Criar tabela
            table = Table(data, colWidths=[100, 60, 70, 260])
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgrey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("WORDWRAP", (3, 1), (3, -1), True),
                    ]
                )
            )
            elements.append(table)

            # Comentários detalhados
            elements.append(Spacer(1, 30))
            elements.append(Paragraph("Comentários Detalhados", subtitle_style))

            for i, comment in enumerate(comments):
                elements.append(Spacer(1, 15))

                # Formatação do timestamp
                ts = getattr(comment, "video_timestamp", 0)
                seconds = ts // 1000
                minutes = seconds // 60
                seconds = seconds % 60
                formatted_time = f"{minutes:02d}:{seconds:02d}"

                # Status
                status = (
                    "Resolvido"
                    if getattr(comment, "is_resolved", False)
                    else "Pendente"
                )

                # Cabeçalho do comentário
                elements.append(
                    Paragraph(
                        f"<b>{i+1}. {getattr(comment, 'author', '')}</b> ({formatted_time}) - "
                        f"<i>{status}</i>",
                        ParagraphStyle(
                            "CommentTitle",
                            parent=normal_style,
                            fontName="Helvetica-Bold",
                            fontSize=10,
                        ),
                    )
                )

                # Texto do comentário
                elements.append(Paragraph(getattr(comment, "text", ""), normal_style))
                elements.append(Spacer(1, 5))

            # Rodapé
            elements.append(Spacer(1, 30))
            elements.append(
                Paragraph(
                    f"Exportado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                    normal_style,
                )
            )

            # Gerar PDF
            doc.build(elements)
            return True

        except Exception as e:
            print(f"Erro ao exportar comentários para PDF: {str(e)}")
            return False
