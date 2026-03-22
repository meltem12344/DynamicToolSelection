from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class CalendarTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="manage_calendar",
            description=(
                "Kullanıcının takvimine etkinlik eklemek, toplantı planlamak, "
                "randevu oluşturmak veya mevcut takvim etkinliklerini görüntülemek için kullanılır. "
                "Sadece zaman, tarih ve planlama ile ilgili işlemlerde kullanılmalıdır."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "create, list, update gibi işlem türü"},
                    "title": {"type": "string", "description": "Etkinlik başlığı"},
                    "datetime": {"type": "string", "description": "Etkinlik tarihi ve saati"}
                },
                "required": ["action"]
            },
            metadata=ToolMetadata(
                category="calendar_service",
                keywords=[
                    "takvim", "etkinlik", "randevu", "toplantı",
                    "calendar", "meeting", "schedule", "event",
                    "planla", "planlama", "hatırlatıcı"
                ],
                risk_level="medium"
            ),
            capabilities=[
                "takvim etkinliği oluşturma",
                "toplantı planlama",
                "randevu oluşturma",
                "takvimdeki etkinlikleri listeleme",
                "zaman bazlı planlama yapma"
            ],
            examples_tr=[
                "Yarın 3'e toplantı ekle.",
                "Takvimimde bugün ne var?",
                "Cuma 10:00'a etkinlik oluştur.",
                "Pazartesi için randevu ayarla.",
                "Saat 5 için toplantı planla."
            ],
            examples_en=[
                "Add a meeting for tomorrow at 3 PM.",
                "What is on my calendar today?",
                "Create an event for Friday at 10.",
                "Schedule a meeting for Monday.",
                "Set an appointment at 5 PM."
            ],
            negative_examples=[
                "100 doları TL'ye çevir",
                "İngilizceye çevir",
                "Ankara'da hava nasıl?",
                "145 ile 25'i çarp",
                "şirket verisinden sipariş sayısını getir",
                "veritabanından kullanıcı bilgisi çek",
                "SQL sorgusu çalıştır"
            ],
            tags=["calendar", "event_manager", "schedule", "time_management"]
        )

    def execute(self, **kwargs) -> Any:
        action = kwargs.get("action", "list")
        title = kwargs.get("title", "İsimsiz Etkinlik")
        dt = kwargs.get("datetime", "belirtilmedi")
        return f"[Takvim]: action={action}, title={title}, datetime={dt}"