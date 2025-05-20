import datetime
import uuid

from database.Database import Database


class VideoRepository:
    """Repositório para operações com edições de vídeo"""

    def __init__(self):
        """Inicializa o repositório com uma conexão ao banco de dados"""
        self.db = Database()

    # ===== Operações com edições de vídeo =====

    def create_video_edit(self, video_data):
        """
        Cria uma nova edição de vídeo

        Parâmetros:
        - video_data: dicionário com os dados da edição

        Retorna:
        - ID da edição criada
        """
        video_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.db.execute(
            """
            INSERT INTO video_edits (
                id, event_id, editor_id, title, deadline, style, status, video_path,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                video_id,
                video_data.get("event_id", ""),
                video_data.get("editor_id", ""),
                video_data.get("title", ""),
                video_data.get("deadline", ""),
                video_data.get("style", ""),
                video_data.get("status", "Em edição"),
                video_data.get("video_path", ""),
                now,
                now,
            ),
        )
        self.db.commit()
        return video_id

    def get_video_edit_by_id(self, video_id):
        """
        Busca uma edição de vídeo pelo ID

        Parâmetros:
        - video_id: ID da edição

        Retorna:
        - Dicionário com os dados da edição ou None se não encontrado
        """
        result = self.db.fetch_one(
            "SELECT * FROM video_edits WHERE id = ?", (video_id,)
        )
        return dict(result) if result else None

    def update_video_edit(self, video_id, video_data):
        """
        Atualiza uma edição de vídeo existente

        Parâmetros:
        - video_id: ID da edição
        - video_data: dicionário com os dados atualizados

        Retorna:
        - True se atualizado com sucesso, False caso contrário
        """
        # Verificar se a edição existe
        existing_video = self.get_video_edit_by_id(video_id)
        if not existing_video:
            return False

        # Timestamp atual
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Executar atualização
        self.db.execute(
            """
            UPDATE video_edits SET
                editor_id = ?,
                title = ?,
                deadline = ?,
                style = ?,
                status = ?,
                video_path = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                video_data.get("editor_id", existing_video["editor_id"]),
                video_data.get("title", existing_video["title"]),
                video_data.get("deadline", existing_video["deadline"]),
                video_data.get("style", existing_video["style"]),
                video_data.get("status", existing_video["status"]),
                video_data.get("video_path", existing_video["video_path"]),
                now,
                video_id,
            ),
        )

        # Salvar alterações
        self.db.commit()

        return True

    def delete_video_edit(self, video_id):
        """
        Remove uma edição de vídeo e seus dados relacionados

        Parâmetros:
        - video_id: ID da edição a ser removida

        Retorna:
        - True se removido com sucesso, False caso contrário
        """
        # Verificar se a edição existe
        existing_video = self.get_video_edit_by_id(video_id)
        if not existing_video:
            return False

        # Remover comentários associados
        self.db.execute(
            "DELETE FROM video_comments WHERE video_edit_id = ?", (video_id,)
        )

        # Remover entregas associadas
        self.db.execute(
            "DELETE FROM editor_deliveries WHERE video_edit_id = ?",
            (video_id,),
        )

        # Remover a edição
        self.db.execute("DELETE FROM video_edits WHERE id = ?", (video_id,))

        # Salvar alterações
        self.db.commit()

        return True

    def get_all_video_edits(self):
        """
        Busca todas as edições de vídeo

        Retorna:
        - Lista de edições como dicionários
        """
        results = self.db.fetch_all("SELECT * FROM video_edits ORDER BY deadline ASC")

        return [dict(row) for row in results]

    def get_video_edits_by_event(self, event_id):
        """
        Busca edições de vídeo associadas a um evento específico

        Parâmetros:
        - event_id: ID do evento

        Retorna:
        - Lista de edições como dicionários
        """
        results = self.db.fetch_all(
            "SELECT * FROM video_edits WHERE event_id = ? ORDER BY deadline ASC",
            (event_id,),
        )

        return [dict(row) for row in results]

    def get_video_edits_by_editor(self, editor_id):
        """
        Busca edições de vídeo atribuídas a um editor específico

        Parâmetros:
        - editor_id: ID do editor

        Retorna:
        - Lista de edições como dicionários
        """
        results = self.db.fetch_all(
            "SELECT * FROM video_edits WHERE editor_id = ? ORDER BY deadline ASC",
            (editor_id,),
        )

        return [dict(row) for row in results]

    def get_video_edits_by_status(self, status):
        """
        Busca edições de vídeo com um status específico

        Parâmetros:
        - status: status a ser buscado

        Retorna:
        - Lista de edições como dicionários
        """
        results = self.db.fetch_all(
            "SELECT * FROM video_edits WHERE status = ? ORDER BY deadline ASC",
            (status,),
        )

        return [dict(row) for row in results]

    # ===== Operações com entregas de editores =====

    def create_delivery(self, delivery_data):
        """
        Cria uma nova entrega para uma edição de vídeo

        Parâmetros:
        - delivery_data: dicionário com os dados da entrega

        Retorna:
        - ID da entrega criada
        """
        # Gerar ID único
        delivery_id = str(uuid.uuid4())

        # Timestamp atual
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Executar inserção
        self.db.execute(
            """
            INSERT INTO editor_deliveries (
                id, video_edit_id, asset_refs, is_submitted, submitted_at,
                approval_status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                delivery_id,
                delivery_data.get("video_edit_id", ""),
                delivery_data.get("asset_refs", ""),
                0,  # Não submetido por padrão
                None,
                "Pendente",
                now,
                now,
            ),
        )

        # Salvar alterações
        self.db.commit()

        return delivery_id

    def submit_delivery(self, delivery_id, asset_refs):
        """
        Marca uma entrega como submetida

        Parâmetros:
        - delivery_id: ID da entrega
        - asset_refs: referências aos assets entregues

        Retorna:
        - True se atualizado com sucesso, False caso contrário
        """
        # Verificar se a entrega existe
        result = self.db.fetch_one(
            "SELECT * FROM editor_deliveries WHERE id = ?", (delivery_id,)
        )
        if not result:
            return False

        # Timestamp atual
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Executar atualização
        self.db.execute(
            """
            UPDATE editor_deliveries SET
                asset_refs = ?,
                is_submitted = ?,
                submitted_at = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (asset_refs, 1, now, now, delivery_id),
        )

        # Salvar alterações
        self.db.commit()

        return True

    def update_approval_status(self, delivery_id, status, feedback=None):
        """
        Atualiza o status de aprovação de uma entrega

        Parâmetros:
        - delivery_id: ID da entrega
        - status: novo status de aprovação
        - feedback: feedback opcional para rejeições

        Retorna:
        - True se atualizado com sucesso, False caso contrário
        """
        # Verificar se a entrega existe
        result = self.db.fetch_one(
            "SELECT * FROM editor_deliveries WHERE id = ?", (delivery_id,)
        )
        if not result:
            return False

        # Timestamp atual
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Executar atualização
        self.db.execute(
            """
            UPDATE editor_deliveries SET
                approval_status = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (status, now, delivery_id),
        )

        # Quando aprovado, atualizar também o status da edição de vídeo
        if status == "Aprovado":
            self.db.execute(
                """
                UPDATE video_edits SET
                    status = 'Entregue',
                    updated_at = ?
                WHERE id = (
                    SELECT video_edit_id FROM editor_deliveries WHERE id = ?
                )
                """,
                (now, delivery_id),
            )

        # Salvar alterações
        self.db.commit()

        return True

    def get_deliveries_by_video(self, video_edit_id):
        """
        Busca todas as entregas relacionadas a uma edição de vídeo

        Parâmetros:
        - video_edit_id: ID da edição de vídeo

        Retorna:
        - Lista de entregas como dicionários
        """
        results = self.db.fetch_all(
            "SELECT * FROM editor_deliveries WHERE video_edit_id = ?",
            (video_edit_id,),
        )

        return [dict(row) for row in results]

    def get_delivery_by_edit_id(self, edit_id):
        """
        Busca a entrega mais recente para uma edição de vídeo

        Parâmetros:
        - edit_id: ID da edição de vídeo

        Retorna:
        - Dicionário com os dados da entrega ou None se não encontrado
        """
        result = self.db.fetch_one(
            """
            SELECT * FROM editor_deliveries
            WHERE video_edit_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (edit_id,),
        )

        if not result:
            return None

        return {
            "id": result[0],
            "video_edit_id": result[1],
            "asset_refs": result[2],
            "is_submitted": bool(result[3]),
            "submitted_at": result[4],
            "approval_status": result[5],
            "created_at": result[6],
            "updated_at": result[7],
        }

    def cancel_delivery(self, delivery_id):
        """
        Cancela uma entrega marcando-a como não enviada

        Parâmetros:
        - delivery_id: ID da entrega

        Retorna:
        - True se atualizado com sucesso, False caso contrário
        """
        # Verificar se a entrega existe
        result = self.db.fetch_one(
            "SELECT * FROM editor_deliveries WHERE id = ?", (delivery_id,)
        )
        if not result:
            return False

        # Timestamp atual
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Executar atualização
        self.db.execute(
            """
            UPDATE editor_deliveries SET
                is_submitted = 0,
                approval_status = 'Não enviada',
                updated_at = ?
            WHERE id = ?
            """,
            (now, delivery_id),
        )

        self.db.commit()
        return True
