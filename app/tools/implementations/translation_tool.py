from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class TranslationTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="translate_text",
            description="Bir metni belirtilen hedef dile çevirir.",
            parameters={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Çevrilecek metin"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Hedef dil"
                    }
                },
                "required": ["text", "target_language"]
            },
            metadata=ToolMetadata(
                category="translation_service",
                keywords=[
                    "çevir", "çeviri", "ingilizceye çevir", "translate",
                    "translation", "dil", "language"
                ],
                risk_level="low"
            ),
            capabilities=[
                "metin çevirme",
                "çok dilli dönüşüm",
                "hedef dile göre çeviri yapma"
            ],
            examples_tr=[
                "Merhaba dünya kelimesini İngilizceye çevir.",
                "Bunu Almancaya çevir.",
                "Şu cümleyi Fransızcaya aktar."
            ],
            examples_en=[
                "Translate this to English.",
                "Convert this sentence into German.",
                "Translate the text into French."
            ],
            negative_examples=[
                "145 ile 25'i çarp",
                "İstanbul'da hava nasıl?",
                "Saat 5'e alarm kur"
            ],
            tags=["translation", "language_tool", "text_conversion"]
        )

    def execute(self, **kwargs) -> Any:
        text = kwargs.get("text", "")
        target_language = kwargs.get("target_language", "English")
        return f"[Çeviri Servisi]: '{text}' metni {target_language} diline çevrildi (Simülasyon)."