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
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return {
            "prompt": prompt,
            "response": response.text
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)