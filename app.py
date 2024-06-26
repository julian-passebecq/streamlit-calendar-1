import streamlit as st
from streamlit_calendar import calendar
import datetime
import random

st.set_page_config(page_title="Streamlit Calendar Demo", layout="wide")

st.title("Streamlit Calendar Demo")

# Define meeting types and their colors
meeting_types = {
    "Maintenance": "#FF9999",
    "FireTest": "#FFCC99",
    "Security": "#99FF99",
    "Monitoring": "#99CCFF"
}

def generate_meeting(date, client, is_night=False):
    if is_night:
        meeting_type = random.choice(["Security", "Monitoring"])
        start_time = datetime.time(hour=random.randint(20, 23))
    else:
        meeting_type = random.choice(list(meeting_types.keys()))
        start_time = datetime.time(hour=random.randint(8, 19))

    duration = datetime.timedelta(hours=random.randint(1, 3))
    end_time = (datetime.datetime.combine(date, start_time) + duration).time()

    return {
        "title": f"Client {client}: {meeting_type}" + (" (Night)" if is_night else ""),
        "start": f"{date}T{start_time}",
        "end": f"{date}T{end_time}",
        "backgroundColor": meeting_types[meeting_type],
        "borderColor": meeting_types[meeting_type],
    }

def generate_meetings(start_date, num_clients=5):
    events = []
    for client in range(1, num_clients + 1):
        for day in range(7):
            current_date = start_date + datetime.timedelta(days=day)

            # Day meetings (2-3 per day)
            for _ in range(random.randint(2, 3)):
                events.append(generate_meeting(current_date, client))

            # Night meeting (0 or 1 per day)
            if random.choice([True, False]):
                events.append(generate_meeting(current_date, client, is_night=True))

    return events

# Use session state to store and retrieve calendar events
if 'calendar_events' not in st.session_state:
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    st.session_state.calendar_events = generate_meetings(start_of_week)

# Define calendar options
calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "initialView": "timeGridWeek",
    "slotMinTime": "06:00:00",
    "slotMaxTime": "23:59:00",
    "expandRows": True,
    "height": "650px",
    "dayMaxEvents": True,
    "allDaySlot": False,
}

# Custom CSS for the calendar
custom_css = """
    .fc-event-past { opacity: 0.8; }
    .fc-event-time { font-weight: bold; }
    .fc-event-title { font-style: italic; }
"""

# Display the calendar
cal = calendar(events=st.session_state.calendar_events, options=calendar_options, custom_css=custom_css)
st.write(cal)

# Display legend
st.subheader("Meeting Types")
for meeting_type, color in meeting_types.items():
    st.markdown(f'<span style="color:{color}">■</span> {meeting_type}', unsafe_allow_html=True)

# Display selected event information
if isinstance(cal, dict) and 'eventClick' in cal:
    event = cal['eventClick']['event']
    st.subheader("Selected Event")
    st.write(f"Title: {event['title']}")
    st.write(f"Start: {event['start']}")
    st.write(f"End: {event['end']}")

# Add a button to regenerate events
if st.button("Generate New Events"):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    st.session_state.calendar_events = generate_meetings(start_of_week)
    st.experimental_rerun()