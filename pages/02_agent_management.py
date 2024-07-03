import streamlit as st
import pandas as pd

# Initialize session state for agents if not exists
if 'agents' not in st.session_state:
    st.session_state.agents = pd.DataFrame(columns=['Name', 'Security', 'Fire', 'Maintenance'])

def agent_management_page():
    st.header("Agent Management")

    # Add new agent
    with st.form("new_agent"):
        st.subheader("Add New Agent")
        name = st.text_input("Name")
        security = st.checkbox("Security Certification")
        fire = st.checkbox("Fire Certification")
        maintenance = st.checkbox("Maintenance Certification")
        
        if st.form_submit_button("Add Agent"):
            new_agent = pd.DataFrame({
                'Name': [name],
                'Security': [security],
                'Fire': [fire],
                'Maintenance': [maintenance]
            })
            st.session_state.agents = pd.concat([st.session_state.agents, new_agent], ignore_index=True)
            st.success(f"Agent {name} added successfully!")

    # Display and edit agents
    st.subheader("Current Agents")
    for i, agent in st.session_state.agents.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])
        with col1:
            st.write(agent['Name'])
        with col2:
            security = st.checkbox("Security", value=agent['Security'], key=f"security_{i}")
        with col3:
            fire = st.checkbox("Fire", value=agent['Fire'], key=f"fire_{i}")
        with col4:
            maintenance = st.checkbox("Maintenance", value=agent['Maintenance'], key=f"maintenance_{i}")
        with col5:
            if st.button("Delete", key=f"delete_{i}"):
                st.session_state.agents = st.session_state.agents.drop(i).reset_index(drop=True)
                st.experimental_rerun()
        
        # Update agent information
        st.session_state.agents.at[i, 'Security'] = security
        st.session_state.agents.at[i, 'Fire'] = fire
        st.session_state.agents.at[i, 'Maintenance'] = maintenance

    # Display agent dataframe
    st.subheader("Agent Overview")
    st.dataframe(st.session_state.agents)