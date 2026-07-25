from typing import Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "app error"
    message: str = "Bad request"

    def __init__(self, message: Optional[str] = None, error_code: Optional[str] = None):
        self.message = message or self.message
        self.error_code = error_code or self.error_code
        super().__init__(self.message)

    
class UserAlreadyExistsException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "user already exists"
    message = "User with this email or phone number already exists"


class UserNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "user not found"
    message = "User not found"


class InvalidCredentialsException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "invalid credentials"
    message = "Invalid credentials"


class CredentialsException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "credentials error"
    message = "Credentials error"


class InactiveAccountException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "inactive account"
    message = "Account is inactive"


class UnverifiedUserException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "unverified user"
    message = "User is not verified"


class SellerAccessRequiredException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "seller access required"
    message = "Seller access required"


class AdminAccessRequiredException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "admin access required"
    message = "Admin access required"


class InvalidOtpException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "invalid otp"
    message = "Invalid OTP"


class OtpExpiredException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "otp expired"
    message = "OTP has expired"


class OtpMaxAttemptsExceededException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "otp max attempts exceeded"
    message = "OTP has exceeded maximum attempts"


class OtpCooldownException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "otp resend cooldown"
    message = "OTP resend cooldown exceeded"


class OtpAlreadyUsedException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "otp already used"
    message = "OTP has already been used"


class InvalidRefreshTokenException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "invalid refresh token"
    message = "Invalid refresh token"


def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
            },
        )

    
