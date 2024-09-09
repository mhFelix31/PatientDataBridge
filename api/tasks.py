from celery import shared_task
import httpx

from config import settings

@shared_task
def send_patient_to_fhir(patient_data):
    async def async_post():
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.FHIR_ENDPOINT}/Patient", json=patient_data)
            print(f"Sent to FHIR: {response.status_code}")
    
    import asyncio
    asyncio.run(async_post())