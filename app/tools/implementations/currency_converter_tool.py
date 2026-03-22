from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class CurrencyConverterTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="convert_currency",
            description=(
                "Bir para birimindeki tutarı başka bir para birimine dönüştürür. "
                "Dolar, Euro, Türk Lirası ve diğer dövizler arasında kur çevirisi yapmak, "
                "bir miktarın başka para birimindeki karşılığını hesaplamak ve döviz kuru bazlı dönüşüm yapmak için kullanılır. "
                "Metin çevirisi için kullanılmaz; sadece finansal para birimi dönüşümü içindir."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Çevrilecek miktar"
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "Kaynak para birimi (Örn: USD, EUR, TRY, BTC)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Hedef para birimi (Örn: TRY, EUR, USD)"
                    }
                },
                "required": ["amount", "from_currency", "to_currency"]
            },
            metadata=ToolMetadata(
                category="finance_service",
                keywords=[
                    "döviz", "kur", "para birimi", "parite", "çevir", "dönüştür",
                    "dolar", "euro", "tl", "try", "usd", "eur", "bitcoin", "btc",
                    "exchange", "exchange rate", "currency", "convert currency"
                ],
                risk_level="low"
            ),
            capabilities=[
                "para birimi dönüştürme",
                "döviz kuru bazlı hesaplama",
                "usd try dönüşümü",
                "eur try dönüşümü",
                "tutarı başka para birimine çevirme",
                "kur üzerinden karşılık hesaplama"
            ],
            examples_tr=[
                "150 doları Türk Lirasına çevir.",
                "100 USD kaç TL eder?",
                "50 euroyu liraya dönüştür.",
                "200 TL'yi dolara çevir.",
                "1 bitcoin kaç dolar yapıyor?",
                "Doları TL'ye çevir.",
                "Euro kurunu kullanarak hesapla."
            ],
            examples_en=[
                "Convert 150 dollars to Turkish lira.",
                "How much is 100 USD in TRY?",
                "Convert 50 euros to lira.",
                "Convert 200 TRY to USD.",
                "How much is 1 BTC in USD?"
            ],
            negative_examples=[
                "Bunu İngilizceye çevir.",
                "Merhaba dünya cümlesini Almancaya aktar.",
                "Ankara'da hava kaç derece?",
                "Yarın saat 3'e toplantı ekle.",
                "Ahmet'e e-posta gönder.",
                "256 ile 48'i çarp."
            ],
            tags=[
                "currency",
                "exchange_rate",
                "finance",
                "money_conversion",
                "usd_try",
                "eur_try"
            ]
        )

    def execute(self, **kwargs) -> Any:
        amount = kwargs.get("amount", 0)
        from_c = kwargs.get("from_currency", "")
        to_c = kwargs.get("to_currency", "")
        return f"[Döviz Servisi]: {amount} {from_c} = {float(amount) * 34.5} {to_c} (Simüle edilmiş kur)"