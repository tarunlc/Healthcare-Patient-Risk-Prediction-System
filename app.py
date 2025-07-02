import streamlit as st
import pandas as pd
import sqlite3
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Healthcare Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏥 Healthcare Analytics Dashboard")
st.markdown("---")

# Load model and database
@st.cache_resource
def load_model():
    try:
        return joblib.load('model.joblib')
    except:
        st.error("Model not found! Please run the training steps first.")
        return None

@st.cache_data
def load_sample_data():
    conn = sqlite3.connect('healthcare.db')
    df = pd.read_sql_query("SELECT * FROM patients LIMIT 100", conn)
    conn.close()
    return df

model = load_model()
sample_data = load_sample_data()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Patient Risk Prediction", "Data Explorer", "Analytics Dashboard"])
st.sidebar.markdown("---")
st.sidebar.info("💡 This dashboard analyzes patient readmission risk using ML")

if page == "Patient Risk Prediction":
    st.header("🎯 Patient Risk Prediction")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Enter Patient Information")
        encounter_id = st.number_input("Patient Encounter ID", value=2278392, min_value=0)

        # Manual input option
        st.subheader("Or Enter Details Manually")
        time_in_hospital = st.slider("Days in Hospital", 1, 14, 3)
        num_medications = st.slider("Number of Medications", 1, 81, 15)
        number_inpatient = st.slider("Previous Inpatient Visits", 0, 21, 0)

        use_manual = st.checkbox("Use manual input instead of patient ID")

    with col2:
        if st.button("🔍 Predict Risk", type="primary"):
            if model is None:
                st.error("Model not available!")
            else:
                try:
                    if use_manual:
                        # Use manual inputs
                        features = [[time_in_hospital, num_medications, number_inpatient]]
                        risk = model.predict_proba(features)[0][1] * 100

                        st.success("✅ Prediction Complete!")
                        st.metric("30-Day Readmission Risk", f"{risk:.1f}%")

                        # Risk level
                        if risk < 30:
                            st.info("🟢 Low Risk")
                        elif risk < 60:
                            st.warning("🟡 Medium Risk")
                        else:
                            st.error("🔴 High Risk")

                    else:
                        # Use patient ID
                        conn = sqlite3.connect('healthcare.db')
                        patient_df = pd.read_sql_query(
                            f"SELECT * FROM patients WHERE encounter_id = {encounter_id}",
                            conn
                        )
                        conn.close()

                        if patient_df.empty:
                            st.error("❌ Patient not found! Try another ID or use manual input.")
                        else:
                            # Prepare features
                            features_cols = ['time_in_hospital', 'num_medications', 'number_inpatient']
                            X = patient_df[features_cols].fillna(0)

                            # Predict
                            risk = model.predict_proba(X)[0][1] * 100

                            st.success("✅ Prediction Complete!")
                            st.metric("30-Day Readmission Risk", f"{risk:.1f}%")

                            # Show patient details
                            with st.expander("👤 Patient Details"):
                                st.dataframe(patient_df[['encounter_id', 'race', 'gender', 'age', 'time_in_hospital', 'num_medications']])

                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif page == "Data Explorer":
    st.header("🔍 Data Explorer")

    # Sample data view
    st.subheader("Sample Patient Data")
    st.dataframe(sample_data.head(10))

    # SQL Query interface
    st.subheader("Custom SQL Query")
    default_query = "SELECT age, gender, COUNT(*) as count FROM patients GROUP BY age, gender LIMIT 10"
    query = st.text_area("Enter your SQL query:", value=default_query, height=100)

    if st.button("Execute Query"):
        try:
            conn = sqlite3.connect('healthcare.db')
            result = pd.read_sql_query(query, conn)
            conn.close()

            st.success(f"✅ Query returned {len(result)} rows")
            st.dataframe(result)

        except Exception as e:
            st.error(f"❌ Query Error: {str(e)}")

else:  # Analytics Dashboard
    st.header("📊 Analytics Dashboard")

    try:
        conn = sqlite3.connect('healthcare.db')

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients", conn).iloc[0]['count']
        readmit_rate = pd.read_sql_query("SELECT AVG(readmitted = '<30')*100 as rate FROM patients", conn).iloc[0]['rate']
        avg_stay = pd.read_sql_query("SELECT AVG(time_in_hospital) as avg_stay FROM patients", conn).iloc[0]['avg_stay']
        avg_meds = pd.read_sql_query("SELECT AVG(num_medications) as avg_meds FROM patients", conn).iloc[0]['avg_meds']

        col1.metric("Total Patients", f"{total_patients:,}")
        col2.metric("Readmission Rate", f"{readmit_rate:.1f}%")
        col3.metric("Avg Hospital Stay", f"{avg_stay:.1f} days")
        col4.metric("Avg Medications", f"{avg_meds:.1f}")

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Readmission by Age Group")
            age_data = pd.read_sql_query("""
                SELECT age, AVG(readmitted = '<30')*100 as readmit_rate, COUNT(*) as count
                FROM patients
                GROUP BY age
                ORDER BY age
            """, conn)

            fig = px.bar(age_data, x='age', y='readmit_rate',
                        title="30-Day Readmission Rate by Age",
                        labels={'readmit_rate': 'Readmission Rate (%)', 'age': 'Age Group'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Gender Distribution")
            gender_data = pd.read_sql_query("""
                SELECT gender, COUNT(*) as count
                FROM patients
                GROUP BY gender
            """, conn)

            fig = px.pie(gender_data, values='count', names='gender',
                        title="Patient Distribution by Gender")
            st.plotly_chart(fig, use_container_width=True)

        # Hospital stay analysis
        st.subheader("Hospital Stay vs Medications")
        stay_med_data = pd.read_sql_query("""
            SELECT time_in_hospital, num_medications,
                   CASE WHEN readmitted = '<30' THEN 'Readmitted' ELSE 'Not Readmitted' END as status
            FROM patients
            WHERE time_in_hospital <= 14 AND num_medications <= 50
            LIMIT 500
        """, conn)

        fig = px.scatter(stay_med_data, x='time_in_hospital', y='num_medications',
                        color='status', title="Hospital Stay vs Number of Medications",
                        labels={'time_in_hospital': 'Days in Hospital', 'num_medications': 'Number of Medications'})
        st.plotly_chart(fig, use_container_width=True)

        conn.close()

    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")
