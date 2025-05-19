import json
from datetime import datetime

import bcrypt

from database.db_manager import DatabaseManager


class BaseModel:
    def __init__(self):
        self.db = DatabaseManager()

    def _get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class User(BaseModel):
    def __init__(self, user_id=None):
        super().__init__()
        self.id = user_id
        self.username = None
        self.email = None
        self.password = None
        self.full_name = None
        self.role = None
        self.profile_picture = None
        self.created_at = None
        self.updated_at = None

        if user_id:
            self.load()

    def load(self):
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE id = ?", (self.id,)
        )
        if user:
            self.username = user["username"]
            self.email = user["email"]
            self.password = user["password"]
            self.full_name = user["full_name"]
            self.role = user["role"]
            self.profile_picture = user["profile_picture"]
            self.created_at = user["created_at"]
            self.updated_at = user["updated_at"]
            return True
        return False

    def authenticate(self, username, password):
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            self.id = user["id"]
            self.load()
            return True
        return False

    def save(self):
        now = self._get_timestamp()
        if self.id:
            # Atualizar usuário existente
            return self.db.update(
                "users",
                {
                    "username": self.username,
                    "email": self.email,
                    "full_name": self.full_name,
                    "role": self.role,
                    "profile_picture": self.profile_picture,
                    "updated_at": now,
                },
                {"id": self.id},
            )
        else:
            # Criar novo usuário
            # Hash da senha
            hashed_password = bcrypt.hashpw(
                self.password.encode("utf-8"), bcrypt.gensalt()
            )

            user_id = self.db.insert(
                "users",
                {
                    "username": self.username,
                    "email": self.email,
                    "password": hashed_password.decode("utf-8"),
                    "full_name": self.full_name,
                    "role": self.role,
                    "profile_picture": self.profile_picture,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            if user_id:
                self.id = user_id
                return True
            return False

    def delete(self):
        if self.id:
            return self.db.delete("users", {"id": self.id})
        return False

    def change_password(self, new_password):
        if self.id:
            hashed_password = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            )
            return self.db.update(
                "users",
                {
                    "password": hashed_password.decode("utf-8"),
                    "updated_at": self._get_timestamp(),
                },
                {"id": self.id},
            )
        return False

    @classmethod
    def get_all(cls):
        db = DatabaseManager()
        users = db.fetch_all("SELECT * FROM users ORDER BY username")
        return users


class Event(BaseModel):
    def __init__(self, event_id=None):
        super().__init__()
        self.id = event_id
        self.name = None
        self.start_date = None
        self.end_date = None
        self.location = None
        self.client_id = None
        self.status = None
        self.created_by = None
        self.created_at = None
        self.updated_at = None

        if event_id:
            self.load()

    def load(self):
        event = self.db.fetch_one(
            "SELECT * FROM events WHERE id = ?", (self.id,)
        )
        if event:
            self.name = event["name"]
            self.start_date = event["start_date"]
            self.end_date = event["end_date"]
            self.location = event["location"]
            self.client_id = event["client_id"]
            self.status = event["status"]
            self.created_by = event["created_by"]
            self.created_at = event["created_at"]
            self.updated_at = event["updated_at"]
            return True
        return False

    def save(self):
        now = self._get_timestamp()
        if self.id:
            # Atualizar evento existente
            return self.db.update(
                "events",
                {
                    "name": self.name,
                    "start_date": self.start_date,
                    "end_date": self.end_date,
                    "location": self.location,
                    "client_id": self.client_id,
                    "status": self.status,
                    "updated_at": now,
                },
                {"id": self.id},
            )
        else:
            # Criar novo evento
            event_id = self.db.insert(
                "events",
                {
                    "name": self.name,
                    "start_date": self.start_date,
                    "end_date": self.end_date,
                    "location": self.location,
                    "client_id": self.client_id,
                    "status": self.status,
                    "created_by": self.created_by,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            if event_id:
                self.id = event_id
                return True
            return False

    def delete(self):
        if self.id:
            return self.db.delete("events", {"id": self.id})
        return False

    def get_team(self):
        if self.id:
            return self.db.fetch_all(
                """
                SELECT et.*, u.full_name, u.username, u.email, u.profile_picture 
                FROM event_team et
                JOIN users u ON et.user_id = u.id
                WHERE et.event_id = ?
            """,
                (self.id,),
            )
        return []

    def get_briefing(self):
        if self.id:
            return self.db.fetch_one(
                """
                SELECT * FROM briefings WHERE event_id = ?
            """,
                (self.id,),
            )
        return None

    def get_sponsors(self):
        if self.id:
            sponsors = self.db.fetch_all(
                """
                SELECT * FROM sponsors WHERE event_id = ?
            """,
                (self.id,),
            )

            for sponsor in sponsors:
                sponsor["actions"] = self.db.fetch_all(
                    """
                    SELECT sa.*, u1.full_name as responsible_name, u2.full_name as editor_name
                    FROM sponsor_actions sa
                    LEFT JOIN users u1 ON sa.responsible_id = u1.id
                    LEFT JOIN users u2 ON sa.editor_id = u2.id
                    WHERE sa.sponsor_id = ?
                """,
                    (sponsor["id"],),
                )

            return sponsors
        return []

    def get_stages(self):
        if self.id:
            stages = self.db.fetch_all(
                """
                SELECT * FROM stages WHERE event_id = ?
            """,
                (self.id,),
            )

            for stage in stages:
                stage["attractions"] = self.db.fetch_all(
                    """
                    SELECT * FROM attractions WHERE stage_id = ? ORDER BY time
                """,
                    (stage["id"],),
                )

            return stages
        return []

    def get_realtime_deliveries(self):
        if self.id:
            return self.db.fetch_all(
                """
                SELECT rd.*, u.full_name as editor_name
                FROM realtime_deliveries rd
                LEFT JOIN users u ON rd.editor_id = u.id
                WHERE rd.event_id = ?
                ORDER BY rd.delivery_time
            """,
                (self.id,),
            )
        return []

    def get_post_deliveries(self):
        if self.id:
            return self.db.fetch_one(
                """
                SELECT * FROM post_deliveries WHERE event_id = ?
            """,
                (self.id,),
            )
        return None

    def get_timeline(self):
        if self.id:
            return self.db.fetch_all(
                """
                SELECT t.*, u.full_name as responsible_name
                FROM timeline_items t
                LEFT JOIN users u ON t.responsible_id = u.id
                WHERE t.event_id = ?
                ORDER BY t.start_time
            """,
                (self.id,),
            )
        return []

    def get_videos(self):
        if self.id:
            return self.db.fetch_all(
                """
                SELECT v.*, u.full_name as editor_name
                FROM videos v
                LEFT JOIN users u ON v.editor_id = u.id
                WHERE v.event_id = ?
                ORDER BY v.updated_at DESC
            """,
                (self.id,),
            )
        return []

    def get_assets(self):
        if self.id:
            return self.db.fetch_all(
                """
                SELECT a.*, u.full_name as uploader_name
                FROM assets a
                LEFT JOIN users u ON a.uploaded_by = u.id
                WHERE a.event_id = ?
                ORDER BY a.uploaded_at DESC
            """,
                (self.id,),
            )
        return []

    @classmethod
    def get_all(cls, status=None):
        db = DatabaseManager()
        query = "SELECT e.*, u.full_name as client_name FROM events e LEFT JOIN users u ON e.client_id = u.id"
        params = None

        if status:
            query += " WHERE e.status = ?"
            params = (status,)

        query += " ORDER BY e.start_date DESC"

        return db.fetch_all(query, params)


class Briefing(BaseModel):
    def __init__(self, briefing_id=None):
        super().__init__()
        self.id = briefing_id
        self.event_id = None
        self.general_info = None
        self.style_info = None
        self.references_info = None
        self.created_at = None
        self.updated_at = None

        if briefing_id:
            self.load()

    def load(self):
        briefing = self.db.fetch_one(
            "SELECT * FROM briefings WHERE id = ?", (self.id,)
        )
        if briefing:
            self.event_id = briefing["event_id"]
            self.general_info = briefing["general_info"]
            self.style_info = briefing["style_info"]
            self.references_info = briefing["references_info"]
            self.created_at = briefing["created_at"]
            self.updated_at = briefing["updated_at"]
            return True
        return False

    def load_by_event(self, event_id):
        briefing = self.db.fetch_one(
            "SELECT * FROM briefings WHERE event_id = ?", (event_id,)
        )
        if briefing:
            self.id = briefing["id"]
            self.event_id = briefing["event_id"]
            self.general_info = briefing["general_info"]
            self.style_info = briefing["style_info"]
            self.references_info = briefing["references_info"]
            self.created_at = briefing["created_at"]
            self.updated_at = briefing["updated_at"]
            return True
        return False

    def save(self):
        now = self._get_timestamp()
        if self.id:
            # Atualizar briefing existente
            return self.db.update(
                "briefings",
                {
                    "general_info": self.general_info,
                    "style_info": self.style_info,
                    "references_info": self.references_info,
                    "updated_at": now,
                },
                {"id": self.id},
            )
        else:
            # Criar novo briefing
            briefing_id = self.db.insert(
                "briefings",
                {
                    "event_id": self.event_id,
                    "general_info": self.general_info,
                    "style_info": self.style_info,
                    "references_info": self.references_info,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            if briefing_id:
                self.id = briefing_id
                return True
            return False


class Sponsor(BaseModel):
    def __init__(self, sponsor_id=None):
        super().__init__()
        self.id = sponsor_id
        self.event_id = None
        self.name = None

        if sponsor_id:
            self.load()

    def load(self):
        sponsor = self.db.fetch_one(
            "SELECT * FROM sponsors WHERE id = ?", (self.id,)
        )
        if sponsor:
            self.event_id = sponsor["event_id"]
            self.name = sponsor["name"]
            return True
        return False

    def save(self):
        if self.id:
            # Atualizar patrocinador existente
            return self.db.update(
                "sponsors", {"name": self.name}, {"id": self.id}
            )
        else:
            # Criar novo patrocinador
            sponsor_id = self.db.insert(
                "sponsors", {"event_id": self.event_id, "name": self.name}
            )

            if sponsor_id:
                self.id = sponsor_id
                return True
            return False

    def delete(self):
        if self.id:
            # Excluir as ações relacionadas primeiro
            self.db.delete("sponsor_actions", {"sponsor_id": self.id})
            # Excluir o patrocinador
            return self.db.delete("sponsors", {"id": self.id})
        return False

    def get_actions(self):
        if self.id:
            return self.db.fetch_all(
                """
                SELECT sa.*, u1.full_name as responsible_name, u2.full_name as editor_name
                FROM sponsor_actions sa
                LEFT JOIN users u1 ON sa.responsible_id = u1.id
                LEFT JOIN users u2 ON sa.editor_id = u2.id
                WHERE sa.sponsor_id = ?
            """,
                (self.id,),
            )
        return []

    def add_action(self, action_data):
        if self.id:
            action_id = self.db.insert(
                "sponsor_actions",
                {
                    "sponsor_id": self.id,
                    "action_name": action_data["action_name"],
                    "capture_time": action_data.get("capture_time"),
                    "is_free_time": action_data.get("is_free_time", False),
                    "responsible_id": action_data.get("responsible_id"),
                    "is_real_time": action_data.get("is_real_time", False),
                    "delivery_time": action_data.get("delivery_time"),
                    "editor_id": action_data.get("editor_id"),
                    "instructions": action_data.get("instructions"),
                },
            )
            return action_id
        return None


class Video(BaseModel):
    def __init__(self, video_id=None):
        super().__init__()
        self.id = video_id
        self.event_id = None
        self.title = None
        self.description = None
        self.editor_id = None
        self.status = None
        self.version = None
        self.file_path = None
        self.created_at = None
        self.updated_at = None

        if video_id:
            self.load()

    def load(self):
        video = self.db.fetch_one(
            "SELECT * FROM videos WHERE id = ?", (self.id,)
        )
        if video:
            self.event_id = video["event_id"]
            self.title = video["title"]
            self.description = video["description"]
            self.editor_id = video["editor_id"]
            self.status = video["status"]
            self.version = video["version"]
            self.file_path = video["file_path"]
            self.created_at = video["created_at"]
            self.updated_at = video["updated_at"]
            return True
        return False

    def save(self):
        now = self._get_timestamp()
        if self.id:
            # Atualizar vídeo existente
            return self.db.update(
                "videos",
                {
                    "title": self.title,
                    "description": self.description,
                    "editor_id": self.editor_id,
                    "status": self.status,
                    "version": self.version,
                    "file_path": self.file_path,
                    "updated_at": now,
                },
                {"id": self.id},
            )
        else:
            # Criar novo vídeo
            video_id = self.db.insert(
                "videos",
                {
                    "event_id": self.event_id,
                    "title": self.title,
                    "description": self.description,
                    "editor_id": self.editor_id,
                    "status": self.status,
                    "version": self.version,
                    "file_path": self.file_path,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            if video_id:
                self.id = video_id
                return True
            return False

    def delete(self):
        if self.id:
            # Excluir comentários relacionados primeiro
            self.db.delete("video_comments", {"video_id": self.id})
            # Excluir o vídeo
            return self.db.delete("videos", {"id": self.id})
        return False

    def get_comments(self):
        if self.id:
            return self.db.fetch_all(
                """
                SELECT c.*, u.full_name, u.username, u.profile_picture
                FROM video_comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.video_id = ?
                ORDER BY c.created_at
            """,
                (self.id,),
            )
        return []

    def add_comment(self, user_id, comment, timestamp=None):
        if self.id:
            return self.db.insert(
                "video_comments",
                {
                    "video_id": self.id,
                    "user_id": user_id,
                    "comment": comment,
                    "timestamp": timestamp,
                    "created_at": self._get_timestamp(),
                },
            )
        return None


class Asset(BaseModel):
    def __init__(self, asset_id=None):
        super().__init__()
        self.id = asset_id
        self.event_id = None
        self.name = None
        self.file_path = None
        self.asset_type = None
        self.category = None
        self.uploaded_by = None
        self.uploaded_at = None

        if asset_id:
            self.load()

    def load(self):
        asset = self.db.fetch_one(
            "SELECT * FROM assets WHERE id = ?", (self.id,)
        )
        if asset:
            self.event_id = asset["event_id"]
            self.name = asset["name"]
            self.file_path = asset["file_path"]
            self.asset_type = asset["asset_type"]
            self.category = asset["category"]
            self.uploaded_by = asset["uploaded_by"]
            self.uploaded_at = asset["uploaded_at"]
            return True
        return False

    def save(self):
        now = self._get_timestamp()
        if self.id:
            # Atualizar asset existente
            return self.db.update(
                "assets",
                {
                    "name": self.name,
                    "file_path": self.file_path,
                    "asset_type": self.asset_type,
                    "category": self.category,
                },
                {"id": self.id},
            )
        else:
            # Criar novo asset
            asset_id = self.db.insert(
                "assets",
                {
                    "event_id": self.event_id,
                    "name": self.name,
                    "file_path": self.file_path,
                    "asset_type": self.asset_type,
                    "category": self.category,
                    "uploaded_by": self.uploaded_by,
                    "uploaded_at": now,
                },
            )

            if asset_id:
                self.id = asset_id
                return True
            return False

    def delete(self):
        if self.id:
            # Excluir o asset
            return self.db.delete("assets", {"id": self.id})
        return False
