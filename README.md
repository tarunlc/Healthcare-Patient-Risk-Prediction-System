# 🏥 Healthcare Patient Risk Prediction System

This project predicts the 30-day readmission risk for hospital patients using machine learning and provides an interactive dashboard for data exploration and analytics.

## 📌 Features

* ✅ **ML-Based Patient Readmission Prediction**
* 📊 **Interactive Dashboard** using Streamlit
* 🧮 **Custom SQL Queries** on patient data
* 📈 **Visual Analytics** (Readmission by age, gender distribution, etc.)
* 🔌 Hosted with **ngrok** for easy access

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install pandas scikit-learn plotly streamlit pyngrok
```

### 2. Download & Extract Dataset

```bash
wget https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip
unzip diabetes+130-us+hospitals+for+years+1999-2008.zip
```

---

## 📦 Project Structure

* `diabetic_data.csv` — Dataset from UCI
* `healthcare.db` — SQLite database created from the dataset
* `model.joblib` — Trained Random Forest classifier
* `app.py` — Streamlit dashboard (embedded in script)
* `healthcare_patient_risk_prediction_system.py` — Main script with all steps combined

---

## 🧠 ML Model

* **Model**: Random Forest Classifier
* **Target**: Predict if a patient is readmitted within 30 days
* **Features**:

  * `time_in_hospital`
  * `num_medications`
  * `number_inpatient`

---

## 🚀 Running the Project

```bash
python healthcare_patient_risk_prediction_system.py
```

This will:

* Create the database
* Train the model
* Launch the Streamlit app on port `8501`
* Share a public URL using `ngrok`

---

## 🌐 Accessing the Dashboard

After execution, look for the printed URL like:

```
🔗 Access your dashboard here: https://<your-ngrok-url>.ngrok.io
```

Open it in your browser to explore the app!

---

## 📋 Dashboard Pages

1. **Patient Risk Prediction**

   * Predict risk using patient ID or manual input
2. **Data Explorer**

   * Run custom SQL queries on the dataset
3. **Analytics Dashboard**

   * View charts for readmission rates, demographics, etc.

---

## 📁 Notes

* Keep the main script running to maintain access to the Streamlit app.
* Ensure port `8501` is available before launching.

---

## 📚 Dataset Source

[UCI ML Repository - Diabetes 130-US hospitals](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008)

---


