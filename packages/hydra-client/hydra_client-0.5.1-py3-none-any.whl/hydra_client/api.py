import typing

import attr
import requests

from .model import Resource
from .consent import ConsentRequest, ConsentSession
from .login import LoginRequest, LoginSession
from .logout import LogoutRequest
from .oauth2 import OAuth2Client
from .version import Version


class HydraAdmin(Resource):
    def __init__(self, url: str, session: requests.Session = None):
        self.url_ = url
        self.session_ = session or requests.Session()

    def clients(
        self, limit: int = None, offset: int = None
    ) -> typing.List[OAuth2Client]:
        return OAuth2Client._list(self, limit, offset)

    def client(self, id: str) -> OAuth2Client:
        return OAuth2Client._get(self, id)

    def create_client(
        self,
        allowed_cors_origins: typing.List[str] = None,
        audience: typing.List[str] = None,
        backchannel_logout_session_required: bool = None,
        backchannel_logout_uri: str = None,
        client_id: str = None,
        client_name: str = None,
        client_secret: str = None,
        client_secret_expires_at: int = None,
        client_uri: str = None,
        contacts: typing.List[str] = None,
        frontchannel_logout_session_required: bool = None,
        frontchannel_logout_uri: str = None,
        grant_types: typing.List[str] = None,
        jwks: dict = None,
        jwks_uri: str = None,
        logo_uri: str = None,
        owner: str = None,
        policy_uri: str = None,
        post_logout_redirect_uris: typing.List[str] = None,
        redirect_uris: typing.List[str] = None,
        redirect_object_signing_alg: str = None,
        request_uris: typing.List[str] = None,
        response_uris: typing.List[str] = None,
        scope: str = None,
        sector_identifier_uri: str = None,
        subject_type: str = None,
        token_endpoint_auth_method: str = None,
        tos_uri: str = None,
        userinfo_signed_response_alg: str = None,
    ) -> OAuth2Client:
        return OAuth2Client.create(
            self,
            allowed_cors_origins,
            audience,
            backchannel_logout_session_required,
            backchannel_logout_uri,
            client_id,
            client_name,
            client_secret,
            client_secret_expires_at,
            client_uri,
            contacts,
            frontchannel_logout_session_required,
            frontchannel_logout_uri,
            grant_types,
            jwks,
            jwks_uri,
            logo_uri,
            owner,
            policy_uri,
            post_logout_redirect_uris,
            redirect_uris,
            redirect_object_signing_alg,
            request_uris,
            response_uris,
            scope,
            sector_identifier_uri,
            subject_type,
            token_endpoint_auth_method,
            tos_uri,
            userinfo_signed_response_alg,
        )

    def login_request(self, challenge: str) -> LoginRequest:
        return LoginRequest._get(self, challenge)

    def consent_request(self, challenge: str) -> ConsentRequest:
        return ConsentRequest._get(self, challenge)

    def logout_request(self, challenge: str) -> LogoutRequest:
        return LogoutRequest._get(self, challenge)

    def consent_sessions(self, subject: str) -> typing.Iterator[ConsentSession]:
        yield from ConsentSession._list(self, subject)

    def revoke_consent_sessions(self, subject: str, client: str = None) -> None:
        ConsentSession._revoke(self, subject, client)

    def invalidate_login_sessions(self, subject: str) -> None:
        LoginSession._invalidate_all(self, subject)

    def version(self) -> str:
        return Version._get(self)
