import os
# 解決 macOS 上 PyTorch 和 Faiss 同時使用時的 OpenMP 衝突問題
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 強制先載入 PyTorch，這通常能解決與 Faiss 的 OpenMP 衝突 (Segfault)
import torch

import time
from fastapi import FastAPI
from pydantic import BaseModel

from .config import settings
from .agents.orchestrator import Orchestrator
from .agents.research_agent import ResearchAgent
from .agents.reasoning_agent import ReasoningAgent
from .agents.tool_agent import ToolAgent
from .rag.vector_store import VectorStore
from .rag.embedder import Embedder
from .rag.loader import load_sample_docs
from .models.local_llm import LocalLLM
from .monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY, metrics_app


class ChatRequest(BaseModel):
    query: str


app = FastAPI(title=settings.PROJECT_NAME)

# Mount /metrics for Prometheus
app.mount("/metrics", metrics_app)

# 初始化組件（簡化版，實務可用依賴注入/工廠模式）
embedder = Embedder(model_name=settings.EMBEDDING_MODEL_NAME)
vector_store = VectorStore(embedder=embedder)

# 載入示範文件
docs = load_sample_docs()
vector_store.build_index(docs)

llm = LocalLLM(model_name=settings.MODEL_NAME)

research_agent = ResearchAgent(vector_store=vector_store)
reasoning_agent = ReasoningAgent(llm=llm)
tool_agent = ToolAgent()
orchestrator = Orchestrator(
    research_agent=research_agent,
    reasoning_agent=reasoning_agent,
    tool_agent=tool_agent,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    start_time = time.time()
    REQUEST_COUNT.inc()
    result = await orchestrator.handle_query(req.query)
    elapsed = time.time() - start_time
    REQUEST_LATENCY.observe(elapsed)
    return {
        "query": req.query,
        "result": result,
        "latency_sec": elapsed,
    }
