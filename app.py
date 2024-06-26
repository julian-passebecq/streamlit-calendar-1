import streamlit as st
from streamlit_calendar import calendar
import datetime
import random
import pandas as pd

st.set_page_config(page_title="Scheduling App", layout="wide")

# Define meeting types and their properties
meeting_types = {
    "Maintenance": {"color": "#FF9999", "duration": 1},
    "FireTest": {"color": "#FFCC99", "duration": 2},
    "Security": {"color": "#99FF99", "duration": 3},
        "Monitoring": {"color": "#99CCFF", "duration": 2}
    }

    # Helper functions (keep the existing generate_meeting and generate_meetings functions here)

    def generate_meeting(date, client, is_night=False):
        if is_night:
            meeting_type = random.choice(["Security", "Monitoring"])
            start_hour = random.randint(20, 23) if meeting_type == "Security" else random.randint(22, 23)
        else:
            meeting_type = random.choice(["Maintenance", "FireTest", "Security"])
            start_hour = random.randint(8, 19)

        start_time = datetime.time(hour=start_hour)
        duration = datetime.timedelta(hours=meeting_types[meeting_type]["duration"])
        end_time = (datetime.datetime.combine(date, start_time) + duration).time()

        return {
            "title": f"Client {client}: {meeting_type}" + (" (Night)" if is_night else ""),
            "start": f"{date}T{start_time}",
            "end": f"{date}T{end_time}",
            "backgroundColor": meeting_types[meeting_type]["color"],
            "borderColor": meeting_types[meeting_type]["color"],
            "client": f"Client {client}",
            "type": meeting_type,
            "is_night": is_night
        }

    def generate_meetings(start_date, num_clients=5):
        events = []
        for client in range(1, num_clients + 1):
            for day in range(7):
                current_date = start_date + datetime.timedelta(days=day)
                for _ in range(random.randint(2, 3)):
                    events.append(generate_meeting(current_date, client, is_night=False))
                if random.choice([True, False]):
                    events.append(generate_meeting(current_date, client, is_night=True))
        return events

    # Page functions
    def calendar_page():
        st.title("Calendar View")

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
            st.markdown(f'<span style="color:{info["color"]}">■</span> {meeting_type} ({info["duration"]} hour{"s" if info["duration"] > 1 else ""})', unsafe_allow_html=True)

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
            day_events = [event for event in filtered_events if datetime.datetime.fromisoformat(event['start']).date() == current_date]

            total_hours = sum(meeting_types[event['type']]['duration'] for event in day_events)
            required_agents = len(day_events)
            night_appointments = sum(1 for event in day_events if event['is_night'] or int(event['start'].split('T')[1].split(':')[0]) >= 20)
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

        if st.button("Generate New Events"):
            today = datetime.date.today()
            start_of_week = today - datetime.timedelta(days=today.weekday())
            st.session_state.calendar_events = generate_meetings(start_of_week)
            st.experimental_rerun()

    def genetic_algorithm_page():
        st.title("Genetic Algorithm Scheduling")
        st.write("This page will contain the genetic algorithm implementation for scheduling agents.")
        # We'll implement this page in the next step

    def results_page():
        st.title("Scheduling Results")
        st.write("This page will display the results of the genetic algorithm scheduling.")
        # We'll implement this page after completing the genetic algorithm

    # Main app logic
    def main():
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Calendar", "Genetic Algorithm", "Results"])

        if page == "Calendar":
            calendar_page()
        elif page == "Genetic Algorithm":
            genetic_algorithm_page()
        elif page == "Results":
            results_page()

    if __name__ == "__main__":
        main()