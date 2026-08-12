"""HTTP API and static file serving for the room booking service."""

from __future__ import annotations

import pathlib

import fastapi
from fastapi import responses, staticfiles

from app import models, store as store_module

STATIC_DIR = pathlib.Path(__file__).parent / 'static'

api = fastapi.FastAPI(title='Room Booking')
store = store_module.store


@api.exception_handler(store_module.BookingError)
async def booking_error_handler(
    _request: fastapi.Request, exc: store_module.BookingError
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=exc.status, content={'error': exc.message}
    )


@api.get('/api/rooms')
def list_rooms() -> list[models.Room]:
    return store.rooms()


@api.get('/api/bookings')
def list_bookings() -> list[models.Booking]:
    return store.all()


@api.get('/api/bookings/{booking_id}')
def get_booking(booking_id: int) -> models.Booking:
    booking = store.get(booking_id)
    if booking is None:
        raise store_module.BookingError(
            f'No booking with id {booking_id}', status=404
        )
    return booking


@api.post('/api/bookings', status_code=201)
def create_booking(request: models.BookingRequest) -> models.Booking:
    return store.create(request)


@api.put('/api/bookings/{booking_id}')
def update_booking(
    booking_id: int, request: models.BookingRequest
) -> models.Booking:
    return store.update(booking_id, request)


@api.delete('/api/bookings/{booking_id}', status_code=204)
def delete_booking(booking_id: int) -> responses.Response:
    store.delete(booking_id)
    return responses.Response(status_code=204)


@api.post('/api/reset', status_code=204)
def reset() -> responses.Response:
    """Clear all bookings. Used by the UI tests between runs."""
    store.reset()
    return responses.Response(status_code=204)


api.mount('/', staticfiles.StaticFiles(directory=STATIC_DIR, html=True), name='ui')
