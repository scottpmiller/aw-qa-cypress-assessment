"""In-memory storage and booking rules.

The whole service is a single process with no database. Restarting the server
resets everything back to the seed data below.
"""

from __future__ import annotations

from app import models

ROOMS: list[models.Room] = [
    models.Room(id=1, name='Ellsworth', capacity=4),
    models.Room(id=2, name='Fairmount', capacity=10),
    models.Room(id=3, name='Rittenhouse', capacity=20),
]


class BookingError(Exception):
    """Raised when a booking cannot be created or changed."""

    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status = status


class BookingStore:
    def __init__(self) -> None:
        self._bookings: dict[int, models.Booking] = {}
        self._next_id = 1

    def reset(self) -> None:
        self._bookings.clear()
        self._next_id = 1

    def rooms(self) -> list[models.Room]:
        return list(ROOMS)

    def room(self, room_id: int) -> models.Room | None:
        return next((r for r in ROOMS if r.id == room_id), None)

    def all(self) -> list[models.Booking]:
        return sorted(self._bookings.values(), key=lambda b: b.start)

    def get(self, booking_id: int) -> models.Booking | None:
        return self._bookings.get(booking_id)

    def create(self, request: models.BookingRequest) -> models.Booking:
        room = self.room(request.room_id)
        if room is None:
            raise BookingError(f'No room with id {request.room_id}', status=404)
        if request.end <= request.start:
            raise BookingError('A booking must end after it starts')
        if request.attendees < 1:
            raise BookingError('A booking needs at least one attendee')
        if request.attendees > room.capacity:
            raise BookingError(
                f'{room.name} holds {room.capacity} people, '
                f'{request.attendees} requested'
            )
        for existing in self._bookings.values():
            if existing.room_id != request.room_id:
                continue
            if self._overlaps(request.start, request.end, existing):
                raise BookingError(
                    f'{room.name} is already booked for that time', status=409
                )

        booking = models.Booking(id=self._next_id, **request.model_dump())
        self._bookings[booking.id] = booking
        self._next_id += 1
        return booking

    def update(self, booking_id: int, request: models.BookingRequest) -> models.Booking:
        if booking_id not in self._bookings:
            raise BookingError(f'No booking with id {booking_id}', status=404)
        booking = models.Booking(id=booking_id, **request.model_dump())
        self._bookings[booking_id] = booking
        return booking

    def delete(self, booking_id: int) -> None:
        if booking_id not in self._bookings:
            raise BookingError(f'No booking with id {booking_id}', status=404)
        del self._bookings[booking_id]

    @staticmethod
    def _overlaps(start, end, existing: models.Booking) -> bool:
        return start <= existing.end and end >= existing.start


store = BookingStore()
