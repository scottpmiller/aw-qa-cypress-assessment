"""Domain models for the room booking service."""

from __future__ import annotations

import datetime

import pydantic


class Room(pydantic.BaseModel):
    id: int
    name: str
    capacity: int


class BookingRequest(pydantic.BaseModel):
    room_id: int
    title: str
    start: datetime.datetime
    end: datetime.datetime
    attendees: int


class Booking(pydantic.BaseModel):
    id: int
    room_id: int
    title: str
    start: datetime.datetime
    end: datetime.datetime
    attendees: int
