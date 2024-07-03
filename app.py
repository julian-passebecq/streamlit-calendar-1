import streamlit as st
from streamlit_calendar import calendar
import datetime
import pandas as pd
from utils.meeting_utils import generate_meetings, meeting_types

st.set_page_config(page_title="Scheduling App", layout="wide")

def show_calendar_page():
    st.title("Calendar View")

    # Add slicing options
    st.sidebar.subheader("Calendar Generation Options")
    num_clients = st.sidebar.slider("Number of Clients", 1, 10, 5)
    start_date = st.sidebar.date_input("Start Date", datetime.date.today())
    date_range = st.sidebar.slider("Date Range (days)", 1, 14, 7)
    num_night_shifts = st.sidebar.slider("Number of Night Shifts", 0, 10, 2)
    num_day_shifts = st.sidebar.slider("Number of Day Shifts", 0, 10, 3)
    shift_duration = st.sidebar.slider("Duration of Shifts (hours)", 1, 12, 2)
    night_start_time = st.sidebar.slider("Starting Time of Night Shifts", 18, 23, 20)

    if 'calendar_events' not in st.session_state:
        st.session_state.calendar_events = []

    if st.sidebar.button("Generate New Events"):
        st.session_state.calendar_events = generate_meetings(
            start_date, num_clients, date_range, num_night_shifts, num_day_shifts, shift_duration, night_start_time
        )

    if not st.session_state.calendar_events:
        st.info("No events generated yet. Adjust the options and click 'Generate New Events'.")

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
            "Day Appointments (6AM-8PM)": day_appointments,
            "Night Appointments (After 8PM)": night_appointments
        })

    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

def main():
    show_calendar_page()

if __name__ == "__main__":
    main()
