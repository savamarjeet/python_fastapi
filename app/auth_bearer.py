import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .const import ALGORITHM, JWT_SECRET_KEY
from app.utils import get_token_from_db

def decodeJWT(jwtoken: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM)
        return payload
    except InvalidTokenError as e:
        # Signature has expired
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            return payload.get("sub")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
            if payload:
                # Check if the token exists in the databases
                db_token = get_token_from_db(user_id = int(payload["sub"]))  # "sub" is the user identifier in the token
                if not db_token:
                    payload = None
        except Exception as e:
            print("Exception check", str(e))
            payload = None
        return payload

jwt_bearer = JWTBearer()
