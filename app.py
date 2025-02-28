import streamlit as st
import pandas as pd
import plotly.express as px


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
    
    # Grade Classification
    def classify_grade(avg):
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"

    grades = [classify_grade(avg) for avg in averages]

    # Create DataFrame
    df = pd.DataFrame({
        "Name": [s["Name"] for s in students],
        "Average Grade (%)": [f"{avg:.2f}%" for avg in averages],
        "Grade": grades
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

    # Grade Distribution Chart (Using Plotly)
    st.markdown("<h2 style='color: #9B59B6;'>📊 Grade Distribution</h2>", unsafe_allow_html=True)
    
    # Prepare data for Plotly
    df_plotly = df.copy()
    df_plotly["Average Grade (%)"] = df_plotly["Average Grade (%)"].str.replace('%', '').astype(float)
    
    # Create a beautiful bar chart with Plotly
    fig = px.bar(
        df_plotly,
        x="Name",
        y="Average Grade (%)",
        color="Grade",
        text="Average Grade (%)",
        title="Student Grade Distribution",
        labels={"Average Grade (%)": "Average Grade (%)", "Name": "Student Name"},
        color_discrete_sequence=px.colors.qualitative.Pastel,  # Use a pastel color palette
    )
    
    # Customize hover text
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Average Grade: %{y:.2f}%<br>Grade: %{marker.color}"
    )
    
    # Customize layout
    fig.update_layout(
        xaxis_title="Student Name",
        yaxis_title="Average Grade (%)",
        template="plotly_white",  # Use a clean white theme
        showlegend=True,
        hovermode="x unified",
    )
    
    # Display the Plotly chart
    st.plotly_chart(fig, use_container_width=True)

    # Subject-wise Analysis
    st.markdown("<h2 style='color: #3498DB;'>📚 Subject-wise Analysis</h2>", unsafe_allow_html=True)
    subject_analysis = pd.DataFrame({
        "Subject": [f"Subject {j+1}" for j in range(num_subjects)],
        **{s["Name"]: s["Scores"] for s in students}
    })
    st.dataframe(subject_analysis)

    # Downloadable Report
    st.markdown("<h2 style='color: #F39C12;'>📥 Download Report</h2>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='student_grades.csv',
        mime='text/csv',
    )

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #7F8C8D;'>© 2023 Grade Calculator. All rights reserved.</p>", unsafe_allow_html=True)