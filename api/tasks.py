import os

import httpx
from celery import shared_task
from dotenv import load_dotenv

load_dotenv()

FHIR_ENDPOINT = os.getenv("FHIR_ENDPOINT", "http://localhost:8080/fhir")

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 10})
def send_patient_to_fhir(patient_data):
    async def async_post():
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{FHIR_ENDPOINT}/Patient", json=patient_data)
                print(f"Sent to FHIR: {response.status_code}")
            except Exception as e:
                print("Connection Failed, Retrying in 10 seconds")
                raise

    import asyncio
    asyncio.run(async_post())
