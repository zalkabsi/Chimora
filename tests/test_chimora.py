import asyncio
from typing import Any

import httpx

from chimora.app import app, reset_demo


class LocalClient:
    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        async def send_request() -> httpx.Response:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                return await client.request(method, path, **kwargs)

        return asyncio.run(send_request())

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", path, **kwargs)


client = LocalClient()


def setup_function() -> None:
    reset_demo()


def test_expected_arrival_matches_booking_and_reports_early_minutes() -> None:
    response = client.post("/api/arrivals", json={"scenario": "expected"})

    assert response.status_code == 200
    state = response.json()
    arrival = state["arrivals"][0]
    assert arrival["match"]["matched"] is True
    assert arrival["match"]["appointment"]["name"] == "Elena Ruiz"
    assert arrival["match"]["minutes_early"] == 2
    assert arrival["reply"]["status"] == "pending"


def test_question_matches_time_and_returns_traceable_tool_calls() -> None:
    client.post("/api/arrivals", json={"scenario": "expected"})

    response = client.post("/api/ask", json={"question": "Is my 3 o'clock here?"})

    assert response.status_code == 200
    payload = response.json()
    assert "2 minutes early" in payload["answer"]
    assert {call["name"] for call in payload["state"]["tool_calls"]} >= {
        "list_appointments",
        "match_arrival",
    }


def test_early_arrival_is_matched_and_suggests_wait_or_return() -> None:
    state = client.post("/api/arrivals", json={"scenario": "early"}).json()
    arrival = state["arrivals"][0]

    assert arrival["match"]["matched"] is True
    assert arrival["match"]["minutes_early"] == 30
    assert "wait here or come back" in arrival["reply"]["text"]


def test_unrecognized_visitor_is_not_guessed() -> None:
    state = client.post("/api/arrivals", json={"scenario": "unknown"}).json()
    arrival = state["arrivals"][0]

    assert arrival["match"]["matched"] is False
    assert arrival["match"]["appointment"] is None
    assert "can’t match them confidently" in state["messages"][-1]["text"]
    assert "Which booking time or name" in arrival["reply"]["text"]


def test_unresolved_visitor_does_not_get_misreported_as_a_known_booking() -> None:
    client.post("/api/arrivals", json={"scenario": "unknown"})

    response = client.post("/api/ask", json={"question": "Is my 3 o’clock here?"})

    assert response.status_code == 200
    assert "can’t tell if it’s Elena Ruiz" in response.json()["answer"]


def test_reply_requires_owner_approval_and_approval_does_not_send() -> None:
    state = client.post("/api/arrivals", json={"scenario": "expected"}).json()
    arrival_id = state["arrivals"][0]["id"]

    response = client.post(
        f"/api/arrivals/{arrival_id}/approve",
        json={"text": "Edited owner-approved draft"},
    )

    assert response.status_code == 200
    approved = response.json()["arrivals"][0]["reply"]
    assert approved["status"] == "approved_simulated"
    assert approved["text"] == "Edited owner-approved draft"
    assert "no message was sent" in response.json()["tool_calls"][0]["result"].lower()


def test_reply_cannot_be_approved_twice_or_without_a_pending_draft() -> None:
    response = client.post("/api/arrivals/arrival-unknown/approve", json={"text": "Hello"})
    assert response.status_code == 404

    state = client.post("/api/arrivals", json={"scenario": "unknown"}).json()
    arrival_id = state["arrivals"][0]["id"]
    client.post(f"/api/arrivals/{arrival_id}/dismiss")
    response = client.post(f"/api/arrivals/{arrival_id}/approve", json={"text": "Hello"})

    assert response.status_code == 409


def test_blank_reply_text_is_rejected() -> None:
    state = client.post("/api/arrivals", json={"scenario": "expected"}).json()
    arrival_id = state["arrivals"][0]["id"]

    response = client.post(
        f"/api/arrivals/{arrival_id}/approve",
        json={"text": "   "},
    )

    assert response.status_code == 422


def test_reset_clears_events_and_restores_seed_schedule() -> None:
    client.post("/api/arrivals", json={"scenario": "unknown"})

    response = client.post("/api/reset")

    assert response.status_code == 200
    assert response.json()["arrivals"] == []
    assert response.json()["simulated_now"] == "2:58 PM"
    assert len(response.json()["appointments"]) == 4


def test_homepage_serves_the_web_app() -> None:
    response = client.get("/")
    favicon = client.get("/favicon.svg")

    assert response.status_code == 200
    assert "Chimora" in response.text
    assert "Expected arrival" in response.text
    assert favicon.status_code == 200
    assert "<svg" in favicon.text
