from os import getenv

from dotenv import load_dotenv
import uvicorn

load_dotenv()

PORT = int(getenv("PORT")) if getenv("PORT") else 3000

if __name__ == "__main__":
    uvicorn.run(
        "app.app:init",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        factory=True
    )
