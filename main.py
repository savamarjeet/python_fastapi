from app import app

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    except Exception as e:
        print(f"Error during UVicorn run: {e}")
