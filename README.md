# Room Booking: QA Exercise

Thanks for taking the time to do this. Here is what it is and what it is not.

This is a **fictional conference room booking app** we built for interviews. It is
not our product, we do not use any part of it, and nothing you write here goes
anywhere. You are not doing work for us. You are looking at a codebase we broke
on purpose.

## The scenario

An engineer just finished building this. The test suite is green. They are ready
to ship it.

**Your job is to decide whether you would ship it.**

## Time box

**Spend 90 minutes. Please stop when the timer goes off.**

We mean this. We would much rather watch an honest 90 minutes where you got
halfway than a polished three-hour session. We are evaluating how you think, not
how much you can finish, and a submission that clearly ran long counts against
you rather than for you.

## Recording

Record your screen with audio for the whole session. Loom, QuickTime, OBS, or
whatever you already use is fine.

**Talk through what you are doing and why.** A silent recording of someone
reading code tells us nothing. We want to hear your reasoning, particularly
every time you decide something is or is not trustworthy. Thinking out loud
while you are unsure is exactly what we want to hear. So is changing your mind.

**Close the recording by telling us whether you would ship this and why.** If
your answer is no, tell us what would have to change first.

Send us the recording link when you are done.

## Use your own tools

Use whatever you normally use, including AI. Claude Code, Cursor, Copilot,
whatever your setup is. We are genuinely interested in how you work, so please
do not perform a version of yourself that avoids the tools you would reach for
on a Tuesday. Narrate what you ask them and what you make of the answers.

## Running it

You need Python 3.12+ and Node 20+.

```bash
# API
uv venv
uv pip install -e ".[dev]"
uv run uvicorn app.main:api --port 8000 --reload

# API tests, in a second terminal
uv run pytest

# UI tests, with the server running
npm install
npx cypress install   # npm 11 skips Cypress's own installer
npx cypress run       # or: npx cypress open
```

The app is at http://localhost:8000. Everything is stored in memory, so
restarting the server wipes all bookings. There is also a `POST /api/reset`
endpoint if you want to clear state without restarting.

## What is in here

| Path | What it is |
|---|---|
| `app/` | FastAPI service plus a small vanilla JS front end |
| `app/store.py` | Booking rules live here |
| `tests/test_api.py` | API tests (pytest) |
| `cypress/e2e/booking.cy.ts` | UI tests (Cypress + TypeScript) |

## The rules the app is supposed to enforce

1. A booking must end after it starts.
2. A booking needs at least one attendee.
3. Attendees cannot exceed the room's capacity.
4. A room cannot be double booked. Two bookings overlap if they share any
   time. Back to back bookings are fine: one ending at 10:00 and the next
   starting at 10:00 do not overlap.
5. These rules apply whenever a booking is created **or changed**.

## What we are looking for

How you decide whether a test suite is telling you the truth. That is the whole
exercise. Everything else is scaffolding.

## Questions

Reply to whoever sent you this. If something will not run, tell us and we will
sort it out. Do not spend your 90 minutes fighting an install.
