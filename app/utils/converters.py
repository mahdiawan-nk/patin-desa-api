from typing import Type, TypeVar, List, Union
from beanie import Document
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def to_read_model(doc: Document, schema: Type[T]) -> T:
    """Konversi satu Document Beanie menjadi Pydantic schema dengan id sebagai str."""
    return schema(**doc.dict(exclude={"id"}), id=str(doc.id))

def to_read_model_list(docs: List[Document], schema: Type[T]) -> List[T]:
    """Konversi list Document Beanie menjadi list schema Pydantic."""
    return [to_read_model(doc, schema) for doc in docs]

def to_str_id(data: dict) -> dict:
    if "id" in data and not isinstance(data["id"], str):
        data["id"] = str(data["id"])
    return data