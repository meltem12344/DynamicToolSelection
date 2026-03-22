from typing import List
from sentence_transformers import CrossEncoder
from app.tools.tool_registry import ToolRegistry
from app.schemas.tool_schema import ToolSchema


class AdvancedToolSearcher:
    """
    1. Semantic retrieval ile aday araçları getirir
    2. Cross-Encoder ile yeniden sıralar
    3. Relative confidence kontrolü ile final adayları döndürür
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        print("[Sistem] Cross-Encoder Re-Ranker Modeli yükleniyor... (~90 MB)")
        self.cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def search(self, query: str, top_k: int = 2) -> List[ToolSchema]:
        print(f"\n[Hybrid Search] '{query}' için Semantic + Cross-Encoder taraması başlatıldı...")

        results = self.registry.collection.query(
            query_texts=[query],
            n_results=10
        )

        candidate_tool_names = results["ids"][0]
        candidate_documents = results["documents"][0]

        if not candidate_tool_names:
            print("[Search] Hiç aday araç bulunamadı.")
            return []

        cross_inp = [[query, doc] for doc in candidate_documents]
        cross_scores = self.cross_encoder.predict(cross_inp)

        scored_tools = []
        for i in range(len(candidate_tool_names)):
            scored_tools.append((
                float(cross_scores[i]),
                candidate_tool_names[i]
            ))

        scored_tools.sort(key=lambda x: x[0], reverse=True)

        print("\n[Cross-Encoder Değerlendirmesi]")
        for score, name in scored_tools:
            print(f"  -> Aday: {name} | CE Skoru: {score:.3f}")

        # En iyi aday yoksa çık
        if not scored_tools:
            return []

        best_score, best_name = scored_tools[0]
        second_score = scored_tools[1][0] if len(scored_tools) > 1 else -999.0

        score_gap = best_score - second_score

        print(f"\n[Decision Layer]")
        print(f"  -> En iyi aday: {best_name} | Skor: {best_score:.3f}")
        print(f"  -> İkinci aday skoru: {second_score:.3f}")
        print(f"  -> Skor farkı: {score_gap:.3f}")

        # İlk aşamada yumuşak bir relative threshold
        # İstersen bunu 0.8 / 1.0 / 1.5 diye deneyebilirsin
        min_gap = 0.80

        if score_gap < min_gap:
            print("[Decision Layer] Adaylar birbirine çok yakın. Güven düşük, araç seçilmedi.")
            return []

        if best_score < 0:
            print("[Decision Layer] Hiçbir tool yeterince iyi değil.")
            return []

        final_schemas = []
        best_score, best_name = scored_tools[0]

        print(f"\n[Final Selection]")
        print(f"  -> Seçilen tool: {best_name} | Skor: {best_score:.3f}")

        tool_obj = self.registry.get_tool(best_name)

        return [tool_obj.schema]