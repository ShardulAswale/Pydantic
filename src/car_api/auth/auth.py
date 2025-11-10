from typing import Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# In-memory user store
_USERS: Dict[str, str] = {
    "admin": "changeme",
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """Validate HTTP Basic credentials and return the username if valid."""
    correct_password = _USERS.get(credentials.username)
    if not correct_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Use constant-time compare for the password
    password_ok = secrets.compare_digest(credentials.password, correct_password)
    if not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
