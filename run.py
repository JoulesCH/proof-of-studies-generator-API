from core import app

if __name__ == "__main__":
    import uvicorn
    import os
    
    start = "run:app"
    uvicorn.run(
        start, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", default=8080)), 
        reload=True
        )