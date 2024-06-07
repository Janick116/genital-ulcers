import streamlit as st
from datetime import datetime

def decision_tree():
    st.set_page_config(page_title="STI Management Decision Tree", layout='wide')
    st.title("Initial Evaluation of New Genital Ulcers in Sexually Active Patients")
    st.caption("Follow the questionnaire to guide the management of genital ulcers.")
    st.markdown("---")

    # Initialize state management
    if 'page' not in st.session_state:
        st.session_state['page'] = 'intro'  # Start at the introduction step

    def navigate_page(page):
        st.session_state['page'] = page

    # Function to reset the decision tree
    def reset_tree():
        st.session_state['page'] = 'intro'

    # Introduction page for demographics
    if st.session_state['page'] == 'intro':
        with st.form("patient_info"):
            st.subheader("Patient Details")
            name = st.text_input("Name", key='name_input')
            birth_date = st.date_input("Birth Date", min_value=datetime(1900, 1, 1), max_value=datetime.today(), key='birth_date_input')
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key='gender_select')
            submit = st.form_submit_button("Submit")

            if submit:
                st.session_state['patient_name'] = name
                st.session_state['birth_date'] = birth_date
                st.session_state['gender'] = gender
                navigate_page('B')

    # PAGE B
    if st.session_state['page'] == 'B':
        st.subheader("Known Exposure")
        sti_exposure = st.radio(
            "Has the patient had a known exposure to an STI that causes genital ulcers in the last 90 days?",
            ('Herpes', 'Syphilis', 'Chlamydia', 'Chancroid', 'No STI contact'), key='sti_exposure')
        
        if st.button('Confirm Exposure', key='confirm_exposure_btn'):
            if sti_exposure == 'No STI contact':
                navigate_page('D')
            elif sti_exposure == 'Herpes':
                navigate_page('F')
            elif sti_exposure == 'Syphilis':
                navigate_page('L')
            elif sti_exposure == 'Chlamydia':
                navigate_page('N')
            elif sti_exposure == 'Chancroid':
                navigate_page('G')

    # PAGE C
    elif st.session_state['page'] == 'C':
        st.info("Initiate empiric treatment for that disease and await further testing.")
        st.table({
            "Medication": ["Acyclovir", "Famciclovir", "Valacyclovir"],
            "Dosage": ["400 mg three times daily", "250 mg three times daily", "1000 mg twice daily"],
            "Duration": ["7-10 days for primary infection", "7-10 days for primary infection", "7-10 days for primary infection"],
            "Notes": ["Primary infection treatment", "Primary infection treatment", "Primary infection treatment"]
        })
        if st.button('Reset', key='reset_in_c'):
            reset_tree()

    # PAGE D
    elif st.session_state['page'] == 'D':
        painful_ulcers = st.radio("Are there any painful ulcers?", ('Yes', 'No'), key='painful_ulcers')
        if st.button('Confirm Pain Status', key='confirm_pain_status'):
            navigate_page('E' if painful_ulcers == 'Yes' else 'I')

    # PAGE E
    elif st.session_state['page'] == 'E':
        herpes_consistent = st.radio(
            "Is the appearance consistent with Herpes simplex virus (HSV)?",
            ('Yes', 'No'), key='herpes_consistent')

        st.info("""
        **Clinical Appearance of Herpes Ulcers:**
        - **PAINFUL ULCERS (common symptom).**
        - **Grouped Vesicles:** These appear on an erythematous base.
        - **Shallow Ulcerations:** Typical presentation.
        - **Large, Crusted Erosions:** Can occur in immunosuppressed patients.
        """)
        
        if st.button('Confirm HSV Consistency', key='confirm_hsv_consistency'):
            navigate_page('F' if herpes_consistent == 'Yes' else 'G')

    # PAGE F
    elif st.session_state['page'] == 'F':
        st.subheader("Recommended Treatment Options for Herpes")
        st.table({
            "Medication": ["Acyclovir", "Famciclovir", "Valacyclovir"],
            "Dosage": ["400 mg three times daily", "250 mg three times daily", "1000 mg twice daily"],
            "Duration": ["7-10 days for primary infection", "7-10 days for primary infection", "7-10 days for primary infection"],
            "Notes": ["Primary infection treatment", "Primary infection treatment", "Primary infection treatment"]
        })
        st.write("Options for recurrent disease include: Chronic suppression, Episodic therapy, or no intervention.")
        if st.button('Proceed to Further Evaluation'):
            navigate_page('H')

    # PAGE G
    elif st.session_state['page'] == 'G':
        st.info("Consider alternative diagnosis (e.g., syphilis, chancroid). Administer empiric treatment if risk factors are present.")
        if st.button('Proceed to Further Evaluation'):
            navigate_page('H')

    # PAGE H
    elif st.session_state['page'] == 'H':
        st.subheader("Further Evaluation")
        st.write("further evaluation is needed.")
        if st.button('Reset'):
            reset_tree()
    
    # PAGE I
    elif st.session_state['page'] == 'I':
        rapid_syphilis = st.radio("Is rapid syphilis testing available?", ('Yes', 'No'), key='rapid_syphilis')
        if st.button('Confirm Rapid Test Availability'):
            navigate_page('J' if rapid_syphilis == 'Yes' else 'K')

    # PAGE J
    elif st.session_state['page'] == 'J':
        syphilis_positive = st.radio("Is testing positive for syphilis?", ('Yes', 'No'), key='syphilis_positive')
        if st.button('Confirm Syphilis Test Result'):
            navigate_page('L' if syphilis_positive == 'Yes' else 'M')

    # PAGE K
    elif st.session_state['page'] == 'K':
        high_risk_syphilis = st.radio("Is the patient at high risk for syphilis?", ('Yes', 'No'), key='high_risk_syphilis')
        if st.button('Confirm High Risk Status'):
            navigate_page('P' if high_risk_syphilis == 'Yes' else 'Q')

    # PAGE L
    elif st.session_state['page'] == 'L':
        st.subheader("Syphilis Treatment")
        st.table({
            "Medication": ["Penicillin G benzathine"],
            "Dosage": ["2.4 million units IM"],
            "Duration": ["Single dose"],
            "Notes": ["Primary syphilis treatment"]
        })
        if st.button('Treatment Complete, Reset Decision Tree'):
            reset_tree()

    # PAGE M
    elif st.session_state['page'] == 'M':
        lgv_risk = st.radio("Has patient or sexual partner lived or traveled to an LGV-endemic area OR does patient have painful lymphadenopathy present?", ('Yes', 'No'), key='lgv_risk')
        if st.button('Confirm LGV Risk'):
            navigate_page('N' if lgv_risk == 'Yes' else 'O')

    # PAGE N
    elif st.session_state['page'] == 'N':
        st.subheader("Lymphogranuloma Venereum (LGV) Testing and Treatment")
        st.write("Testing for LGV is recommended. Administer empiric treatment while awaiting results.")
        st.table({
            "Medication": ["Doxycycline"],
            "Dosage": ["100 mg twice daily"],
            "Duration": ["21 days"],
            "Notes": ["LGV treatment"]
        })
        if st.button('Further Evaluation Required, Reset Decision Tree'):
            reset_tree()

    # PAGE O
    elif st.session_state['page'] == 'O':
        st.subheader("Further Evaluation Needed")
        st.write("If the initial tests are negative and/or there is no response to therapy, further evaluation is needed, including evaluation for non-STI causes.")
        if st.button('Reset Decision Tree'):
            reset_tree()

    # PAGE P
    elif st.session_state['page'] == 'P':
        st.subheader("Empiric Treatment for Syphilis")
        st.write("Treat empirically for syphilis while awaiting further results.")
        if st.button('Proceed to Evaluate LGV Risk'):
            navigate_page('M')

    # PAGE Q
    elif st.session_state['page'] == 'Q':
        st.subheader("Further Evaluation for Non-STI Causes")
        st.write("If the initial tests are negative, further evaluation is needed, including evaluation for non-STI causes.")
        if st.button('Reset Decision Tree'):
            reset_tree()

    # General reset button shown at each step for convenience
    if st.session_state['page'] != 'intro' and not st.session_state['page'] in ['C', 'F']:
        if st.button('Reset', key=f'reset_{st.session_state["page"]}'):
            reset_tree()

if __name__ == '__main__':
    decision_tree()



