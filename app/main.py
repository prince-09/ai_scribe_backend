from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints.upload import router as upload_router
from api.endpoints.transcription import router as trasncript_router
# from database.mongo import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="AI Scribe API",
    description="An API for processing audio files to generate transcripts and SOAP notes.",
    version="1.0.0",
)

# CORS Configuration: Allow frontend requests from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains; you can specify your frontend domain here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Add Routers
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(trasncript_router, prefix="/api", tags=["Save Transcript"])

# # Lifecycle Events
# @app.on_event("startup")
# async def startup_event():
#     """
#     Actions to perform at application startup.
#     """
#     await connect_to_mongo()


# @app.on_event("shutdown")
# async def shutdown_event():
#     """
#     Actions to perform at application shutdown.
#     """
#     await close_mongo_connection()

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "AI Scribe API is running."}
