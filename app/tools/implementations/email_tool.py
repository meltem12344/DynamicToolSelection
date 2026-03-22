from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class EmailTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="send_email",
            description="Belirtilen alıcıya konu ve içerik bilgisiyle e-posta gönderir.",
            parameters={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Alıcı e-posta adresi"},
                    "subject": {"type": "string", "description": "E-posta konusu"},
                    "body": {"type": "string", "description": "E-posta içeriği"}
                },
                "required": ["to", "subject", "body"]
            },
            metadata=ToolMetadata(
                category="email_service",
                keywords=[
                    "mail", "email", "eposta", "gönder", "send email",
                    "mesaj", "subject", "body"
                ],
                risk_level="high"
            ),
            capabilities=[
                "e-posta gönderme",
                "konu ve içerik ile mesaj iletme",
                "alıcıya ileti gönderme"
            ],
            examples_tr=[
                "Ali'ye mail gönder.",
                "Bu metni e-posta olarak yolla.",
                "Şu konu ile mail oluştur ve gönder."
            ],
            examples_en=[
                "Send an email to Ali.",
                "Email this message.",
                "Send a mail with this subject and body."
            ],
            negative_examples=[
                "İstanbul'da hava nasıl?",
                "100 doları TL'ye çevir",
                "145 ile 25'i çarp"
            ],
            tags=["email", "messaging", "communication"]
        )

    def execute(self, **kwargs) -> Any:
        to = kwargs.get("to", "")
        subject = kwargs.get("subject", "")
        body = kwargs.get("body", "")
        return f"[Email]: '{subject}' konulu e-posta {to} adresine gönderildi (Simülasyon)."