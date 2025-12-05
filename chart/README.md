
# ai-platform-demo Helm Chart

這個 chart 用來部署 AI Platform Demo（FastAPI + Multi-Agent + RAG）到 Kubernetes。

## 使用方式

### 安裝（CPU 版本）

```bash
helm install ai-demo ./ai-platform-demo -n dev --create-namespace
```

### 安裝（GPU 版本）

先準備一份 `values-gpu.yaml`，覆寫：

```yaml
gpu:
  enabled: true
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
env:
  USE_GPU: "true"
resources:
  requests:
    cpu: "1"
    memory: "2Gi"
  limits:
    cpu: "2"
    memory: "4Gi"
```

然後：

```bash
helm install ai-demo-gpu ./ai-platform-demo -n prod -f values-gpu.yaml
```

### 升級

```bash
helm upgrade ai-demo ./ai-platform-demo -n dev
```
