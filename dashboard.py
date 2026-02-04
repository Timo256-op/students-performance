import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import os

from dataset_manager import DatasetManager
from analzer import Analyzer
from visualizer import Visualizer
from report_generator import ReportGenerator
from pdf_report_generator import PDFReportGenerator

# Streamlit page setup
st.set_page_config(page_title="Student Attendance Dashboard", layout="wide")

st.title("Student Attendance and Performance Dashboard")
st.markdown("Analyze and visualize how student attendance affects performance"
".")

# File uploader
uploaded_file = st.file_uploader("Upload Student Dataset (CSV format)", type=["csv"])

if uploaded_file:
    try:
        # Save uploaded CSV temporarily
        os.makedirs("data", exist_ok=True)
        temp_path = os.path.join("data", "uploaded_students.csv")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load and analyze data
        dataset = DatasetManager(temp_path)
        students = dataset.load_data()
    except ValueError as e:
        st.error(f" {str(e)}")
        st.info("Your CSV should have these columns: Student_ID, Name, Attendance, Average_Grade")
        # Show sample CSV format
        st.code("""
Sample CSV format:
Student_ID,Name,Attendance,Average_Grade
1,John Doe,85,92.5
2,Jane Smith,92,88.7
        """.strip())
        st.stop()  # Stop execution here

    analyzer = Analyzer(students)
    stats = analyzer.compute_statistics()

    # Display data
    st.subheader("Dataset Preview")
    st.dataframe(analyzer.df.head())

    st.subheader("Summary Statistics")
    st.json(stats)

    # Visualization
    visualizer = Visualizer(analyzer.df)
    visualizer.scatter_plot()
    visualizer.bar_chart()

    # Show plots inline
    st.subheader("Scatter Plot: Attendance vs Performance")
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=analyzer.df, x='Attendance', y='Average_Grade', hue='Attendance_Level', s=100, ax=ax1)
    plt.title("Attendance vs Performance")
    st.pyplot(fig1)

    st.subheader("Bar Chart: Average Grade by Attendance Category")
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    avg_grades = analyzer.df.groupby('Attendance_Level')['Average_Grade'].mean()
    sns.barplot(x=avg_grades.index, y=avg_grades.values, ax=ax2)
    plt.title("Average Grade by Attendance Level")
    st.pyplot(fig2)

    # Generate reports
    os.makedirs("reports", exist_ok=True)
    text_report = ReportGenerator(stats)
    text_path = text_report.generate()

    pdf_report = PDFReportGenerator(stats)
    pdf_path = pdf_report.generate_pdf()

    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        with open(text_path, "r") as f:
            st.download_button("Download Text Report", f.read(), "summary_report.txt", "text/plain")
    with col2:
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF Report", f.read(), "summary_report.pdf", "application/pdf")

    st.success(" Full analysis and PDF report generated successfully!")
else:
    st.info("Please upload a CSV file to begin analysis.")
