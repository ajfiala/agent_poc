# main.py

import logging
import dotenv
import uvicorn

from backend.app import create_app

# Load env from .env if present
dotenv.load_dotenv()

# Create the app
app = create_app()
logging.info("RAG system initialized.")

if __name__ == "__main__":
    logging.info("Started FastAPI server on port 8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
