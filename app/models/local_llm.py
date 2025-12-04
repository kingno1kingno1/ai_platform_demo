
from typing import Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ..config import settings


class LocalLLM:
    """簡化版本地 LLM 封裝。

    - 預設載入一個小型開源模型，盡量適合在單張 1060 上跑。
    - 若模型載入失敗，會 fallback 成非常簡單的回應，避免整個系統掛掉。
    """

    def __init__(self, model_name: str = settings.MODEL_NAME):
        self.model_name = model_name
        self.device = (
            "cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu"
        )
        self.model: Optional[AutoModelForCausalLM] = None
        self.tokenizer = None

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
            )
            if self.device == "cpu":
                self.model.to(self.device)
        except Exception as e:
            print(f"[LocalLLM] 載入模型失敗，將使用 fallback：{e}")
            self.model = None
            self.tokenizer = None

    def generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        if self.model is None or self.tokenizer is None:
            # Fallback：避免因為模型下載問題讓 demo 不能跑
            return (
                "（本機模型尚未正確載入，這是 fallback 回應。）\n"
                f"你問的問題是：{prompt[:200]}..."
            )

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(
            self.device
        )
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
            )
        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        # 把輸入 prompt 切掉，只保留新生成的部分
        return output_text[len(prompt) :]
