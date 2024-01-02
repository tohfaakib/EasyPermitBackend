from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from validate_address import validate_address, save_property
from models import SmartyAutoAddress, Property

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://13.52.237.115:9000",
    "http://13.52.237.115:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"data": "ok"}

@app.post("/api/get-permit-validation")
def get_permit_validation(smartyAutoAddress: SmartyAutoAddress):
    return validate_address(smartyAutoAddress.model_dump())

@app.post("/api/property-save")
def property(property: Property):
    try:
        return save_property(property.model_dump())
    except Exception as e:
        response = {
                'data': {
                    'message': "Input Data Missing. Please check",
                    'success': False
                },
            }
        return response
