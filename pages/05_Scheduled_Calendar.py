import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import datetime
from utils.meeting_utils import meeting_types

st.title("Scheduled Calendar")

if 'best_schedule' not in st.session_state:
    st.warning("No schedule has been generated yet. Please run the genetic algorithm first.")
    st.stop()

best_schedule = st.session_state.best_schedule

# Sidebar for calendar settings
st.sidebar.title("Calendar Settings")
show_unassigned = st.sidebar.checkbox("Show Unassigned Meetings", value=True)
show_issues = st.sidebar.checkbox("Highlight Issues", value=True)

# Generate calendar events from the best schedule
events = []
start_date = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
for meeting, agent in best_schedule.assignments.items():
    event_date = meeting.start.date()
    start_time = meeting.start.time()
    end_time = (meeting.start + datetime.timedelta(hours=meeting.duration)).time()
    
    # Check for issues
    has_issue = False
    if show_issues:
        if meeting.required_skill not in agent.skills and meeting.required_skill != 'Monitoring':
            has_issue = True
        # Add more issue checks here (e.g., overlapping, consecutive meetings, etc.)

    event_color = meeting_types[meeting.required_skill]["color"]
    if has_issue:
        event_color = "red"
    elif not agent:
        event_color = "gray"

    events.append({
        "title": f"Agent {agent.id if agent else 'Unassigned'}: {meeting.required_skill}",
        "start": f"{event_date}T{start_time}",
        "end": f"{event_date}T{end_time}",
        "backgroundColor": event_color,
        "borderColor": event_color,
        "textColor": "white" if has_issue else "black"
    })

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

cal = calendar(events=events, options=calendar_options, custom_css=custom_css)
st.write(cal)

st.subheader("Legend")
st.write("Green: Meeting assigned without issues")
st.write("Red: Meeting with issues (wrong skill, overlapping, etc.)")
st.write("Gray: Unassigned meeting")

# Summary Table
st.subheader("Summary Table")

summary_data = []
for day in range(7):
    current_date = start_date + datetime.timedelta(days=day)
    day_events = [event for event in events if
                  datetime.datetime.fromisoformat(event['start']).date() == current_date]

    total_meetings = len(day_events)
    assigned_meetings = sum(1 for event in day_events if "Unassigned" not in event['title'])
    issues = sum(1 for event in day_events if event['backgroundColor'] == "red")

    summary_data.append({
        "Date": current_date.strftime("%Y-%m-%d"),
        "Total Meetings": total_meetings,
        "Assigned Meetings": assigned_meetings,
        "Unassigned Meetings": total_meetings - assigned_meetings,
        "Meetings with Issues": issues
    })

summary_df = pd.DataFrame(summary_data)
st.table(summary_df)