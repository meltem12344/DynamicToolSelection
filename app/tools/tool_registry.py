import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
from app.tools.base_tool import BaseTool


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

        self.chroma_client = chromadb.Client()

        print("\n[Sistem] Çok Dilli Hafif Embedding Modeli yükleniyor... (~470 MB)")
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.collection = self.chroma_client.create_collection(
            name="agent_tools",
            embedding_function=self.emb_fn
        )

    def register(self, tool: BaseTool):
        schema = tool.schema
        self._tools[schema.name] = tool

        search_text = tool.get_search_document()

        self.collection.add(
            documents=[search_text],
            metadatas=[{
                "name": schema.name,
                "category": schema.metadata.category,
                "keywords": ",".join(schema.metadata.keywords),
                "risk_level": schema.metadata.risk_level
            }],
            ids=[schema.name]
        )

        print(f"[Vector Registry] '{schema.name}' aracı Vektör DB'ye gömüldü.")
        print(f"[Vector Registry] Embedded Text Preview:\n{search_text}\n")

    def get_tool(self, name: str) -> BaseTool:
        return self._tools.get(name)

    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())