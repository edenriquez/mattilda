import os
from flask_openapi3 import OpenAPI, Info, Tag
from src.db import db
from src.api.school_routes import school_router
from src.api.student_routes import student_router
from dotenv import load_dotenv
from flask import redirect

load_dotenv()

def create_app():
    info = Info(title="Mattilda API", version="1.0.0")
    app = OpenAPI(__name__, info=info)

    app.register_api(school_router)
    app.register_api(student_router)

    @app.get("/")
    def index():
        return {"message": "Welcome to Mattilda API. Go to /openapi/swagger for documentation."}

    @app.get("/docs")
    def docs():
        return redirect("/openapi/swagger")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
