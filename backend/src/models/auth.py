"""Authentication-related Pydantic models."""

from pydantic import BaseModel, Field


class User(BaseModel):
    """User model for authentication."""

    user_id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email address")
    name: str = Field(..., description="User display name")
    picture: str | None = Field(None, description="User profile picture URL")
    provider: str = Field(..., description="OAuth provider (google, facebook)")


class Token(BaseModel):
    """JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class AuthResponse(BaseModel):
    """Authentication response with user and token."""

    user: User = Field(..., description="User information")
    token: Token = Field(..., description="JWT token")


class GoogleAuthRequest(BaseModel):
    """Google OAuth authentication request."""

    credential: str = Field(..., description="Google OAuth credential token")


class FacebookAuthRequest(BaseModel):
    """Facebook OAuth authentication request."""

    access_token: str = Field(..., description="Facebook access token")
    user_id: str = Field(..., description="Facebook user ID")
