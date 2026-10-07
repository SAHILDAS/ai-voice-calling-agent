import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_start_call():
    response = client.post(
        "/api/calls/start",
        json={"customer_id": "CUST1001"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == "CUST1001"
    assert data["application_id"] == "LN1001"
    assert data["customer_name"] == "Rahul Sharma"
    assert data["status"] == "CONNECTED"
    assert data["call_id"].startswith("CALL-")


def test_start_call_invalid_customer():
    response = client.post(
        "/api/calls/start",
        json={"customer_id": "INVALID"},
    )

    assert response.status_code == 404


def test_call_lifecycle():
    start_response = client.post(
        "/api/calls/start",
        json={"customer_id": "CUST1001"},
    )

    assert start_response.status_code == 200

    call_id = start_response.json()["call_id"]

    message_response = client.post(
        f"/api/calls/{call_id}/message",
        json={
            "message": "What documents are still pending for my loan?"
        },
    )

    assert message_response.status_code == 200

    message_data = message_response.json()

    assert message_data["agent_response"]
    assert message_data["call_id"] == call_id

    transcript_response = client.get(
        f"/api/calls/{call_id}/transcript"
    )

    assert transcript_response.status_code == 200

    transcript = transcript_response.json()

    assert len(transcript["messages"]) >= 3
    assert transcript["messages"][0]["role"] == "agent"
    assert transcript["messages"][1]["role"] == "customer"
    assert transcript["messages"][2]["role"] == "agent"

    end_response = client.post(
        f"/api/calls/{call_id}/end"
    )

    assert end_response.status_code == 200

    summary = end_response.json()["summary"]

    assert summary["call_id"] == call_id
    assert summary["customer_id"] == "CUST1001"
    assert summary["application_id"] == "LN1001"
    assert summary["duration_seconds"] >= 0
    assert summary["summary"]
    assert summary["sentiment"]

    summary_response = client.get(
        f"/api/calls/{call_id}/summary"
    )

    assert summary_response.status_code == 200

    assert summary_response.json()["call_id"] == call_id
