import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Grade Calculator", layout="wide")

# Custom Title
st.markdown("<h1 style='text-align: center; color: #FF5733;'>📚 Student Grade Calculator</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for Inputs
st.sidebar.header("Settings")
num_students = st.sidebar.number_input("Number of Students", min_value=1, value=1)
num_subjects = st.sidebar.number_input("Number of Subjects", min_value=1, value=1)

# Input Fields for Student Names and Scores
students = []
for i in range(num_students):
    st.subheader(f"👨‍🎓 Student {i+1}")
    name = st.text_input(f"Name of Student {i+1}", key=f"name_{i}")
    scores = [st.number_input(f"Score {j+1}", min_value=0, max_value=100, value=0, key=f"score_{i}_{j}") 
              for j in range(num_subjects)]
    students.append({"Name": name, "Scores": scores})

# Calculate Grades
if st.button("📊 Calculate Grades"):
    # Calculate average grades
    averages = [sum(s["Scores"]) / num_subjects for s in students]
    
    # Create DataFrame
    df = pd.DataFrame({
        "Name": [s["Name"] for s in students],
        "Average Grade (%)": [f"{avg:.2f}%" for avg in averages]
    })

    # Identify Top Performer
    max_grade = max(averages)
    df["Top Performer"] = [avg == max_grade for avg in averages]

    # Display Results
    st.markdown("<h2 style='color: #2ECC71;'>🎓 Student Grades</h2>", unsafe_allow_html=True)
    st.dataframe(df.style.applymap(lambda x: "background-color: lightgreen" if x else "", subset=["Top Performer"]))

    # Top Performer Section
    st.markdown("<h2 style='color: #E74C3C;'>🏆 Top Performer</h2>", unsafe_allow_html=True)
    st.dataframe(df[df["Top Performer"]])

    # Grade Distribution Chart
    st.markdown("<h2 style='color: #9B59B6;'>📊 Grade Distribution</h2>", unsafe_allow_html=True)
    st.bar_chart(df.set_index("Name")["Average Grade (%)"].str.replace('%', '').astype(float))