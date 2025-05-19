def load_comments(self):
    """Carrega os comentários da edição atual"""
    try:
        # Limpar comentários existentes
        if hasattr(self, "comment_items"):
            for item in self.comment_items:
                if item.parent() and hasattr(item.parent(), "layout"):
                    item.parent().layout().removeWidget(item)
                    item.deleteLater()
            self.comment_items = []

        # Limpar o layout de comentários
        if hasattr(self, "comments_layout") and self.comments_layout:
            while self.comments_layout.count():
                item = self.comments_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # Verificar se temos uma edição atual
        if not hasattr(self, "current_editing") or not self.current_editing:
            return

        # Buscar comentários no repositório
        edit_id = self.current_editing.get("id")
        if not edit_id:
            return

        comments = self.comment_repository.get_by_edit_id(edit_id)
        if not comments:
            return

        # Adicionar comentários à interface
        for comment_data in comments:
            # Criar objeto Comment se necessário
            if not isinstance(comment_data, Comment):
                comment = Comment(
                    id=comment_data.get("id"),
                    text=comment_data.get("text", ""),
                    author=comment_data.get("user_id", ""),
                    timestamp=comment_data.get("created_at"),
                    video_timestamp=comment_data.get("timestamp", 0),
                    is_resolved=bool(comment_data.get("is_resolved", 0)),
                )
            else:
                comment = comment_data

            # Criar widget de comentário
            comment_item = CommentItem(
                comment,
                is_editor=(
                    self.current_user
                    and self.current_user.get("role") == "editor"
                ),
            )

            # Conectar sinais
            comment_item.goToTimestampRequested.connect(
                self.video_player.jumpToPosition
            )
            comment_item.resolveRequested.connect(self.resolve_comment)

            # Adicionar ao layout
            self.comments_layout.addWidget(comment_item)

            # Guardar referência
            self.comment_items.append(comment_item)

        # Adicionar comentários ao widget de marcadores
        if hasattr(self, "comment_markers") and self.comment_markers:
            comment_timestamps = [
                (c.video_timestamp, c.is_resolved)
                for c in [item.comment for item in self.comment_items]
            ]
            self.comment_markers.set_markers(
                comment_timestamps, self.video_player.mediaPlayer.duration()
            )

    except Exception as e:
        print(f"Erro ao carregar comentários: {str(e)}")
