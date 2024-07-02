import streamlit as st
from streamlit_calendar import calendar

def show():
    st.title("Scheduling Results")

    if 'best_schedule' not in st.session_state:
        st.warning("No schedule has been generated yet. Please run the scheduling algorithm first.")
        return

    best_schedule = st.session_state.best_schedule

    st.subheader("Best Schedule")
    st.write(f"Fitness Score: {best_schedule.fitness}")

    events = []
    for meeting, agent in best_schedule.assignments.items():
        event = meeting.copy()  # Copy the original meeting data
        event['title'] = f"{event['title']} - {agent.name}"
        events.append(event)

    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        "initialView": "timeGridWeek",
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

    cal = calendar(events=events, options=calendar_options, custom_css=custom_css)
    st.write(cal)

    st.subheader("Schedule Details")
    for agent in best_schedule.agents:
        st.write(f"{agent.name}:")
        agent_meetings = [meeting for meeting, assigned_agent in best_schedule.assignments.items() if assigned_agent == agent]
        for meeting in agent_meetings:
            st.write(f"  - {meeting['title']} at {meeting['start']}")