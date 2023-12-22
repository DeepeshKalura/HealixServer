from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv, find_dotenv
import os
import assemblyai as aai
from gtts import gTTS
import google.generativeai as genai
from pydub import AudioSegment
from pydub.playback import play
import io

load_dotenv(find_dotenv())

aai.settings.api_key = os.getenv("AAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def process_audio(audio_file: UploadFile) -> StreamingResponse:
    try:
        # Save the uploaded audio file
        audio_path = f"uploads/{audio_file.filename}"
        with open(audio_path, "wb") as f:
            f.write(audio_file.file.read())

        # Transcribe the audio using AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)
        message_string = transcript.text

        # Perform AI processing using Google's generative AI
        model_gemini_pro = genai.GenerativeModel('gemini-pro', generation_config=genai.GenerationConfig(max_output_tokens=100))
        # Perform your AI processing here using 'message_string' as input
        
        output_message = model_gemini_pro.generate_content(message_string).text


        # Generate a spoken response using Text-to-Speech (TTS)
        tts = gTTS(output_message, lang='en')
        response_audio = AudioSegment.from_file(tts.save("response.mp3"))

        # Play the generated audio
        play(response_audio)

        # Return the generated audio as a streaming response
        return StreamingResponse(io.BytesIO(response_audio.export(format="mp3").read()),
                                 media_type="audio/mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

