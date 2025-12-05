# 推理效能實驗報告範本（Inference Benchmark Report）

## 1. 實驗目的

（例）比較不同 quantization / 模型設定，在單張 1060 上的 latency / throughput / VRAM 使用。

## 2. 環境說明

- GPU：Nvidia GTX 1060 6GB
- CPU：
- RAM：
- OS：
- Python：
- PyTorch：
- CUDA / Driver：

## 3. 模型與設定

| 名稱 | 模型 | 精度 / 量化 | max_new_tokens | 備註 |
|------|------|-------------|----------------|------|
| M1   | TinyLlama 1.1B | FP16 | 256 | baseline |
| M2   | TinyLlama 1.1B | INT8 | 256 | 8-bit quant |
| M3   | ...            | INT4 | 256 | 4-bit quant |

## 4. 測試方法

- 壓測工具：自寫 script / locust / wrk / vegeta（擇一說明）。
- 測試場景：
  - prompt 長度：
  - 併發數（concurrency）：
  - 每組設定測試時間：
- 指標：QPS、p50/p95/p99 latency、VRAM 使用、GPU 利用率。

## 5. 實驗結果

### 5.1 Latency / QPS

| 模型設定 | Concurrency | p50 (ms) | p95 (ms) | p99 (ms) | QPS |
|----------|------------|----------|----------|----------|-----|
| M1       | 1          |          |          |          |     |
| M1       | 4          |          |          |          |     |
| M2       | 1          |          |          |          |     |
| M2       | 4          |          |          |          |     |

### 5.2 GPU / Memory

| 模型設定 | VRAM (GiB) | GPU 利用率 (%) | 備註 |
|----------|-----------|----------------|------|
| M1       |           |                |      |
| M2       |           |                |      |

## 6. 觀察與分析

- 哪個設定在延遲 / 吞吐量 / VRAM 之間最平衡？
- 什麼情況下延遲開始急遽上升？（例如 concurrency > 4）
- quantization 對品質是否有明顯影響？

## 7. 結論與未來優化

- 建議的預設配置：
- 未來可以嘗試：vLLM / TensorRT-LLM / Triton、更好的 batching 策略、與 Kubernetes HPA 整合。

