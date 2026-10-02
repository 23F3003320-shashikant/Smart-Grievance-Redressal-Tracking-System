from datetime import datetime, timedelta, timezone, secrets
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
import jwt
from pwdlib import PasswordHash
from Database.database import get_db
from schemas import SendOTPRequest,VerifyOTPRequest,RefreshRequest,AuthResponse,NewAccessTokenResponse

# --- CONFIGURATION ---
SECRET_KEY = "super-secret-passphrase-keep-this-private"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30
OTP_EXPIRE_MINUTES = 5

app = FastAPI()
security = HTTPBearer()

# --- MOCK STORAGE (Replace with DB / Redis in production) ---
users_db: set[str] = set()

# phone -> {"otp": "123456", "expires_at": datetime}
otp_store: dict[str, dict] = {}

# Active refresh tokens: token_string -> phone
active_refresh_tokens: dict[str, str] = {}

password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- TOKEN UTILITIES ---
def create_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    #Dependency that guards endpoints using the short-lived access token.
    token = credentials.credentials
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access token expired or invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise unauthorized

        phone: str | None = payload.get("sub")
        if phone is None or phone not in users_db:
            raise unauthorized
        return phone
    except jwt.PyJWTError:
        raise unauthorized


# --- ROUTES ---


@app.post("/send-otp")
def send_otp(request: SendOTPRequest) -> dict:
    phone = request.phone.strip()

    otp_code = str(secrets.randbelow(900000) + 100000)
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=OTP_EXPIRE_MINUTES
    )

    otp_store[phone] = {"otp": otp_code, "expires_at": expires_at}
    users_db.add(phone)

    # In production, integrate an SMS gateway (e.g., Twilio, Gupshup, Fast2SMS)
    print(f"\n[SMS GATEWAY] OTP for {phone}: {otp_code}\n")

    return {"message": "OTP sent successfully", "expires_in_minutes": OTP_EXPIRE_MINUTES}


@app.post("/verify-otp", response_model=AuthResponse)
def verify_otp(request: VerifyOTPRequest):
    phone = request.phone.strip()

    if phone not in otp_store:
        raise HTTPException(
            status_code=400, detail="No OTP requested for this phone number"
        )

    stored = otp_store[phone]

    if datetime.now(timezone.utc) > stored["expires_at"]:
        del otp_store[phone]
        raise HTTPException(status_code=400, detail="OTP has expired")

    if stored["otp"] != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    del otp_store[phone]

    access_token = create_token(
        data={"sub": phone, "type": "access"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = create_token(
        data={"sub": phone, "type": "refresh"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    # Track valid refresh tokens for revocation
    active_refresh_tokens[refresh_token] = phone

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh", response_model=NewAccessTokenResponse)
def refresh_access_token(request: RefreshRequest):

    #Called by the mobile app in the background when the access token expires.
  
    refresh_token = request.refresh_token

    if refresh_token not in active_refresh_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token. Please login again via OTP.",
        )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )
        phone = payload.get("sub")
    except jwt.PyJWTError:
        del active_refresh_tokens[refresh_token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please login again.",
        )

    new_access_token = create_token(
        data={"sub": phone, "type": "access"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


@app.post("/logout")
def logout(request: RefreshRequest):
    """Removes the refresh token so the user is forced to re-authenticate."""
    active_refresh_tokens.pop(request.refresh_token, None)
    return {"message": "Logged out successfully"}


# --- SENSITIVE DATA ROUTE ---
@app.get("/user/sensitive-profile")
def get_sensitive_profile(current_user: Annotated[str, Depends(get_current_user)]):
    return {
        "user_phone": current_user,
        "confidential_records": [
            {"id": 101, "status": "Confidential Grievance Active"}
        ],
    }