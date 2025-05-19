def export_comments(self):
    """Exporta os comentários da edição atual para um arquivo"""
    # Verificar se existem comentários para exportar
    if (
        not hasattr(self, "comment_items")
        or not self.comment_items
        or len(self.comment_items) == 0
    ):
        QMessageBox.information(
            self, "Exportar Comentários", "Não há comentários para exportar."
        )
        return

    # Obter lista de comentários
    comments = []
    for item in self.comment_items:
        if hasattr(item, "comment"):
            comments.append(item.comment)

    # Diálogo para escolher o formato e local do arquivo
    formats = ["JSON (*.json)", "PDF (*.pdf)"]
    selected_format, _ = QInputDialog.getItem(
        self,
        "Exportar Comentários",
        "Selecione o formato de exportação:",
        formats,
        0,
        False,
    )

    if not selected_format:  # Usuário cancelou
        return

    # Definir extensão do arquivo
    extension = ".json" if "JSON" in selected_format else ".pdf"

    # Diálogo para escolher onde salvar o arquivo
    file_name, _ = QFileDialog.getSaveFileName(
        self,
        "Exportar Comentários",
        f"comentarios_edicao{extension}",
        selected_format,
    )

    if not file_name:  # Usuário cancelou
        return

    # Obter metadados da edição
    titulo_edicao = "Edição sem título"
    if (
        hasattr(self, "current_editing")
        and self.current_editing
        and "title" in self.current_editing
    ):
        titulo_edicao = self.current_editing["title"]

    metadata = {
        "título_edição": titulo_edicao,
        "total_comentários": len(comments),
        "comentários_resolvidos": sum(1 for c in comments if c.is_resolved),
    }

    # Exportar com base no formato selecionado
    success = False
    if extension == ".json":
        success = CommentExporter.export_to_json(comments, file_name, metadata)
    else:
        success = CommentExporter.export_to_pdf(
            comments, file_name, "Comentários da Edição", metadata
        )

    # Notificar o usuário sobre o resultado
    if success:
        QMessageBox.information(
            self,
            "Exportar Comentários",
            f"Comentários exportados com sucesso para:\n{file_name}",
        )
    else:
        QMessageBox.critical(
            self,
            "Erro na Exportação",
            f"Não foi possível exportar os comentários para {file_name}.",
        )
