from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class ToolMetadata(BaseModel):
    category: str = Field(
        description="Aracın ait olduğu genel kategori"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Arama ve filtreleme için anahtar kelimeler"
    )
    risk_level: Optional[str] = Field(
        default="low",
        description="Aracın risk seviyesi"
    )


class ToolSchema(BaseModel):
    name: str = Field(..., description="Aracın benzersiz adı")
    description: str = Field(..., description="LLM için kısa ve net açıklama")
    parameters: Dict[str, Any] = Field(..., description="Aracın parametre şeması")
    metadata: ToolMetadata = Field(..., description="Ek meta veriler")

    capabilities: List[str] = Field(
        default_factory=list,
        description="Aracın yapabildiği işler"
    )
    examples_tr: List[str] = Field(
        default_factory=list,
        description="Türkçe örnek kullanıcı istekleri"
    )
    examples_en: List[str] = Field(
        default_factory=list,
        description="İngilizce örnek kullanıcı istekleri"
    )
    negative_examples: List[str] = Field(
        default_factory=list,
        description="Bu araç için uygun olmayan örnek istekler"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Ek arama etiketleri"
    )