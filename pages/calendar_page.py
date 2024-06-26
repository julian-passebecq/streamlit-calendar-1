import streamlit as st
from streamlit_calendar import calendar
import datetime
import pandas as pd
from utils.meeting_utils import generate_meetings, meeting_types

def show():
    st.title("Calendar View")

    if 'calendar_events' not in st.session_state:
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        st.session_state.calendar_events = generate_meetings(start_of_week)

    # Rest of the calendar page code here (filters, calendar display, summary table)
    # ...

    if st.button("Generate New Events"):
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        st.session_state.calendar_events = generate_meetings(start_of_week)
        st.experimental_rerun()