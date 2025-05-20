from datetime import datetime

import streamlit as st


class Notifications:
    """
    Gerencia notificações para os usuários na aplicação.
    Armazena notificações no estado da sessão e permite exibí-las de forma consistente.
    """

    @staticmethod
    def add(message, type="info", expiry_minutes=60, user_id=None):
        """
        Adiciona uma nova notificação

        Args:
            message: Texto da mensagem
            type: Tipo de notificação (info, success, warning, error)
            expiry_minutes: Tempo em minutos até a expiração
            user_id: ID do usuário destinatário (None = todos os usuários)
        """
        if "notifications" not in st.session_state:
            st.session_state.notifications = []

        # Criar notificação com timestamp
        notification = {
            "id": len(st.session_state.notifications) + 1,
            "message": message,
            "type": type,
            "timestamp": datetime.now(),
            "expiry": datetime.now().timestamp() + (expiry_minutes * 60),
            "read": False,
            "user_id": user_id,
        }

        # Adicionar à lista de notificações
        st.session_state.notifications.append(notification)

    @staticmethod
    def get_all(include_read=False, user_id=None):
        """
        Retorna todas as notificações ativas

        Args:
            include_read: Se deve incluir notificações já lidas
            user_id: ID do usuário para filtrar notificações (None = todas)

        Returns:
            list: Lista de notificações
        """
        if "notifications" not in st.session_state:
            st.session_state.notifications = []

        # Filtrar notificações expiradas
        now = datetime.now().timestamp()
        active_notifications = [
            n for n in st.session_state.notifications if n["expiry"] > now
        ]

        # Filtrar por status de leitura se necessário
        if not include_read:
            active_notifications = [n for n in active_notifications if not n["read"]]

        # Filtrar por usuário se especificado
        if user_id is not None:
            active_notifications = [
                n
                for n in active_notifications
                if n.get("user_id") is None or n.get("user_id") == user_id
            ]

        # Atualizar a lista de notificações ativas no estado da sessão
        st.session_state.notifications = active_notifications

        # Atualizar contador de notificações não lidas
        st.session_state.notification_count = len(
            [n for n in active_notifications if not n["read"]]
        )

        return active_notifications

    @staticmethod
    def get_unread_notifications(user_id=None):
        """
        Retorna apenas as notificações não lidas de um usuário específico

        Args:
            user_id: ID do usuário (None = todas as notificações do sistema)

        Returns:
            list: Lista de notificações não lidas
        """
        return Notifications.get_all(include_read=False, user_id=user_id)

    @staticmethod
    def mark_as_read(notification_id):
        """
        Marca uma notificação como lida

        Args:
            notification_id: ID da notificação
        """
        if "notifications" not in st.session_state:
            return

        for i, notification in enumerate(st.session_state.notifications):
            if notification["id"] == notification_id:
                st.session_state.notifications[i]["read"] = True
                break

    @staticmethod
    def mark_all_as_read():
        """Marca todas as notificações como lidas"""
        if "notifications" not in st.session_state:
            return

        for i, _ in enumerate(st.session_state.notifications):
            st.session_state.notifications[i]["read"] = True

    @staticmethod
    def display_notifications():
        """Exibe todas as notificações ativas na interface"""
        notifications = Notifications.get_all(include_read=False)

        if not notifications:
            return

        st.markdown("### Notificações")

        for notification in notifications:
            # Definir o estilo com base no tipo
            if notification["type"] == "success":
                icon = "✅"
            elif notification["type"] == "warning":
                icon = "⚠️"
            elif notification["type"] == "error":
                icon = "❌"
            else:  # info
                icon = "ℹ️"

            # Formatar o timestamp
            time_str = notification["timestamp"].strftime("%H:%M")

            # Exibir a notificação
            with st.container():
                col1, col2, col3 = st.columns([1, 10, 1])
                with col1:
                    st.write(icon)
                with col2:
                    st.write(f"{notification['message']}")
                    st.caption(f"{time_str}")
                with col3:
                    if st.button("✓", key=f"not_{notification['id']}"):
                        Notifications.mark_as_read(notification["id"])
                        st.rerun()

                st.divider()
