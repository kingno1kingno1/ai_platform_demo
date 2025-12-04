
from typing import Any, Dict

from .base import BaseAgent


class ToolAgent(BaseAgent):
    """示範用 Tool Agent。

    真實場景會呼叫外部 API（例如匯率、天氣、內部系統）。
    這裡先做一個簡單的假工具，回傳一些固定資訊。
    """

    def __init__(self):
        super().__init__(name="tool_agent")

    async def run(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        tool_result = {
            "demo_tool_info": "這是示範用 tool 回傳的資訊，可以想像成是系統狀態或外部 API 的結果。",
        }
        return tool_result
