import os
import sys
import uvicorn

# Add the 'src' directory to the Python path so the 'nassa' package is resolvable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

if __name__ == "__main__":
    # Start the FastAPI server using Uvicorn
    uvicorn.run("nassa.main:app", host="127.0.0.1", port=8000, reload=True)
