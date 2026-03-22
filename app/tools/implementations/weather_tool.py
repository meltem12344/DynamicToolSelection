from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class WeatherTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="get_weather",
            description="Belirli bir şehir veya konum için güncel hava durumu, sıcaklık ve temel tahmin bilgisini getirir.",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Hava durumu sorgulanacak konum"
                    }
                },
                "required": ["location"]
            },
            metadata=ToolMetadata(
                category="weather_service",
                keywords=[
                    "hava", "hava durumu", "sıcaklık", "derece", "yağmur",
                    "rüzgar", "forecast", "weather", "temperature"
                ],
                risk_level="low"
            ),
            capabilities=[
                "güncel hava durumu sorgulama",
                "sıcaklık bilgisi verme",
                "yağış durumu söyleme",
                "şehir bazlı hava bilgisi sağlama"
            ],
            examples_tr=[
                "Ankara'da bugün hava nasıl?",
                "İstanbul kaç derece?",
                "İzmir'de yağmur var mı?"
            ],
            examples_en=[
                "What is the weather in Ankara today?",
                "How hot is Istanbul?",
                "Will it rain in Izmir?"
            ],
            negative_examples=[
                "145 ile 25'i çarp",
                "Bunu İngilizceye çevir",
                "Yarın toplantı ekle"
            ],
            tags=["weather_api", "forecast", "temperature"]
        )

    def execute(self, **kwargs) -> Any:
        location = kwargs.get("location", "Bilinmeyen Konum")
        return f"[Hava Durumu]: {location} için hava 22°C, parçalı bulutlu."