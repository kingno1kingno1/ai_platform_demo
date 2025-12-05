
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


# AI 平台 Demo 架構說明

## 專案目標

這個專案是一個縮小版的 AI 平台雛形，用來展示：

- 使用 **Python + FastAPI** 建立一個可擴充的 AI 服務。
- 設計 **Multi-Agent Orchestration**（Research / Reasoning / Tool Agent）。
- 使用 **RAG（Retrieval-Augmented Generation）** 提升回覆品質。
- 將模型跑在本機 **GPU（Nvidia 1060）** 或 CPU 上，示範推理服務封裝方式。
- 暴露 **Prometheus 指標**，作為未來接到 Kubernetes + 監控系統的基礎。

雖然這個 demo 只有單機，但架構概念可以自然延伸到：

- 多服務（不同任務的模型 / Agent）
- 多 GPU / 多節點
- Kubernetes 部署與自動擴縮
- 更完整的 SLO / 效能優化工作

---

## 整體架構概覽

整體可以拆成四層：

1. **API 層（FastAPI）**
2. **Agent Orchestration 層**
3. **RAG / 資料層**
4. **模型推理層＋監控**

請求從 `/chat` 進來時，流程大致如下：

1. FastAPI 接收到使用者的 `query`。
2. Orchestrator 依序呼叫：
   - ResearchAgent：做 RAG 文件檢索。
   - ToolAgent：呼叫外部工具（Demo 版是簡單的假工具）。
   - ReasoningAgent：把 query + 檢索到的內容 + 工具結果 丟給 LLM 整合回答。
3. 回傳 JSON，並且在過程中更新 Prometheus 的 QPS / Latency 指標。

---

## 模組拆解

### 1. API 層（`app/main.py`）

- 使用 FastAPI 建立三個主要 endpoint：
  - `GET /health`：健康檢查。
  - `POST /chat`：主要聊天與推理入口。
  - `GET /metrics`：Prometheus 使用的 metrics endpoint。
- `/chat` 會：
  - 記錄請求開始時間。
  - 呼叫 Orchestrator 執行 multi-agent pipeline。
  - 計算總延遲並更新 Prometheus histogram。

這一層在未來 Kubernetes 化時，可以直接包成 container，透過 Service 對外提供 gRPC / HTTP。

---

### 2. Multi-Agent Orchestration（`app/agents/`）

目前設計了三種 Agent：

1. **ResearchAgent**
   - 負責「查資料」：根據使用者 query 到向量索引中取出相關文件。
   - 回傳 `retrieved_docs`，供後續 Agent 使用。
2. **ToolAgent**
   - Demo 版是簡單的假工具，可以想像成：
     - 查詢系統狀態
     - 呼叫內部 microservice 或外部 API
   - 回傳 `demo_tool_info` 等工具結果。
3. **ReasoningAgent**
   - 負責「整合」：
     - 將使用者 query、ResearchAgent 檢索到的文件、ToolAgent 回傳的資訊組成 prompt。
     - 丟給本地 LLM（LocalLLM）產生最後回答。

Orchestrator（`orchestrator.py`）負責決定：

1. Agent 呼叫順序。
2. context 如何在 Agent 之間傳遞。
3. 最後將所有中間結果與回答整合回傳。

> 未來若要接 Anthropic MCP 或更完整的多 Agent 平台，只要把現在這個 Orchestrator 抽象化成「Agent Graph / Workflow」，並把 ToolAgent 改成符合 MCP 的 tool spec，即可往更正式的平台演進。

---

### 3. RAG 與向量索引（`app/rag/`）

RAG 架構主要包含三個部分：

1. **Embedder（`embedder.py`）**
   - 使用 `sentence-transformers` 模型（預設 `all-MiniLM-L6-v2`）。
   - 自動偵測 `cuda` or `cpu`。
   - 將文字轉成向量，用於相似度搜尋。

2. **VectorStore（`vector_store.py`）**
   - 使用 FAISS 做向量索引，採用 L2 距離。
   - 支援：
     - `build_index(texts)`：建立索引。
     - `search(query, top_k)`：輸入一段文字 query，回傳最相關的文件。
   - 未來可以替換成 Milvus / pgvector / Redis Vector 等分散式方案。

3. **文件載入（`loader.py`）**
   - 從 `data/sample_docs` 載入 `.txt` / `.md` 檔案內容。
   - 若沒檔案，則提供預設說明文字，方便 Demo。
   - 實務上可以換成：
     - 資料庫內容
     - 產品文件 / FAQ
     - 監控報告等內部知識庫

RAG 在這個專案的角色是：

> 「把非結構化文件轉成語意向量，讓 LLM 回答時有更精準的上下文，而不是完全憑模型記憶。」

---

### 4. 模型推理與 GPU 使用（`app/models/local_llm.py`）

LocalLLM 的目標是：

- 封裝一個「可以在單張 1060 上運行的小型 LLM」。
- 提供簡單的 `generate(prompt)` 介面，方便 Agent 使用。

設計重點：

1. **裝置選擇**
   - 若 `settings.USE_GPU = True` 且 `torch.cuda.is_available()`：
     - 使用 `cuda`，並盡量用 `float16` 減少顯存。
   - 否則使用 CPU。
2. **錯誤處理**
   - 若模型下載或載入失敗：
     - 標記為 fallback，回傳一個簡單文字說明，而不是讓整個系統掛掉。
3. **未來擴展**
   - 可以替換成：
     - 量化後的模型（Int8 / Int4）
     - vLLM / TensorRT-LLM / Triton 等更高效的 Serving Engine。
   - 也可以改成 remote LLM（例如內網推理服務或雲端 API）。

---

### 5. 監控與效能指標（`app/monitoring/metrics.py`）

目前定義了兩個基礎指標：

1. `chat_requests_total`（Counter）
   - /chat 被呼叫的總次數。
2. `chat_request_latency_seconds`（Histogram）
   - /chat 的延遲分佈（含多個 bucket）。

這些指標會透過 `/metrics` 暴露，未來可以由 Prometheus 抓取，並用 Grafana 畫出：

- QPS
- P50 / P95 / P99 latency
- 錯誤率（可再補 Counter）

結合 Kubernetes 之後，可以根據這些指標：

- 設定 HPA 自動擴縮。
- 定義 SLO：例如「p95 latency < 1s」。

---

## 未來擴展方向

這個 demo 雖然是單機版本，但設計時已經考慮未來幾個方向：

1. **多服務與多模型**
   - 為不同任務（chat / embedding / rerank）拆成不同 service。
2. **Kubernetes 部署與 GPU 管理**
   - 為每個服務設定：
     - requests/limits
     - GPU 資源（`nvidia.com/gpu`）
     - HPA / VPA。
3. **向量資料庫升級**
   - 將 FAISS 改成 Milvus / pgvector / Redis Vector，支援更大量資料與多副本。
4. **MCP / 多 Agent 平台**
   - 以目前 Orchestrator 為基礎，向 Anthropic MCP 等協定靠攏，統一工具與 Agent 的接入模式。
5. **效能優化**
   - 模型壓縮（Quantization / Pruning / Distillation）。
   - 更高效的 Serving Engine（vLLM / TensorRT-LLM / Triton）。
   - 更完整的 benchmark 與 SLO 設計。

這些方向會讓這個 demo 從「單機練習專案」自然成長為「生產級 AI 平台」的雛型。
