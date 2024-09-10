from unittest.mock import patch, AsyncMock

import httpx
import pytest

from api.tasks import async_post


@pytest.mark.asyncio
async def test_send_to_fhir():
    patient_data = {
        "resourceType": "Patient",
        "name": [{"use": "official", "family": "Da Silva", "given": ["João"]}],
        "gender": "male",
        "birthDate": "2000-01-01"
    }

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": "123"}

        result = await async_post(patient_data)

        assert result == {'id': "123"}

        mock_post.assert_called_once_with("http://fhir:8080/fhir/Patient", json=patient_data)


@pytest.mark.asyncio
async def test_send_to_fhir_with_fhir_disabled():
    patient_data = {
        "resourceType": "Patient",
        "name": [{"use": "official", "family": "Da Silva", "given": ["João"]}],
        "gender": "male",
        "birthDate": "2000-01-01"
    }

    with pytest.raises(Exception) as exception_info:
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.RequestError("Network error")
            await async_post(patient_data)

    assert exception_info.value.__str__() == 'Network error'
