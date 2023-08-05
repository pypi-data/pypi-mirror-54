import logging

from isc_common import ws
from isc_common.models.base_ref import BaseRef, BaseRefManager, BaseRefQuerySet
from isc_common.ws.webSocket import WebSocket

logger = logging.getLogger(__name__)


class ChatsQuerySet(BaseRefQuerySet):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class ChatsManager(BaseRefManager):

    @staticmethod
    def refresh_chat_menu(user, logger):
        from isc_common.auth.http.LoginRequets import LoginRequest
        message = dict(
            type='refresh_chat_menu',
            user_id=user.id,
            chatInfo=LoginRequest.get_chats(user)
        )
        WebSocket.send_message(
            host=ws.WS_HOST,
            port=ws.WS_PORT,
            channel=f'common_{user.username}',
            message=message,
            logger=logger
        )

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
        }
        return res

    def get_queryset(self):
        return ChatsQuerySet(self.model, using=self._db)


class Chats(BaseRef):
    objects = ChatsManager()

    def __str__(self):
        return f"id : {self.code}, code : {self.code}, name : {self.name}, code : {self.description},"

    class Meta:
        verbose_name = 'Групповые чаты'
