import json
from io import BytesIO

import pytest
from django.test import Client

from api.views.entry import DEFAULT_RESPONSE


@pytest.fixture
def csv_text():
    return "Nome,CPF,Gênero,Data de Nascimento,Telefone,País de Nascimento,Observação\nJoão da Silva,123.456.789-00,Masculino,10/05/1980,(11) 1234-5678,Brasil,"


@pytest.mark.django_db
def test_upload_csv_as_text(csv_text):
    client = Client()

    response = client.post("/api/patient/csv", {'data': csv_text}, content_type='application/json')

    assert response.status_code == 200
    assert json.loads(response.content.decode()) == {"message": DEFAULT_RESPONSE}


@pytest.mark.django_db
def test_upload_csv_as_file_with_utf_encoding(csv_text):
    client = Client()

    csv_file = BytesIO(csv_text.encode('utf-8'))
    payload = {'file': csv_file}

    response = client.post("/api/patient/file", data=payload, format='multipart')

    assert response.status_code == 200
    assert json.loads(response.content.decode()) == {"message": DEFAULT_RESPONSE}

@pytest.mark.django_db
def test_upload_csv_as_file_with_iso_encoding(csv_text):
    client = Client()

    csv_file = BytesIO(csv_text.encode('ISO-8859-1'))
    payload = {'file': csv_file}

    response = client.post("/api/patient/file", data=payload, format='multipart')

    assert response.status_code == 200
    assert json.loads(response.content.decode()) == {"message": DEFAULT_RESPONSE}