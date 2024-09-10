import json
from io import StringIO

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
def test_upload_csv_as_file(csv_text):
    client = Client()

    csv_file = StringIO(csv_text)

    response = client.post("/api/patient/file", {'file': csv_file}, format='multipart')

    assert response.status_code == 200
    assert json.loads(response.content.decode()) == {"message": DEFAULT_RESPONSE}
