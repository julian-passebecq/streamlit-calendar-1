import streamlit as st
from streamlit_calendar import calendar
import datetime

st.set_page_config(page_title="Streamlit Calendar Demo", layout="wide")

st.title("Streamlit Calendar Demo")

# Define calendar events
calendar_events = [
    {
        "title": "Event 1",
        "start": f"{datetime.date.today()}T09:00:00",
        "end": f"{datetime.date.today()}T10:00:00",
    },
    {
        "title": "Event 2",
        "start": f"{datetime.date.today() + datetime.timedelta(days=1)}T14:00:00",
        "end": f"{datetime.date.today() + datetime.timedelta(days=1)}T16:00:00",
    },
    {
        "title": "Event 3",
        "start": f"{datetime.date.today() + datetime.timedelta(days=2)}T11:00:00",
        "end": f"{datetime.date.today() + datetime.timedelta(days=2)}T12:30:00",
    },
]

# Define calendar options
calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "initialView": "dayGridMonth",
    "selectable": True,
    "selectMirror": True,
    "dayMaxEvents": True,
    "weekends": True,
    "expandRows": True,
    "showNonCurrentDates": True,
    "height": "650px",
}

# Custom CSS for the calendar
custom_css = """
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: bold;
    }
    .fc-toolbar-title {
        color: #0f52ba;
    }
"""

# Display the calendar
calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
st.write(calendar)

# Display the selected date range
if calendar['events']:
    st.write(f"Selected date range: {calendar['events'][0]} to {calendar['events'][1]}")