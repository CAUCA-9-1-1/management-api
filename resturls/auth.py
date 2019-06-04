from datetime import datetime
from .base import Base
from .webuser import Webuser
from ..core.database import Database
from ..core.token import Token
from ..models.access_token import AccessToken
from ..models.apis_action import ApisAction
from ..config import setup as config

class Auth(Token, Base):
    expires_in_minutes = config.TOKEN_TIMEOUT
    mapping_method = {
        'GET': 'check_active_user',
        'PUT': 'logon',
        'POST': 'register',
        'DELETE': 'logout',
        'PATCH': '',
    }

    def logon(self, username=None, password=None, session_id=None):
        data = super().logon(username, password, session_id)

        return self._check_active_token(data['data']['access_token'])

    def check_active_user(self, token_id=None, session_id=None):
        if token_id is not None:
            return self._check_active_token(token_id)
        elif session_id is not None:
            return self._check_active_session(session_id)
        else:
            return  # No token id or session id received

    def _check_active_session(self, session_id):
        with Database() as db:
            data = db.query(AccessToken).filter(AccessToken.session_id == session_id,
                                                AccessToken.logout_on is None).first()

            if data is None or self.valid_token(data.access_token) is False:
                return  # Invalid token id

            return {
                'data': self._get_user_information(data)
            }

    def _check_active_token(self, token_id):
        with Database() as db:
            data = db.query(AccessToken).filter(AccessToken.access_token == token_id).first()

            if data is None or self.valid_token(token_id) is False:
                return  # Invalid token id

            return {
                'data': self._get_user_information(data)
            }

    def _get_user_information(self, data):
        with Database() as db:
            user = Webuser().get(data.id_webuser)
            apis = db.query(ApisAction).filter(
                ApisAction.id_webuser == data.id_webuser).order_by(
                ApisAction.action_time.desc()).first()

            data.username = user['data'].username
            data.user_attributes = user['data'].attributes
            data.user_ip = apis.action_ip if apis is not None else None

            return data

    def register(self, body):
        return Webuser().create(body)

    def logout(self, token_id):
        with Database() as db:
            data = db.query(AccessToken).filter(AccessToken.access_token == token_id).first()

            if data is not None:
                data.logout_on = datetime.now()
                db.commit()

        return {
            'message': 'auth successfully logout'
        }
