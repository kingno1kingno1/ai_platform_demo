
import pathlib
from typing import List


def load_sample_docs() -> List[str]:
    """載入 data/sample_docs 底下的所有 .txt / .md 檔案內容。"""
    root = pathlib.Path(__file__).resolve().parents[2]
    docs_dir = root / "data" / "sample_docs"
    texts: List[str] = []
    for path in docs_dir.glob("*"):
        if path.suffix.lower() not in {".txt", ".md"}:
            continue
        try:
            texts.append(path.read_text(encoding="utf-8"))
        except Exception:
            continue
    if not texts:
        texts = [
            "這是一個關於 AI 平台 demo 的範例文件。你可以在這裡放上你對系統設計、架構圖說明、或效能實驗的紀錄。",
            "這個系統展示了 multi-agent 協作、RAG 檢索、以及使用 GPU 的本地 LLM。",
        ]
    return texts
