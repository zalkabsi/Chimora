"""A deterministic, privacy-conscious Alexa+ front-desk simulation.

The app deliberately uses synthetic data and a local tool layer. It does not
identify visitors, control a lock, or send messages to anyone.
"""

from __future__ import annotations

import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

APP_DIR = Path(__file__).parent
INDEX_FILE = APP_DIR / "static" / "index.html"
FAVICON_FILE = APP_DIR / "static" / "favicon.svg"

SCENARIOS: dict[str, dict[str, Any]] = {
    "expected": {
        "label": "Scheduled arrival",
        "appointment_id": "apt-1500",
        "arrived_at": "2:58 PM",
        "stated_name": "Elena Ruiz",
        "stated_time": "3:00 PM",
        "minutes_from_midnight": 14 * 60 + 58,
        "description": "Visitor says they are here for a 3:00 appointment.",
    },
    "early": {
        "label": "Early arrival",
        "appointment_id": "apt-1600",
        "arrived_at": "3:30 PM",
        "stated_name": "Marcus Green",
        "stated_time": "4:00 PM",
        "minutes_from_midnight": 15 * 60 + 30,
        "description": "Visitor says they are here for a 4:00 appointment.",
    },
    "unknown": {
        "label": "Unrecognized arrival",
        "appointment_id": None,
        "arrived_at": "3:45 PM",
        "stated_name": None,
        "stated_time": None,
        "minutes_from_midnight": 15 * 60 + 45,
        "description": "Doorbell rang; no booking details were provided.",
    },
}

BASE_APPOINTMENTS: list[dict[str, Any]] = [
    {
        "id": "apt-1030",
        "name": "Priya Shah",
        "time": "10:30 AM",
        "minutes_from_midnight": 10 * 60 + 30,
        "service": "Laptop diagnostics",
        "status": "completed",
    },
    {
        "id": "apt-1500",
        "name": "Elena Ruiz",
        "time": "3:00 PM",
        "minutes_from_midnight": 15 * 60,
        "service": "Watch battery replacement",
        "status": "upcoming",
    },
    {
        "id": "apt-1600",
        "name": "Marcus Green",
        "time": "4:00 PM",
        "minutes_from_midnight": 16 * 60,
        "service": "Phone screen repair",
        "status": "upcoming",
    },
    {
        "id": "apt-1700",
        "name": "Samira Haddad",
        "time": "5:00 PM",
        "minutes_from_midnight": 17 * 60,
        "service": "Tablet pickup",
        "status": "upcoming",
    },
]


class ArrivalRequest(BaseModel):
    scenario: Literal["expected", "early", "unknown"]


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    arrival_id: str | None = None


class ReplyRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)

    @field_validator("text")
    @classmethod
    def require_nonblank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Reply text must not be blank")
        return value


def _new_state() -> dict[str, Any]:
    return {
        "appointments": deepcopy(BASE_APPOINTMENTS),
        "arrivals": [],
        "messages": [],
        "tool_calls": [],
        "next_arrival": 1,
        "next_tool_call": 1,
        "active_arrival_id": None,
        "simulated_now": "2:58 PM",
        "simulated_date": datetime.now().strftime("%A, %B %d").replace(" 0", " "),
    }


_state = _new_state()


def reset_demo() -> dict[str, Any]:
    """Reset the in-memory demo so every run starts with synthetic sample data."""
    global _state
    _state = _new_state()
    return get_state()


def _tool(name: str, arguments: dict[str, Any], result: str) -> None:
    _state["tool_calls"].insert(
        0,
        {
            "id": _state["next_tool_call"],
            "name": name,
            "arguments": arguments,
            "result": result,
            "at": _state["simulated_now"],
        },
    )
    _state["next_tool_call"] += 1
    del _state["tool_calls"][12:]


def _agent_plan(intent: str, tool_sequence: list[str], rationale: str) -> None:
    """Record the local rules-based assistant's selected task and tools."""
    _tool(
        "assistant_plan",
        {"intent": intent, "tool_sequence": tool_sequence},
        rationale,
    )


def list_appointments() -> list[dict[str, Any]]:
    """Tool: list the synthetic appointments on today's schedule."""
    appointments = deepcopy(_state["appointments"])
    _tool("list_appointments", {"date": _state["simulated_date"]}, f"Found {len(appointments)} appointments")
    return appointments


def match_arrival(arrival: dict[str, Any], appointment: dict[str, Any] | None = None) -> dict[str, Any]:
    """Tool: match only an appointment the visitor explicitly stated."""
    if appointment is None and arrival.get("appointment_id"):
        appointment = next(
            (item for item in _state["appointments"] if item["id"] == arrival["appointment_id"]),
            None,
        )
    matched = bool(
        appointment
        and arrival.get("stated_time") == appointment["time"]
        and arrival.get("stated_name")
        and arrival["stated_name"].casefold() == appointment["name"].casefold()
    )
    minutes_early = None
    if matched:
        minutes_early = appointment["minutes_from_midnight"] - arrival["minutes_from_midnight"]
    result = {
        "matched": matched,
        "appointment": deepcopy(appointment) if matched else None,
        "minutes_early": minutes_early,
        "basis": "visitor-stated name and booking time" if matched else "not enough stated details",
    }
    _tool(
        "match_arrival",
        {"arrival_id": arrival["id"], "stated_time": arrival.get("stated_time")},
        f"Matched {appointment['time']} booking" if matched else "No confident schedule match",
    )
    return result


def draft_reply(arrival: dict[str, Any]) -> dict[str, Any]:
    """Tool: draft a reply. The owner must approve it; nothing is delivered."""
    match = arrival.get("match") or {}
    appointment = match.get("appointment")
    if appointment:
        name = appointment["name"].split()[0]
        minutes_early = match.get("minutes_early", 0)
        if minutes_early >= 15:
            text = (
                f"Hi {name}, I see you’re early for your {appointment['time']} appointment. "
                "Would you like to wait here or come back closer to your time?"
            )
        elif minutes_early > 0:
            text = (
                f"Hi {name}, I see you’re here a few minutes early. "
                "Please make yourself comfortable; I’ll be with you shortly."
            )
        else:
            text = f"Hi {name}, I see you’re here. I’ll be with you shortly."
    else:
        text = "Hi there, welcome. Which booking time or name should I look for?"
    arrival["reply"] = {"text": text, "status": "pending", "approved_at": None}
    _tool("draft_reply", {"arrival_id": arrival["id"]}, "Created an owner-review draft")
    return deepcopy(arrival["reply"])


def _arrival_summary(arrival: dict[str, Any]) -> str:
    match = arrival.get("match") or {}
    appointment = match.get("appointment")
    if appointment:
        early = match["minutes_early"]
        timing = f"{early} minutes early" if early > 0 else f"{abs(early)} minutes late" if early < 0 else "on time"
        return (
            f"Yes. {appointment['name']} checked in at {arrival['arrived_at']} for the "
            f"{appointment['time']} appointment, {timing}. I matched the booking from the "
            "name and time the visitor stated; this does not verify identity."
        )
    return (
        f"A visitor rang at {arrival['arrived_at']}, but they haven’t stated a booking time or name. "
        "I can’t match them confidently. You can ask who they’re here to see."
    )


def _parse_time(question: str) -> str | None:
    normalized = question.casefold().replace("o’clock", "").replace("o'clock", "")
    match = re.search(r"\b(1[0-2]|0?[1-9])(?::([0-5]\d))?\s*(a\.?m\.?|p\.?m\.?)?\b", normalized)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    meridiem = (match.group(3) or "").replace(".", "")
    if not meridiem:
        # The demo schedule uses afternoon times for 3, 4, and 5 o'clock.
        meridiem = "pm" if hour in (3, 4, 5) else "am"
    return f"{hour}:{minute:02d} {meridiem.upper()}"


def get_state() -> dict[str, Any]:
    return deepcopy(_state)


def simulate_arrival(scenario_name: str) -> dict[str, Any]:
    if scenario_name not in SCENARIOS:
        raise HTTPException(status_code=404, detail="Unknown arrival scenario")
    scenario = SCENARIOS[scenario_name]
    _agent_plan(
        "handle_incoming_arrival",
        ["doorbell_event", "match_arrival", "draft_reply"],
        "A visitor event needs a schedule match and an editable reply for owner review.",
    )
    arrival = {
        "id": f"arrival-{_state['next_arrival']}",
        "scenario": scenario_name,
        "label": scenario["label"],
        "arrived_at": scenario["arrived_at"],
        "description": scenario["description"],
        "stated_name": scenario["stated_name"],
        "stated_time": scenario["stated_time"],
        "appointment_id": scenario["appointment_id"],
        "minutes_from_midnight": scenario["minutes_from_midnight"],
        "match": None,
        "reply": None,
    }
    _state["next_arrival"] += 1
    _state["simulated_now"] = scenario["arrived_at"]
    _tool("doorbell_event", {"scenario": scenario_name}, "Simulated visitor arrival received")
    arrival["match"] = match_arrival(arrival)
    _state["arrivals"].insert(0, arrival)
    del _state["arrivals"][20:]
    _state["active_arrival_id"] = arrival["id"]
    draft_reply(arrival)
    _state["messages"].append({"role": "assistant", "text": _arrival_summary(arrival)})
    del _state["messages"][:-60]
    return get_state()


def _answer_question(question: str, arrival_id: str | None = None) -> str:
    question_lc = question.casefold()
    target_time = _parse_time(question)
    asks_for_reply = any(word in question_lc for word in ("tell", "reply", "say", "message"))
    if target_time:
        _agent_plan(
            "check_appointment_status",
            ["list_appointments", "match_arrival"],
            f"Appointment time detected ({target_time}); check today's schedule and compare visitor-stated details.",
        )
        appointments = list_appointments()
    elif asks_for_reply:
        _agent_plan(
            "draft_owner_reply",
            ["draft_reply"],
            "A reply was requested; prepare a draft for the active arrival and leave approval to the owner.",
        )
        appointments = []
    else:
        _agent_plan(
            "summarize_active_arrival",
            [],
            "No appointment time or reply was requested; summarize the active arrival or ask for a sample event.",
        )
        appointments = []
    appointment = next(
        (item for item in appointments if item["time"].casefold() == (target_time or "").casefold()),
        None,
    )
    if appointment:
        arrival = next(
            (item for item in _state["arrivals"] if item.get("appointment_id") == appointment["id"]),
            None,
        )
    else:
        arrival = next(
            (item for item in _state["arrivals"] if arrival_id and item["id"] == arrival_id),
            None,
        )
        if arrival is None and _state["active_arrival_id"]:
            arrival = next(
                (item for item in _state["arrivals"] if item["id"] == _state["active_arrival_id"]),
                None,
            )
    if appointment and arrival:
        arrival["match"] = match_arrival(arrival, appointment)
        if arrival["match"]["matched"]:
            answer = _arrival_summary(arrival)
        else:
            answer = f"There’s a doorbell event, but I can’t link it to the {appointment['time']} booking confidently."
    elif appointment:
        unresolved = next(
            (item for item in _state["arrivals"] if not (item.get("match") or {}).get("matched")),
            None,
        )
        _tool(
            "match_arrival",
            {
                "appointment_id": appointment["id"],
                "arrival_id": unresolved["id"] if unresolved else None,
            },
            "Unresolved visitor present" if unresolved else "No linked arrival event",
        )
        if unresolved:
            answer = (
                f"A visitor rang at {unresolved['arrived_at']}, but they haven’t stated details "
                f"that connect them to {appointment['time']}. I can’t tell if it’s {appointment['name']}."
            )
        else:
            answer = (
                f"No visitor is checked in for {appointment['time']} yet. "
                f"{appointment['name']} is booked for {appointment['time']}, and no matching doorbell event is recorded."
            )
    else:
        arrival = next((item for item in _state["arrivals"] if item["id"] == arrival_id), None)
        if arrival is None and _state["active_arrival_id"]:
            arrival = next(
                (item for item in _state["arrivals"] if item["id"] == _state["active_arrival_id"]),
                None,
            )
        if arrival and asks_for_reply:
            reply = draft_reply(arrival)
            answer = f"I drafted a reply for your approval: “{reply['text']}”"
        elif arrival:
            answer = _arrival_summary(arrival)
        else:
            answer = "I don’t see a visitor event yet. Simulate an arrival and I’ll check it against today’s bookings."
    _state["messages"].append({"role": "user", "text": question})
    _state["messages"].append({"role": "assistant", "text": answer})
    del _state["messages"][:-60]
    return answer


app = FastAPI(title="Doorbell Desk", version="0.1.0")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(INDEX_FILE)


@app.get("/favicon.svg", include_in_schema=False)
def favicon() -> FileResponse:
    return FileResponse(FAVICON_FILE, media_type="image/svg+xml")


@app.get("/api/state")
def api_state() -> dict[str, Any]:
    return get_state()


@app.post("/api/reset")
def api_reset() -> dict[str, Any]:
    return reset_demo()


@app.post("/api/arrivals")
def api_arrival(request: ArrivalRequest) -> dict[str, Any]:
    return simulate_arrival(request.scenario)


@app.post("/api/ask")
def api_ask(request: AskRequest) -> dict[str, Any]:
    answer = _answer_question(request.question.strip(), request.arrival_id)
    return {"answer": answer, "state": get_state()}


@app.post("/api/arrivals/{arrival_id}/approve")
def api_approve(arrival_id: str, request: ReplyRequest) -> dict[str, Any]:
    arrival = next((item for item in _state["arrivals"] if item["id"] == arrival_id), None)
    if arrival is None:
        raise HTTPException(status_code=404, detail="Arrival not found")
    if not arrival.get("reply") or arrival["reply"]["status"] != "pending":
        raise HTTPException(status_code=409, detail="There is no pending reply to approve")
    arrival["reply"] = {
        "text": request.text.strip(),
        "status": "approved_simulated",
        "approved_at": _state["simulated_now"],
    }
    _tool("approve_reply", {"arrival_id": arrival_id}, "Owner approved draft (no message was sent)")
    return get_state()


@app.post("/api/arrivals/{arrival_id}/dismiss")
def api_dismiss(arrival_id: str) -> dict[str, Any]:
    arrival = next((item for item in _state["arrivals"] if item["id"] == arrival_id), None)
    if arrival is None:
        raise HTTPException(status_code=404, detail="Arrival not found")
    if not arrival.get("reply") or arrival["reply"]["status"] != "pending":
        raise HTTPException(status_code=409, detail="There is no pending reply to dismiss")
    arrival["reply"]["status"] = "dismissed"
    _tool("dismiss_reply", {"arrival_id": arrival_id}, "Owner dismissed draft")
    return get_state()
