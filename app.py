import streamlit as st
from streamlit_calendar import calendar
import datetime
import random

st.set_page_config(page_title="Streamlit Calendar Demo", layout="wide")
st.title("Streamlit Calendar Demo")

meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
    "Monitoring": {"color": "#99CCFF", "duration": 2}
}

def generate_meeting(date, client, is_night=False):
    if is_night:
        meeting_type = random.choice(["Security", "Monitoring"])
        start_time = datetime.time(hour=random.randint(20, 23))
    else:
        meeting_type = random.choice(list(meeting_types.keys()))
        start_time = datetime.time(hour=random.randint(8, 19))
    duration = datetime.timedelta(hours=meeting_types[meeting_type]["duration"])
    end_time = (datetime.datetime.combine(date, start_time) + duration).time()
    return {
        "title": f"Client {client}: {meeting_type}" + (" (Night)" if is_night else ""),
        "start": f"{date}T{start_time}",
        "end": f"{date}T{end_time}",
        "backgroundColor": meeting_types[meeting_type]["color"],
        "borderColor": meeting_types[meeting_type]["color"],
        "client": f"Client {client}",
        "type": meeting_type
    }

def generate_meetings(start_date, num_clients=5):
    events = []
    for client in range(1, num_clients + 1):
        for day in range(7):
            current_date = start_date + datetime.timedelta(days=day)
            for _ in range(random.randint(2, 3)):
                events.append(generate_meeting(current_date, client))
            if random.choice([True, False]):
                events.append(generate_meeting(current_date, client, is_night=True))
    return events

if 'calendar_events' not in st.session_state:
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    st.session_state.calendar_events = generate_meetings(start_of_week)

all_clients = sorted(set(event['client'] for event in st.session_state.calendar_events))
all_types = sorted(list(meeting_types.keys()))

col1, col2 = st.columns(2)
with col1:
    selected_clients = st.multiselect("Select Clients", all_clients, default=all_clients)
with col2:
    selected_types = st.multiselect("Select Appointment Types", all_types, default=all_types)

filtered_events = [
    event for event in st.session_state.calendar_events
    if event['client'] in selected_clients and event['type'] in selected_types
]

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

custom_css = """
    .fc-event-past { opacity: 0.8; }
    .fc-event-time { font-weight: bold; }
    .fc-event-title { font-style: italic; }
"""

cal = calendar(events=filtered_events, options=calendar_options, custom_css=custom_css)
st.write(cal)

st.subheader("Meeting Types and Durations")
for meeting_type, info in meeting_types.items():
    st.markdown(f'<span style="color:{info["color"]}">■</span> {meeting_type} ({info["duration"]} hour{"s" if info["duration"] > 1 else ""})', unsafe_allow_html=True)

if isinstance(cal, dict) and 'eventClick' in cal:
    event = cal['eventClick']['event']
    st.subheader("Selected Event")
    st.write(f"Title: {event['title']}")
    st.write(f"Start: {event['start']}")
    st.write(f"End: {event['end']}")

if st.button("Generate New Events"):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    st.session_state.calendar_events = generate_meetings(start_of_week)
    st.experimental_rerun()