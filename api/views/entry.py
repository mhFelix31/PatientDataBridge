from io import StringIO

import pandas
from django.http import HttpRequest
from ninja import Router, Schema, File
from ninja.files import UploadedFile

from api.tasks import send_patient_to_fhir

router = Router()


class PatientInJSONText(Schema):
    data: str


class DefaultResponse(Schema):
    message: str


DEFAULT_RESPONSE = "CSV uploaded and processing started."


@router.post(path="/csv", response=DefaultResponse, tags=["Send info"])
def receive_patient_via_text(request: HttpRequest, body: PatientInJSONText):
    """
    Receives the patient info as JSON containing a CSV string
    Example:
    {"data": "Nome,CPF,Gênero,Data de Nascimento,Telefone,País de Nascimento,Observação\\nJoão da Silva,123.456.789-00,Masculino,10/05/1980,(11) 1234-5678,Brasil,"}
    """
    csv_string_io = StringIO(body.data)
    data = pandas.read_csv(csv_string_io)

    process_data(data)

    return {"message": DEFAULT_RESPONSE}


@router.post(path="/file", response=DefaultResponse, tags=["Send info"])
def receive_patient_via_file(request: HttpRequest, file: UploadedFile = File(...)):
    """
    Receives the patient info as a CSV file
    """

    file_read = file.read()
    try:
        file_decoded = file_read.decode("utf-8")
    except UnicodeDecodeError:
        file_decoded = file_read.decode("ISO-8859-1")

    data = pandas.read_csv(StringIO(file_decoded))

    process_data(data)

    return {'message': DEFAULT_RESPONSE}


def process_data(data):
    for _, row in data.iterrows():
        full_name = row["Nome"].split()
        first_name = full_name[0]
        last_name = " ".join(full_name[1:]) if len(full_name) > 1 else ""
        birth_date = pandas.to_datetime(row["Data de Nascimento"], dayfirst=True).strftime('%Y-%m-%d')
        gender = "male" if row["Gênero"].lower() == "masculino" else "female"

        send_patient_to_fhir.delay({
            "resourceType": "Patient",
            "name": [{"use": "official", "family": last_name, "given": [first_name]}],
            "gender": gender,
            "birthDate": birth_date,
        })
