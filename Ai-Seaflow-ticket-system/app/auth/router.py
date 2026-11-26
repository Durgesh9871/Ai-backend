from fastapi import APIRouter, status , HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.schemas import RegisterRequest, UserResponse,TokenResponse
from app.auth.service import register_user,authenticate_user
from app.core.security import create_access_token



router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload:RegisterRequest):
    return register_user(payload)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)    