from abc import ABC, abstractmethod
from typing import Any, Dict
from app.schemas.tool_schema import ToolSchema


class BaseTool(ABC):
    """
    Sistemdeki tüm araçların türetileceği temel (Base) sınıf.
    """

    @property
    @abstractmethod
    def schema(self) -> ToolSchema:
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

    def get_tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.schema.name,
                "description": self.schema.description,
                "parameters": self.schema.parameters
            }
        }

    def get_search_document(self) -> str:
        schema = self.schema

        parts = [
            f"Tool Name: {schema.name}",
            f"Description: {schema.description}",
            f"Category: {schema.metadata.category}",
        ]

        if schema.metadata.keywords:
            parts.append("Keywords:")
            parts.append(", ".join(schema.metadata.keywords))

        if schema.capabilities:
            parts.append("Capabilities:")
            parts.extend([f"- {item}" for item in schema.capabilities])

        if schema.examples_tr:
            parts.append("Turkish Examples:")
            parts.extend([f"- {item}" for item in schema.examples_tr])

        if schema.examples_en:
            parts.append("English Examples:")
            parts.extend([f"- {item}" for item in schema.examples_en])

        if schema.negative_examples:
            parts.append("Not Suitable For:")
            parts.extend([f"- {item}" for item in schema.negative_examples])

        if schema.tags:
            parts.append("Tags:")
            parts.append(", ".join(schema.tags))

        return "\n".join(parts).strip()