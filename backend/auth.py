from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
import jwt
from pydantic import BaseModel
from pwdlib import PasswordHash

# --- CONFIGURATION ---
SECRET_KEY = "super-secret-passphrase-keep-this-private"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


db ={}

class UserRegister(BaseModel):
    username: str
    password: str

def make_token(username: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expiration_time
    }
    # Sign the token using our SECRET_KEY
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register", status_code=status.HTTP_201_CREATED)
def registration(user: UserRegister):
    if user.username in db:
        raise HTTPException(status_code=400, detail="Username taken!")
    scrambled_password = password_hasher.hash(user.password)
    db[user.username] = scrambled_password
    print(f"Stored user {user.username} with hash password {user.password}")

    return {"message":f"User {user.username} registered successfully"}

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username not in db:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    stored_hash = db[form_data.username]
    if not password_hasher.verify(form_data.password,stored_hash):
        raise HTTPException(status_code=400,detail="Invalid username or password")
    token_string = make_token(form_data.username)
    return {"access_token":token_string,"token_type":"bearer"}

# A reusable function that checks if the incoming token is valid
def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    unauthorized_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using the SAME secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in db:
            raise unauthorized_error
        return username
    except jwt.PyJWTError:
        raise unauthorized_error

# --- PROTECTED ROUTE ---
@app.get("/secret-dashboard")
def secret_dashboard(current_user: Annotated[str, Depends(verify_token)]):
    return {"message": f"Welcome to the VIP room, {current_user}!"}