from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class DocumentReaderTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="read_document_from_url",
            description="Verilen URL'deki belge veya metin içeriğini okuyup özetlemek ya da çıkarmak için kullanılır.",
            parameters={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Okunacak belge URL'si"}
                },
                "required": ["url"]
            },
            metadata=ToolMetadata(
                category="document_service",
                keywords=[
                    "doküman", "belge", "url", "oku", "read document",
                    "pdf", "web page", "content extract"
                ],
                risk_level="medium"
            ),
            capabilities=[
                "URL'den belge okuma",
                "içerik çıkarma",
                "doküman inceleme"
            ],
            examples_tr=[
                "Bu URL'deki belgeyi oku.",
                "Şu linkteki PDF'i analiz et.",
                "Bu dökümanın içeriğini çıkar."
            ],
            examples_en=[
                "Read the document from this URL.",
                "Analyze the PDF at this link.",
                "Extract the content from this page."
            ],
            negative_examples=[
                "145 ile 25'i çarp",
                "Doları TL'ye çevir",
                "Ankara'nın hava durumunu söyle"
            ],
            tags=["document_reader", "url_reader", "content_extractor"]
        )

    def execute(self, **kwargs) -> Any:
        url = kwargs.get("url", "")
        return f"[Document Reader]: {url} adresindeki içerik okundu (Simülasyon)."