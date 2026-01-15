import json
import os
from typing import Any, Dict
from litellm import completion
from dotenv import load_dotenv
import logging
from pydantic import ValidationError, TypedDict

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a travel expert assistant. Generate structured travel itineraries in JSON format.
The response must be valid JSON with the following keys:
- destination: string
- price_range: string (e.g., "$", "$$", "$$$", "$$$$")
- ideal_visit_times: array of strings
- top_attractions: array of strings

Always return valid JSON only, no additional text."""

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

class TravelItinerary(TypedDict):
    destination: str
    price_range: str
    ideal_visit_times: str
    top_attractions: str 

def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    # implement litellm call here to generate a structured travel itinerary for the given destination

    # See https://docs.litellm.ai/docs/ for reference.


    response = completion(
        model=MODEL,
        api_key=api_key,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Generate a travel itinerary for the destination: " + destination}
        ]
    ) 
    try:    
        data = json.loads(response.choices[0].message.content)  
        return TravelItinerary(**data)
    except (json.JSONDecodeError, ValidationError):
        # TODO: Can add retry logic here if needed
        raise ValueError("Invalid response schema")

# curl "http://localhost:8000/api/v1/itinerary?destination=Paris"