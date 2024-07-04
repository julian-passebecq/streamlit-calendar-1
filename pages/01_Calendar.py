import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import datetime
from utils.meeting_utils import generate_meetings, meeting_types

st.title("Meeting Generation Calendar")

# Sidebar for calendar settings
st.sidebar.title("Calendar Settings")
num_clients = st.sidebar.number_input("Number of Clients", min_value=1, max_value=20, value=5)

# Meeting duration settings
st.sidebar.subheader("Meeting Durations (hours)")
for meeting_type in meeting_types:
    meeting_types[meeting_type]["duration"] = st.sidebar.slider(
        f"{meeting_type} duration",
        min_value=1.0,
        max_value=3.0,
        value=float(meeting_types[meeting_type]["duration"]),
        step=0.5
    )

# Workload percentage
workload_percentage = st.sidebar.slider("Workload Percentage", 50, 150, 100, 5)

col1, col2 = st.sidebar.columns(2)
with col1:
    day_shift_1_start = st.time_input("Day Shift 1 Start", datetime.time(7, 0))
    day_shift_1_end = st.time_input("Day Shift 1 End", datetime.time(16, 0))
with col2:
    day_shift_2_start = st.time_input("Day Shift 2 Start", datetime.time(13, 0))
    day_shift_2_end = st.time_input("Day Shift 2 End", datetime.time(22, 0))

night_shift_start = st.sidebar.time_input("Night Shift Start", datetime.time(22, 0))
night_shift_end = st.sidebar.time_input("Night Shift End", datetime.time(7, 0))

if 'agents' not in st.session_state:
    st.warning("Please configure agents in the Agent Configuration page first.")
    st.stop()

num_agents = len(st.session_state.agents)
total_agent_hours = num_agents * 8 * 5  # 8 hours per day, 5 days a week
adjusted_hours = total_agent_hours * (workload_percentage / 100)

if 'calendar_events' not in st.session_state or st.button("Generate New Calendar"):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    st.session_state.calendar_events = generate_meetings(
        start_of_week, num_clients, adjusted_hours,
        day_shift_1_start, day_shift_1_end,
        day_shift_2_start, day_shift_2_end,
        night_shift_start, night_shift_end,
        meeting_types
    )

all_clients = sorted(set(event['client'] for event in st.session_state.calendar_events))
all_types = sorted(list(meeting_types.keys()))

selected_clients = st.multiselect("Select Clients", all_clients, default=all_clients)
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
    "slotMaxTime": "30:00:00",  # 6:00 AM next day
    "expandRows": True,
    "height": "650px",
    "dayMaxEvents": True,
    "allDaySlot": False,
    "scrollTime": "08:00:00",  # Start scrolled to 8:00 AM
    "nowIndicator": True,
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
    st.markdown(
        f'<span style="color:{info["color"]}">■</span> {meeting_type} ({info["duration"]} hour{"s" if info["duration"] > 1 else ""})',
        unsafe_allow_html=True)

if isinstance(cal, dict) and 'eventClick' in cal:
    event = cal['eventClick']['event']
    st.subheader("Selected Event")
    st.write(f"Title: {event['title']}")
    st.write(f"Start: {event['start']}")
    st.write(f"End: {event['end']}")

# Summary Table
st.subheader("Summary Table")

summary_data = []
start_date = min(datetime.datetime.fromisoformat(event['start']).date() for event in filtered_events)

for day in range(7):
    current_date = start_date + datetime.timedelta(days=day)
    day_events = [event for event in filtered_events if
                  datetime.datetime.fromisoformat(event['start']).date() == current_date]

    total_hours = sum(meeting_types[event['type']]['duration'] for event in day_events)
    required_agents = len(day_events)
    night_appointments = sum(
        1 for event in day_events if event['is_night'] or int(event['start'].split('T')[1].split(':')[0]) >= 20)
    day_appointments = required_agents - night_appointments

    summary_data.append({
        "Date": current_date.strftime("%Y-%m-%d"),
        "Total Hours": total_hours,
        "Required Agents": required_agents,
        "Day Appointments": day_appointments,
        "Night Appointments": night_appointments
    })

summary_df = pd.DataFrame(summary_data)
st.table(summary_df)