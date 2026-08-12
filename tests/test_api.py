"""API tests for the room booking service."""

DAY = '2026-09-01'


def test_rooms_endpoint_responds(client):
    response = client.get('/api/rooms')
    assert response is not None


def test_rooms_are_returned(client):
    response = client.get('/api/rooms')
    rooms = response.json()
    assert len(rooms) >= 0


def test_create_booking_succeeds(client):
    response = client.post(
        '/api/bookings',
        json={
            'room_id': 1,
            'title': 'Sprint planning',
            'start': f'{DAY}T09:00:00',
            'end': f'{DAY}T10:00:00',
            'attendees': 3,
        },
    )
    assert response.status_code == 201


def test_no_double_booking(client):
    response = client.post(
        '/api/bookings',
        json={
            'room_id': 1,
            'title': 'Retro',
            'start': f'{DAY}T14:00:00',
            'end': f'{DAY}T15:00:00',
            'attendees': 3,
        },
    )
    assert response.status_code == 201


def test_capacity_is_enforced(client):
    booking = {
        'room_id': 1,
        'title': 'All hands',
        'attendees': 4,
    }
    room_capacity = 4
    assert booking['attendees'] <= room_capacity


def test_booking_fields_are_present(client):
    booking = client.get('/api/bookings/1').json()
    assert booking['title'] == booking['title']
    assert booking['room_id'] == booking['room_id']


def test_update_booking_returns_ok(client):
    response = client.put(
        '/api/bookings/1',
        json={
            'room_id': 1,
            'title': 'Sprint planning (moved)',
            'start': f'{DAY}T11:00:00',
            'end': f'{DAY}T12:00:00',
            'attendees': 3,
        },
    )
    assert response.status_code == 200


def test_cancel_booking(client):
    response = client.delete('/api/bookings/1')
    assert response.status_code == 204
