from typing import Any
from app.tools.base_tool import BaseTool
from app.schemas.tool_schema import ToolSchema, ToolMetadata


class DatabaseTool(BaseTool):
    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name="query_sql_database",
            description=(
                "Şirket verisi, kullanıcı kayıtları, müşteri bilgileri, siparişler, "
                "satış verileri ve veritabanındaki kayıtları sorgulamak için kullanılır. "
                "Kullanıcı bir kişinin kaç sipariş verdiğini, bir tabloda kaç kayıt olduğunu, "
                "müşteri veya sipariş verisinin getirilmesini istediğinde kullanılmalıdır."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Çalıştırılacak SQL sorgusu"
                    }
                },
                "required": ["query"]
            },
            metadata=ToolMetadata(
                category="database_service",
                keywords=[
                    "sql", "veritabanı", "database", "sorgu", "query",
                    "tablo", "select", "insert", "update", "delete",
                    "veri", "kayıt", "sipariş", "müşteri", "kullanıcı",
                    "orders", "customers", "users", "count", "rapor"
                ],
                risk_level="high"
            ),
            capabilities=[
                "sql sorgusu çalıştırma",
                "tablodan veri çekme",
                "veritabanı erişimi",
                "kayıt sayısı bulma",
                "sipariş sayısını hesaplama",
                "müşteri ve kullanıcı verisi sorgulama",
                "raporlama amaçlı veri alma"
            ],
            examples_tr=[
                "Kullanıcı tablosundan tüm kayıtları getir.",
                "Orders tablosunu sorgula.",
                "Şu SQL sorgusunu çalıştır.",
                "X kullanıcısının kaç sipariş verdiğini getir.",
                "Şirket verisinden sipariş sayısını öğrenmek istiyorum.",
                "Bir müşterinin toplam sipariş sayısını bul.",
                "Veritabanından kullanıcı bilgilerini çek.",
                "Sipariş tablosunda kaç kayıt var?"
            ],
            examples_en=[
                "Run this SQL query.",
                "Fetch all rows from the users table.",
                "Query the orders table.",
                "How many orders did user X make?",
                "Get the order count from the database.",
                "Fetch customer records from the database.",
                "Count how many rows are in the orders table."
            ],
            negative_examples=[
                "Bunu İngilizceye çevir",
                "Ankara'da hava nasıl?",
                "10 dakikalık timer kur",
                "Yarın 3'e toplantı ekle",
                "100 doları TL'ye çevir"
            ],
            tags=[
                "database",
                "sql",
                "data_query",
                "analytics",
                "reporting",
                "order_lookup",
                "user_data"
            ]
        )

    def execute(self, **kwargs) -> Any:
        query = kwargs.get("query", "")
        return f"[Database]: SQL sorgusu çalıştırıldı -> {query} (Simülasyon)."