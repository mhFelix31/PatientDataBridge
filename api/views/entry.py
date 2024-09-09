
from io import StringIO
from django.http import HttpRequest
from ninja import File, Router, Schema
import pandas

from api.tasks import send_patient_to_fhir


router = Router()

class PatientInJSONText(Schema):
    data:str

class DefaultResponse(Schema):
    message: str

DEFAULT_RESPONSE = "CSV uploaded and processing started."


@router.post("/patient/file", response=DefaultResponse)
def receive_patient_via_file(request: HttpRequest, file: any):
    data = pandas.read_csv(file)

    process_data(data)

    return DEFAULT_RESPONSE

@router.post("/patient", response=DefaultResponse)
def receive_patient_via_text(request: HttpRequest, body: PatientInJSONText):
    csv_string_IO = StringIO(body.data)
    data = pandas.read_csv(csv_string_IO, sep=',', header=None)
    
    process_data(data)
    
    return DEFAULT_RESPONSE


def process_data(data):
    patients_data = []

    for _, row in data.iterrows():
        patients_data.append({
            "resourceType": "Patient",
            "name": [{"use": "official", "family": row["last_name"], "given": [row["first_name"]]}],
            "gender": row["gender"],
            "birthDate": row["birthdate"]
        })
    
    async def send_to_task():
        for patient_data in patients_data:
            send_patient_to_fhir.delay(patient_data)
    
    import asyncio
    asyncio.run(send_to_task())

    
    