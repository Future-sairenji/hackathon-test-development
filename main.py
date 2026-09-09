import os
from fastapi import FastAPI, Query
import google.generativeai as genai

app = FastAPI()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.get("/")
def read_root(prompt: str = Query("ハッカソンに向けて一言応援メッセージを頂戴！")):
    if not api_key:
        return {"error": "GEMINI_API_KEY が設定されていません。"}
    
    # 1. まずアカウントで利用可能なモデル一覧を自動取得する
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # 'models/gemini-pro' から 'models/' を除去した純粋な名前も保持
                available_models.append(m.name)
    except Exception as e:
        return {"error_list_models": str(e)}

    # 2. 利用可能なモデルの中から呼び出しを試行
    # 候補リスト：gemini-1.5-flash-8b, gemini-1.5-pro, gemini-pro など
    target_model = None
    for m_name in available_models:
        if "flash" in m_name or "pro" in m_name:
            target_model = m_name
            break
            
    if not target_model and available_models:
        target_model = available_models[0]

    if not target_model:
        return {
            "error": "利用可能なモデルが見つかりませんでした。",
            "available_models": available_models
        }

    try:
        model = genai.GenerativeModel(target_model)
        response = model.generate_content(prompt)
        return {
            "used_model": target_model,
            "available_models_count": len(available_models),
            "prompt": prompt,
            "response": response.text
        }
    except Exception as e:
        return {
            "attempted_model": target_model,
            "available_models": available_models,
            "error": str(e)
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)