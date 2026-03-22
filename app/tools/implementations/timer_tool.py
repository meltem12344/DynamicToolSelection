from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class TimerTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="set_timer",
            description="Belirli bir süre için zamanlayıcı veya alarm kurar.",
            parameters={
                "type": "object",
                "properties": {
                    "duration": {"type": "string", "description": "Süre bilgisi, örn: 10 dakika"},
                    "label": {"type": "string", "description": "İsteğe bağlı etiket"}
                },
                "required": ["duration"]
            },
            metadata=ToolMetadata(
                category="timer_service",
                keywords=[
                    "zamanlayıcı", "alarm", "hatırlatıcı", "timer",
                    "set timer", "countdown", "süre"
                ],
                risk_level="low"
            ),
            capabilities=[
                "zamanlayıcı kurma",
                "alarm başlatma",
                "süre bazlı hatırlatma"
            ],
            examples_tr=[
                "10 dakikalık timer kur.",
                "Yarım saat sonra beni uyar.",
                "5 dakika için zamanlayıcı başlat."
            ],
            examples_en=[
                "Set a timer for 10 minutes.",
                "Remind me in 30 minutes.",
                "Start a 5-minute countdown."
            ],
            negative_examples=[
                "Yarın takvime toplantı ekle",
                "145 ile 25'i çarp",
                "Bunu İngilizceye çevir"
            ],
            tags=["timer", "alarm", "countdown"]
        )

    def execute(self, **kwargs) -> Any:
        duration = kwargs.get("duration", "belirtilmedi")
        label = kwargs.get("label", "")
        return f"[Timer]: {duration} süreli zamanlayıcı kuruldu. {label}"