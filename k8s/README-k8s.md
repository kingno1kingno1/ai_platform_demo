# Kubernetes 部署說明（AI Platform Demo）

## 檔案一覽

- `deployment-cpu.yaml`：CPU 版本 Deployment。
- `deployment-gpu.yaml`：GPU 版本 Deployment，示範 `nvidia.com/gpu` 與 `nodeSelector`。
- `service.yaml`：ClusterIP Service，暴露 HTTP 介面。
- `hpa.yaml`：CPU-based HPA，自動擴縮。
- `servicemonitor.yaml`：Prometheus Operator 用的 ServiceMonitor，抓 `/metrics`。

## 基本部署流程

1. 建立並推送 image：

   ```bash
   docker build -t your-registry/ai-platform-demo:latest .
   docker push your-registry/ai-platform-demo:latest
   ```

2. CPU 版本：

   ```bash
   kubectl apply -f k8s/deployment-cpu.yaml
   kubectl apply -f k8s/service.yaml
   ```

3. GPU 版本（有 GPU node 時）：

   ```bash
   kubectl delete deployment ai-platform-demo || true
   kubectl apply -f k8s/deployment-gpu.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. 啟用 HPA：

   ```bash
   kubectl apply -f k8s/hpa.yaml
   ```

5. 若使用 Prometheus Operator：

   ```bash
   kubectl apply -f k8s/servicemonitor.yaml
   ```
