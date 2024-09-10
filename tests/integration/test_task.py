from unittest.mock import patch

import httpx
import pytest

from api.tasks import send_patient_to_fhir


def test_send_to_fhir():
    patient_data = {
        "resourceType": "Patient",
        "name": [{"use": "official", "family": "Da Silva", "given": ["João"]}],
        "gender": "male",
        "birthDate": "2000-01-01"
    }

    with patch("httpx.Client.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": "123"}

        result = send_patient_to_fhir(patient_data)

        assert result == {'id': "123"}
        mock_post.assert_called_once_with("http://fhir:8080/fhir/Patient", json=patient_data)


def test_send_to_fhir_with_fhir_disabled():
    patient_data = {
        "resourceType": "Patient",
        "name": [{"use": "official", "family": "Da Silva", "given": ["João"]}],
        "gender": "male",
        "birthDate": "2000-01-01"
    }

    with pytest.raises(Exception) as exception_info:
        with patch("httpx.Client.post") as mock_post:
            mock_post.side_effect = httpx.RequestError("Network error")
            send_patient_to_fhir(patient_data)

    assert str(exception_info.value) == 'Network error'
