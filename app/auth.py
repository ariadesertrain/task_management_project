"""
JWT Authentication Utilities - FIPS Compliant
Uses RS256 (RSA with SHA-256) for JWT tokens.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from jwt.exceptions import InvalidTokenError
from app.config import settings


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


def create_access_token(
    data: Dict[str, Any], #Dict is a dictionary of user information. Usually includes "sub" (subject/user email) claim with user identifier, and can include other claims like "role", "permissions", etc.
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token using RS256.
    
    Args:
        data: Dictionary of claims to include in token
        expires_delta: Token expiration time (default: 30 minutes)
    
    Returns:
        str: Encoded JWT token
    
    Example:
        token = create_access_token(
            data={"sub": "user@example.com", "role": "admin"}
        )
    """
    # Make a copy so we don't modify the original. We are going to modify the copy (add expiration,etc.) before encoding it into a JWT token.
    to_encode = data.copy()
    
    # Set expiration time. If custom expiration is provided, use it. Otherwise, default to 30 minutes from now.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    # Add standard JWT claims. It allows time-based validation and prevent token replay attacks.
    to_encode.update({
        "exp": expire,              # Expiration time
        "iat": datetime.now(timezone.utc),   # Issued at
        "nbf": datetime.now(timezone.utc)    # Not before
    })
    
    # Load private RSA key from file. Use PyJWT to encode the data. Sign in with RS256 algorithm. Returns a JWT string that can be sent to clients. Clients will use the corresponding public key to verify the token's authenticity and integrity when they send it back to the server for authentication/authorization.
    private_key = settings.get_private_key()
    encoded_jwt = jwt.encode(
        to_encode,
        private_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token using RS256.
    
    Args:
        token: JWT token string to verify
    
    Returns:
        Dict[str, Any]: Decoded token payload
    
    Raises:
        AuthenticationError: If token is invalid or expired
    
    Example:
        try:
            payload = verify_token(token)
            user_email = payload["sub"]
        except AuthenticationError as e:
            print(f"Auth failed: {e}")
    """
    try:
        # Load public RSA key. Decode and verify the token. Return the payload if valid. If the token is expired or invalid, it will raise an exception that we catch and re-raise as AuthenticationError with a user-friendly message.
        public_key = settings.get_public_key()
        payload = jwt.decode( #jwt.decode() automatically checks if the signature is valid, if token is expireD, if the token is not valid yet (nbf claim), and if the algorithm matches (RS256). If any of these checks fail, it raises an exception that we catch and handle.
            token,
            public_key,
            algorithms=[settings.algorithm]
        )
        return payload

    #Error handling for expired token and invalid token. We catch specific exceptions from PyJWT and raise our own AuthenticationError with a clear message that can be used in our API responses.    
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")