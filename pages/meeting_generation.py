import streamlit as st
import datetime
import random
from streamlit_calendar import calendar
from utils.meeting_utils import generate_meetings, meeting_types

def show():
    st.title("Meeting Generation")

    col1, col2 = st.columns(2)
    
    with col1:
        num_clients = st.slider("Number of Clients", 1, 20, 5)
        num_days = st.slider("Number of Days", 1, 30, 7)
        meetings_per_day = st.slider("Meetings per Day", 1, 50, 20)
    
    with col2:
        night_shift_ratio = st.slider("Night Shift Ratio", 0.0, 1.0, 0.2)
        day_start_hour = st.slider("Day Shift Start Hour", 0, 23, 8)
        day_end_hour = st.slider("Day Shift End Hour", day_start_hour + 1, 24, 20)
        night_start_hour = st.slider("Night Shift Start Hour", 0, 23, 20)
        night_end_hour = st.slider("Night Shift End Hour", night_start_hour + 1, 24, 6)

    if st.button("Generate Meetings"):
        start_date = datetime.date.today()
        events = generate_meetings(start_date, num_days, num_clients, meetings_per_day, night_shift_ratio,
                                   day_start_hour, day_end_hour, night_start_hour, night_end_hour)
        st.session_state.calendar_events = events
        st.success(f"Generated {len(events)} meetings.")

    if 'calendar_events' in st.session_state:
        st.subheader("Generated Meetings Calendar")
        calendar_options = {
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,timeGridDay",
            },
            "initialView": "timeGridWeek",
            "slotMinTime": f"{min(day_start_hour, night_start_hour):02d}:00:00",
            "slotMaxTime": f"{max(day_end_hour, night_end_hour):02d}:00:00",
            "expandRows": True,
            "height": "650px",
            "dayMaxEvents": True,
            "allDaySlot": False,
            "nowIndicator": True,
        }

        custom_css = """
            .fc-event-past { opacity: 0.8; }
            .fc-event-time { font-weight: bold; }
            .fc-event-title { font-style: italic; }
        """

        cal = calendar(events=st.session_state.calendar_events, options=calendar_options, custom_css=custom_css)
        st.write(cal)

        st.subheader("Meeting Types and Durations")
        for meeting_type, info in meeting_types.items():
            st.markdown(
                f'<span style="color:{info["color"]}">■</span> {meeting_type} ({info["duration"]} hour{"s" if info["duration"] > 1 else ""})',
                unsafe_allow_html=True)