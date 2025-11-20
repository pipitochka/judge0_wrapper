from fastapi.security import HTTPBearer

bearer_schema = HTTPBearer(
    scheme_name="JWT",
    bearerFormat="JWT"
)
