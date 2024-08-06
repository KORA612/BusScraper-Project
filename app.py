from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import motor.motor_asyncio
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Load environment variables
load_dotenv()

app = FastAPI()

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.bus_scraper
collection = db.search_results

class SearchQuery(BaseModel):
    origin: str
    destination: str
    date: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/search")
async def search_bus(query: SearchQuery):
    # Construct the URL
    url = f"https://safar724.com/bus/{query.origin}-{query.destination}?date={query.date}"
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    driver = webdriver.Chrome()
    driver.get(url)
'''
    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the search results to load (adjust the selector as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-result-item"))
        )

        # Extract the search results
        results = []
        result_elements = driver.find_elements(By.CLASS_NAME, "search-result-item")
        for element in result_elements:
            result = {
                'departure_time': element.find_element(By.CLASS_NAME, "departure-time").text,
                'arrival_time': element.find_element(By.CLASS_NAME, "arrival-time").text,
                'price': element.find_element(By.CLASS_NAME, "price").text,
                # Add more fields as needed
            }
            results.append(result)

        # Print results to terminal
        print("Search Results:")
        for result in results:
            print(result)

        # Store request and response in MongoDB
        document = {
            "request": query.model_dump(),
            "response": results,
            "timestamp": datetime.now()
        }
        await collection.insert_one(document)

        return {"message": "Search completed and results stored in database", "results": results}

    except TimeoutException:
        raise HTTPException(status_code=408, detail="Request timed out. The page took too long to load.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        driver.quit()
'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)