from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.routes import router

app = FastAPI(title="Receipt Processor")

# Include the router
app.include_router(router)

# Add root endpoint that redirects to docs
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# For running the app directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)