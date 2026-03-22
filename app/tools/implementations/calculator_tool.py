from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class CalculatorTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="execute_math",
            description="Toplama, çıkarma, çarpma, bölme, yüzde hesabı ve temel matematik işlemleri yapar.",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Hesaplanacak matematik ifadesi"
                    }
                },
                "required": ["expression"]
            },
            metadata=ToolMetadata(
                category="math_service",
                keywords=[
                    "hesapla", "matematik", "çarp", "böl", "topla", "çıkar",
                    "calculate", "multiply", "divide", "sum"
                ],
                risk_level="low"
            ),
            capabilities=[
                "aritmetik işlem yapma",
                "çarpma ve bölme",
                "yüzde hesabı",
                "basit matematik çözümü"
            ],
            examples_tr=[
                "145 ile 25'i çarpar mısın?",
                "100'ün yüzde 20'si kaç?",
                "81'i 9'a böl"
            ],
            examples_en=[
                "Multiply 145 by 25",
                "What is 20 percent of 100?",
                "Divide 81 by 9"
            ],
            negative_examples=[
                "Ankara'da hava nasıl?",
                "Bunu İngilizceye çevir",
                "Bana mail gönder"
            ],
            tags=["calculator", "math", "arithmetic"]
        )

    def execute(self, **kwargs) -> Any:
        expression = kwargs.get("expression", "")
        try:
            result = eval(expression, {"__builtins__": {}})
            return f"[Hesap Sonucu]: {result}"
        except Exception:
            return "[Hesap Sonucu]: İşlem çözümlenemedi."