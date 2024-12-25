from bson import ObjectId
from fastapi import HTTPException, APIRouter
from database.mongo import mongo_instance

router = APIRouter()

@router.post("/transcription")
async def update_transcription(id: str, soap_note: dict):
    """
    Update the transcription of a document by its ID.
    """
    try:
        # Convert the string ID to ObjectId
        object_id = ObjectId(id)
        
        # Validate transcription
        if not isinstance(soap_note, dict):
            raise HTTPException(status_code=400, detail="Invalid transcription format. Expected a dictionary.")

        # Update the document in the collection
        update_result = await mongo_instance.transcripts.update_one(
            {"_id": object_id},
            {"$set": {'soap_note': soap_note}}
        )

        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Document not found.")

        return {"message": "Transcription updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating transcription: {e}")