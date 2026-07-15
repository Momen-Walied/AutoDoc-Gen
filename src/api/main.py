from fastapi import FastAPI

def create_app() -> FastAPI:
    return FastAPI(title="autodoc-gen", version="0.1.0")