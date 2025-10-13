from fastapi.responses import JSONResponse
from typing import Any, Dict, List, Optional, Union
from datetime import datetime,date
from bson import ObjectId  # untuk MongoDB

def convert_value(value: Any) -> Any:
    """Konversi nilai ke tipe yang dapat di-JSON-kan."""
    if isinstance(value, (datetime, date)):  # Tangani datetime dan date
        return value.isoformat()
    if isinstance(value, ObjectId):
        return str(value)
    if hasattr(value, "dict"):  # Jika Pydantic model
        return sanitize_data(value.dict())
    if isinstance(value, list):  # Tangani list dalam value
        return [convert_value(v) for v in value]
    if isinstance(value, dict):  # Tangani dict nested
        return {k: convert_value(v) for k, v in value.items()}
    return value

# Fungsi untuk menghapus field sensitif dan konversi tipe
def sanitize_data(data: Union[Dict, List, Any], exclude: List[str] = ["password"]) -> Any:
    if isinstance(data, dict):
        return {k: convert_value(v) for k, v in data.items() if k not in exclude}
    elif isinstance(data, list):
        return [sanitize_data(item, exclude) for item in data]
    else:
        return convert_value(data)

def success_response(
    message: str = "Berhasil",
    data: Optional[Any] = None,
    status_code: int = 200,
    exclude: List[str] = ["password"]
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": sanitize_data(data, exclude)
        }
    )

def paginated_response(
    items: List[Any],
    total: int,
    page: int,
    per_page: int,
    message: str = "Berhasil mengambil data",
    exclude: List[str] = ["password"]
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "meta": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page
            },
            "data": sanitize_data(items, exclude)
        }
    )

def error_response(
    message: str = "Terjadi kesalahan",
    status_code: int = 400,
    errors: Optional[Any] = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "errors": errors
        }
    )
