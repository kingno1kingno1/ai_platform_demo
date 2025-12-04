
from typing import Any, Dict, List

from .base import BaseAgent
from ..models.local_llm import LocalLLM


class ReasoningAgent(BaseAgent):
    def __init__(self, llm: LocalLLM):
        super().__init__(name="reasoning_agent")
        self.llm = llm

    async def run(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        retrieved_docs: List[str] = context.get("retrieved_docs", [])
        system_prompt = (
            "你是一個幫助使用者理解這個 AI 平台 demo 架構的助理。"
            "根據提供的文件內容與使用者問題，給出清楚、有結構的回答。"
        )

        context_block = "\n\n".join(
            [f"[Doc {i+1}] {t}" for i, t in enumerate(retrieved_docs)]
        )
        prompt = (
            f"{system_prompt}\n\n"
            f"文件內容：\n{context_block}\n\n"
            f"使用者問題：{query}\n"
        )

        answer = self.llm.generate(prompt)
        return {
            "answer": answer,
        }
