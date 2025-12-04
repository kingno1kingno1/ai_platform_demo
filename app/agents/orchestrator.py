
from typing import Any, Dict

from .research_agent import ResearchAgent
from .reasoning_agent import ReasoningAgent
from .tool_agent import ToolAgent


class Orchestrator:
    """負責 orchestrate 多個 agent 的簡單管線。

    目前流程：
    1. ResearchAgent：根據 query 做 RAG 檢索。
    2. ToolAgent：取得一些工具資訊（示範用）。
    3. ReasoningAgent：根據 retrived docs + tools + query 產生最後回答。
    """

    def __init__(
        self,
        research_agent: ResearchAgent,
        reasoning_agent: ReasoningAgent,
        tool_agent: ToolAgent,
    ):
        self.research_agent = research_agent
        self.reasoning_agent = reasoning_agent
        self.tool_agent = tool_agent

    async def handle_query(self, query: str) -> Dict[str, Any]:
        context: Dict[str, Any] = {}

        research_output = await self.research_agent.run(query, context)
        context.update(research_output)

        tool_output = await self.tool_agent.run(query, context)
        context.update(tool_output)

        reasoning_output = await self.reasoning_agent.run(query, context)
        context.update(reasoning_output)

        return context
