import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vanna_setup import get_agent
from vanna.core.user import RequestContext

# 1. Initialize FastAPI
app = FastAPI(title="Clinic AI Assistant")
agent = get_agent()

# 2. Request Model
class ChatRequest(BaseModel):
    question: str

# 3. Step 7: Security Validation Logic
def is_sql_safe(sql: str) -> bool:
    if not sql:
        return False
    sql_upper = sql.upper().strip()
    # List of keywords that could modify data
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "EXEC"]
    # Ensure it's a SELECT statement and contains no forbidden words
    return sql_upper.startswith("SELECT") and not any(k in sql_upper for k in forbidden)

# 4. The Chat Endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        context = RequestContext(user_id="admin", tenant_id="default")
        
        generated_sql = None
        final_answer_data = None

        async for chunk in agent.send_message(context, request.question):
            # 1. Capture the SQL if it exists in this chunk
            if hasattr(chunk, 'sql') and chunk.sql:
                generated_sql = chunk.sql
            
            # 2. Capture the Data/Text
            # Check for the 'data' attribute (for tables)
            if hasattr(chunk, 'data') and chunk.data:
                final_answer_data = chunk.data
            # Check for 'text' attribute (common in SimpleTextComponent)
            elif hasattr(chunk, 'text') and chunk.text:
                final_answer_data = chunk.text
            # Check for 'simple_component' as a backup
            elif hasattr(chunk, 'simple_component') and chunk.simple_component:
                comp = chunk.simple_component
                # If it's an object, check its attributes; if it's a dict, use .get()
                final_answer_data = getattr(comp, 'data', None) or comp.get('data') if isinstance(comp, dict) else None

        # Step 7: Security Check
        if generated_sql and not is_sql_safe(generated_sql):
            return {"status": "error", "message": "Security: Unsafe SQL blocked."}

        return {
            "status": "success",
            "question": request.question,
            "sql": generated_sql,
            "answer": final_answer_data if final_answer_data else "No data found."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Agent Error: {str(e)}")

# 5. Health Check
@app.get("/health")
async def health():
    return {"status": "active", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)