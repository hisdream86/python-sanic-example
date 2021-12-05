from pydantic import Field, BaseModel


class BaseResponse(BaseModel):
    code: int = Field(..., description="Result code")


class ErrorResponse(BaseModel):
    code: int = Field(..., description="Result code")
    error: str = Field("", description="Error message")
