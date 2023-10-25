#pylint: disable=E0401
""" Security methods to
    hash and verify passwords
"""
from datetime        import datetime, timedelta
from typing          import Optional, Union, Any
from passlib.context import CryptContext
import json
import jwt
from jwt.exceptions  import InvalidTokenError, ExpiredSignatureError, PyJWTError
from core.config     import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM   = "HS256"


class Security():
    """
    Security methods to hash and verify passwords.
    """

    def __init__(self):
        """
        Constructor to initialize the Security object.
        """
        self._pwd_context: CryptContext = pwd_context
        self._ALGORITHM  : str          = ALGORITHM


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """verify if a passwrod match with the
            passed plain

        Args:
            plain_password (str): password to validate
            hashed_password (str): hash to compare

        Returns:
            bool: True on success, False on error
        """
        return self._pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password: str) -> str:
        """get a hash from a plain_password

        Args:
            password (str): password to hash

        Returns:
            str: hashed password
        """
        return self._pwd_context.hash(password)


    def verify_password_reset_token(self, token: str) -> Optional[str]:
        """
        Verify a password reset token and
        extract the email from it.

        Args:
            token (str): The password reset token to verify.

        Returns:
            Optional[str]: The email associated with the token
                            if it's valid, else None.
        """
        try:
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[self._ALGORITHM]
            )
            return decoded_token["email"]
        except jwt.JWTError:
            return None


    def create_access_token(
        self,
        subject: Union[str, Any],
        expires_delta: timedelta = None
    ) -> str:
        """
        Create an access token with an optional expiration time.

        Args:
            subject (Union[str, Any]): The subject to encode into the token.
            expires_delta (timedelta, optional): Optional expiration time for the token.
                If not provided, the default expiration from settings is used.

        Returns:
            str: The encoded access token as a string.
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = {"exp": expire, "sub": json.dumps(subject)}
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=self._ALGORITHM
        )

        return encoded_jwt


    def decode_access_token(self, access_token: str) -> Any:
        """
        Decode an access token and return the decoded data.

        Args:
            access_token (str): The access token to decode.

        Returns:
            Any: The decoded token data as a dictionary.

        Raises:
            ValueError: If the access token has expired or is invalid.
        """
        try:
            decoded_token = jwt.decode(
                access_token,
                settings.SECRET_KEY,
                algorithms=[self._ALGORITHM]
            )
            return decoded_token
        except ExpiredSignatureError:
            raise ValueError("Access token has expired.")
        except InvalidTokenError as err:
            raise ValueError("Invalid access token.")
        except PyJWTError as err:
            raise ValueError("The signature does not match.")
