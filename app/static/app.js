const form = document.getElementById('booking-form');
const errorEl = document.getElementById('error');
const listEl = document.getElementById('bookings');
const roomEl = document.getElementById('room');

let rooms = [];

function formatWhen(startIso, endIso) {
  const opts = { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' };
  const start = new Date(startIso);
  const end = new Date(endIso);
  const endOpts = { hour: 'numeric', minute: '2-digit' };
  return `${start.toLocaleString([], opts)} to ${end.toLocaleTimeString([], endOpts)}`;
}

function roomName(roomId) {
  const room = rooms.find((r) => r.id === roomId);
  return room ? room.name : `Room ${roomId}`;
}

async function loadRooms() {
  const response = await fetch('/api/rooms');
  rooms = await response.json();
  roomEl.innerHTML = rooms
    .map((r) => `<option value="${r.id}">${r.name} (holds ${r.capacity})</option>`)
    .join('');
}

async function loadBookings() {
  const response = await fetch('/api/bookings');
  const bookings = await response.json();
  if (bookings.length === 0) {
    listEl.innerHTML = '<li class="empty" data-empty>No bookings yet.</li>';
    return;
  }
  listEl.innerHTML = bookings
    .map(
      (b) => `
      <li data-booking-id="${b.id}">
        <span>
          <strong data-title>${b.title}</strong><br>
          <span class="when" data-when>${roomName(b.room_id)}, ${formatWhen(b.start, b.end)}</span>
        </span>
        <button type="button" data-delete="${b.id}">Cancel</button>
      </li>`
    )
    .join('');
}

listEl.addEventListener('click', async (event) => {
  const id = event.target.dataset.delete;
  if (!id) return;
  await fetch(`/api/bookings/${id}`, { method: 'DELETE' });
  await loadBookings();
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorEl.textContent = '';

  const payload = {
    room_id: Number(roomEl.value),
    title: document.getElementById('title').value,
    start: document.getElementById('start').value,
    end: document.getElementById('end').value,
    attendees: Number(document.getElementById('attendees').value)
  };

  const response = await fetch('/api/bookings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const body = await response.json();
    errorEl.textContent = body.error || 'Something went wrong.';
    return;
  }

  form.reset();
  document.getElementById('attendees').value = '1';
  await loadBookings();
});

(async function init() {
  await loadRooms();
  await loadBookings();
})();
