from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from deep_translator import GoogleTranslator
from .models import TranslationRequest, TranslationResponse, FoodItem, NavigationAlert, FoodTrackRequest
from .database import db
import base64
from PIL import Image
import io

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.pages.dev",
        "https://your-custom-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/translate", response_model=TranslationResponse)
async def translate_image(request: TranslationRequest):
    try:
        # Input validation
        if not request.image_url:
            print("Error: Missing image data")
            raise HTTPException(status_code=400, detail="Image data is required")
            
        # Extract base64 data
        try:
            image_data = request.image_url
            if "base64," in image_data:
                # Split on first occurrence of base64,
                image_data = image_data.split("base64,", 1)[1]
            
            # Validate base64 format
            try:
                image_bytes = base64.b64decode(image_data)
                print("Successfully decoded base64 image data")
            except Exception as e:
                print(f"Base64 decode error: {str(e)}")
                raise HTTPException(status_code=400, detail="Invalid image format")
                
            # Validate image data
            try:
                image = Image.open(io.BytesIO(image_bytes))
                print(f"Successfully opened image: {image.format} {image.size}")
            except Exception as e:
                print(f"Image processing error: {str(e)}")
                raise HTTPException(status_code=400, detail="Invalid image data")
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"Image extraction error: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to process image data")
            
        # Translation
        try:
            # For now, we'll simulate with dummy text
            original_text = "Hello World"
            translator = GoogleTranslator(source='auto', target=request.target_language)
            translated = translator.translate(original_text)
            print(f"Translation successful: {original_text} -> {translated}")
            
            return TranslationResponse(
                translated_text=translated,
                original_text=original_text,
                confidence=0.95
            )
        except Exception as e:
            print(f"Translation service error: {str(e)}")
            raise HTTPException(status_code=500, detail="Translation service error")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in translation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/food/track/{user_id}")
async def track_food(user_id: str, request: FoodTrackRequest):
    try:
        # Remove data URL prefix if present
        if "base64," in request.image:
            image = request.image.split("base64,")[1]
            
        # Decode base64 image
        try:
            image_data = base64.b64decode(image)
            image_io = io.BytesIO(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")
        
        # In a real implementation, we would:
        # 1. Use ML model to identify food
        # 2. Calculate calories
        # For now, we'll simulate with dummy data
        food_item = FoodItem(
            name="Sample Food",
            calories=500.0,
            timestamp=datetime.now(),
            image_url="sample_url"
        )
        
        db.add_food_item(user_id, food_item)
        return {"message": "Food tracked successfully", "food_item": food_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/food/history/{user_id}")
async def get_food_history(user_id: str):
    try:
        food_items = db.get_food_items(user_id)
        return {"food_items": food_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/navigation/alert/{user_id}")
async def process_navigation(user_id: str, image: str):
    try:
        # Remove data URL prefix if present
        if "base64," in image:
            image = image.split("base64,")[1]
            
        # Decode base64 image
        try:
            image_data = base64.b64decode(image)
            image_io = io.BytesIO(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")
            
        # In a real implementation, we would:
        # 1. Process image using computer vision
        # 2. Detect obstacles and landmarks
        # For now, we'll simulate with different types of alerts
        import random
        alert_types = [
            ("obstacle", "Door ahead", 2.5, "forward"),
            ("warning", "Stairs approaching", 3.0, "forward"),
            ("landmark", "Open space ahead", 5.0, "forward"),
            ("obstacle", "Wall on the right", 1.0, "right")
        ]
        alert_type, desc, dist, direction = random.choice(alert_types)
        
        alert = NavigationAlert(
            alert_type=alert_type,
            description=desc,
            distance=dist,
            direction=direction
        )
        db.add_navigation_alert(user_id, alert)
        return {"message": "Navigation alert processed", "alert": alert}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/navigation/history/{user_id}")
async def get_navigation_history(user_id: str):
    try:
        alerts = db.get_navigation_history(user_id)
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to AI Glasses API"}
