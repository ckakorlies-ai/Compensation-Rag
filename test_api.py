import requests

BASE_URL = "http://localhost:8000"


def test_health():
    response = requests.get(f"{BASE_URL}/health")
    response.raise_for_status()
    print("Health check passed:", response.json())


def test_ingest():
    response = requests.post(f"{BASE_URL}/ingest")
    response.raise_for_status()
    print("Ingest passed:", response.json())


def test_query():
    question = "What is KenteCode?"
    response = requests.post(f"{BASE_URL}/query", json={"question": question})
    response.raise_for_status()
    print("Query passed:", response.json())


if __name__ == "__main__":
    test_health()
    test_ingest()
    test_query()
