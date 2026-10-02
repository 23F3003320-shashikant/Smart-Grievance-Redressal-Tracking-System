from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str
    password: str

class SendOTPRequest(BaseModel):
    phone : str = Field(
                ...,
                examples="+919876543210",
                description="E.164 phone format"
    )

class VerifyOTPRequest(BaseModel):
    phone : str = Field(
        ...,
        example="+919876543210"
    )
    otp : str = Field(
        ...,
        min_length=6,
        max_length=6,
        example="123456"
    )
    
class RefreshRequest(BaseModel):
    refresh_token : str

class AuthResponse(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str = "bearer"

class NewAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"