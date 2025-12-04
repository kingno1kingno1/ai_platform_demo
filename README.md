
# AI Platform Demo (FastAPI + Multi-Agent RAG)

這是一個為面試準備的示範專案，重點不是要做到超大規模，而是展示你對以下概念的理解：

- 使用 **Python + FastAPI** 打造一個簡單的 AI 服務。
- **Multi-Agent Orchestration**：Research Agent + Reasoning Agent + Tool Agent。
- **RAG 架構**：用向量搜尋做文件檢索。
- **GPU 使用**：使用 PyTorch + Transformers 在 GPU 上跑一個小模型（或嵌入模型）。
- **基本監控**：用 Prometheus metrics 暴露簡單的 QPS / latency 指標。

## 快速開始

### 1. 建立虛擬環境與安裝依賴

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 2. 啟動開發伺服器

```bash
uvicorn app.main:app --reload
```

伺服器預設跑在 `http://127.0.0.1:8000`，你可以打：

- `POST /chat`：主要入口，會走 multi-agent + RAG pipeline。
- `GET /health`：健康檢查。
- `GET /metrics`：Prometheus 指標。

### 3. 測試聊天 API

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "請問這個 demo 的架構設計重點是什麼？"}'
```

### 4. GPU 使用說明

- 專案裡的 `app/models/local_llm.py` 會偵測是否有 CUDA：
  - 有的話：將模型載入到 GPU（你的 1060）。
  - 沒有的話：fallback 到 CPU。
- 你可以用 `nvidia-smi` 確認推理時 GPU 有被使用。

> 實務上，你可以在 README 裡增加：
> - 你用哪一個模型（例如 TinyLlama、Qwen 0.5B 等）
> - 量化設定（例如 4-bit）
> - 不同設定下的 latency / throughput 測試結果

## 結構概覽

```text
ai_platform_demo/
├── app/
│   ├── main.py              # FastAPI 入口，串起整個 pipeline
│   ├── config.py            # 環境設定
│   ├── agents/              # Multi-Agent 實作
│   ├── rag/                 # RAG (embedding + vector store)
│   ├── models/              # LLM / embedding 模型封裝
│   └── monitoring/          # Prometheus metrics
├── data/
│   └── sample_docs/         # 示範用文件
├── tests/                   # 未來可以補測試
├── requirements.txt
└── README.md
```

你可以在面試時拿這個專案當作 talking point，說明：

- 你如何設計 agent 之間的協作流程。
- 你怎麼做 RAG 與向量檢索。
- 你怎麼讓模型跑在 GPU 上，以及未來怎麼擴展到多 GPU / Kubernetes。
- 你怎麼設計監控與效能指標。
