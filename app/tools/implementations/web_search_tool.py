from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class WebSearchTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="web_search",
            description="Genel web araması yaparak güncel veya genel bilgi bulur.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Arama sorgusu"}
                },
                "required": ["query"]
            },
            metadata=ToolMetadata(
                category="search_service",
                keywords=[
                    "web", "arama", "internette ara", "search", "google",
                    "güncel bilgi", "latest"
                ],
                risk_level="low"
            ),
            capabilities=[
                "web'de arama yapma",
                "güncel bilgi bulma",
                "genel bilgi araştırma"
            ],
            examples_tr=[
                "İnternette bunu ara.",
                "Bugünkü haberleri bul.",
                "Şu konu hakkında web'de araştırma yap."
            ],
            examples_en=[
                "Search the web for this.",
                "Find the latest news about this topic.",
                "Look this up online."
            ],
            negative_examples=[
                "145 ile 25'i çarp",
                "Bunu İngilizceye çevir",
                "10 dakikalık timer kur"
            ],
            tags=["web_search", "online_lookup", "internet_search"]
        )

    def execute(self, **kwargs) -> Any:
        query = kwargs.get("query", "")
        return f"[Web Search]: '{query}' için arama sonuçları getirildi (Simülasyon)."