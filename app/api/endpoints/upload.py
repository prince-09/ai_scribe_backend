from fastapi import APIRouter, File, UploadFile, HTTPException
from services.audio_processing import process_audio
from services.soap_generation import generate_soap
from database.mongo import mongo_instance
# from app.services.database import save_transcript, save_soap_note

import os
from datetime import datetime

router = APIRouter()

async def save_transcript(transcript: dict, soap_note: dict):
    """
    Save the transcript and SOAP note to MongoDB.
    """
    # collection = database.get_collection("transcripts")
    document = {"transcript": transcript, "soap_note": soap_note}
    result = await mongo_instance.transcripts.insert_one(document)
    print("Resu--", (result.inserted_id))
    return str(result.inserted_id)


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload an audio file, process it for transcription and SOAP generation,
    and return the results.
    """
    try:
        # Save the uploaded file locally
        print("prince")
        file_path = f"temp_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        # Process the audio for transcription and diarization
        transcription = await process_audio(file_path)
        if not transcription:
            raise HTTPException(status_code=400, detail="Failed to process audio file.")
        
        # Generate SOAP Note
        soap_note = generate_soap(transcription)
        if not soap_note:
            raise HTTPException(status_code=400, detail="Failed to generate SOAP note.")

        transcription_id = await save_transcript(transcription, soap_note)

        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "message": "Audio processed successfully",
            "transcript_id": transcription_id,
            # "soap_note_id": soap_note_id,
            "transcription": transcription,
            "soap_note": soap_note,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")
