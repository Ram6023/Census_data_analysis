import streamlit as st
import pandas as pd

st.set_page_config(page_title="Census Data Analysis", layout="wide")

st.title("📊 Census Data Analysis By Sriram Vissakoti")

# Upload file
uploaded_file = st.file_uploader("📂 Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Define column names manually
    column_names = [
        'Age', 'Education', 'Marital_Status', 'Gender',
        'Occupation', 'Income', 'Parents_Present',
        'Country', 'Native', 'Weeks_Worked'
    ]

    # Read CSV without header and apply column names
    census_data = pd.read_csv(uploaded_file, names=column_names, header=None)

    st.success("✅ File uploaded successfully!")

    st.subheader("🔍 Data Preview")
    st.dataframe(census_data.head())

    # Dropdown to select report
    report_options = [
        "Select Report",
        "Education Distribution",
        "College Dropouts",
        "Senior Citizens (55-60)",
        "Employable Widows & Divorced",
        "Gender-wise Total Income",
        "Total Tax (by Gender)",
        "Non-Citizens Working %",
        "Orphans by Parents Category & Gender",
        "Education Category & Gender Count"
    ]

    selected_report = st.selectbox("📑 Choose a report to generate:", report_options)

    # ---- Education Distribution ----
    if selected_report == "Education Distribution":
        if 'Education' in census_data.columns:
            edu_counts = census_data['Education'].value_counts()
            st.subheader("🎓 Education Distribution")
            st.bar_chart(edu_counts)
            st.write(edu_counts)
        else:
            st.error("❌ 'Education' column not found.")

    # ---- College Dropouts ----
    elif selected_report == "College Dropouts":
        if 'Education' in census_data.columns:
            dropouts = census_data[census_data['Education'] == "Somecollegebutnodegree"]
            st.subheader("🎓 College Dropouts")
            st.write(f"Total count: {dropouts.shape[0]}")
            st.dataframe(dropouts)
        else:
            st.error("❌ 'Education' column not found.")

    # ---- Senior Citizens ----
    elif selected_report == "Senior Citizens (55-60)":
        senior = census_data[(census_data['Age'] >= 55) & (census_data['Age'] < 60)]
        st.subheader("👴 Senior Citizens (Age 55-60)")
        st.write(f"Count: {senior.shape[0]}")
        st.dataframe(senior)

    # ---- Employable Widows & Divorced ----
    elif selected_report == "Employable Widows & Divorced":
        emp_widow_div = census_data[
            (census_data['Marital_Status'].isin(['Widowed', 'Divorced'])) &
            (census_data['Occupation'] != 'Unemployed')
        ]
        st.subheader("👩 Employable Widows & Divorced")
        st.write(f"Count: {emp_widow_div.shape[0]}")
        st.dataframe(emp_widow_div)

    # ---- Gender-wise Total Income ----
    elif selected_report == "Gender-wise Total Income":
        if 'Income' in census_data.columns:
            census_data['Income'] = pd.to_numeric(census_data['Income'], errors='coerce')
            gender_income = census_data.groupby('Gender')['Income'].sum()
            st.subheader("💰 Gender-wise Total Income")
            st.bar_chart(gender_income)
            st.write(gender_income)
        else:
            st.error("❌ 'Income' column not found.")

    # ---- Total Tax by Gender ----
    elif selected_report == "Total Tax (by Gender)":
        if 'Income' in census_data.columns:
            census_data['Income'] = pd.to_numeric(census_data['Income'], errors='coerce')
            tax_rate = 0.10
            gender_tax = census_data.groupby('Gender')['Income'].sum() * tax_rate
            gender_tax['Total'] = gender_tax.sum()
            st.subheader("💸 Total Tax To Be Collected (by Gender)")
            st.bar_chart(gender_tax)
            st.write(gender_tax)
        else:
            st.error("❌ 'Income' column not found.")

    # ---- Non-Citizens Working % ----
    elif selected_report == "Non-Citizens Working %":
        if 'Country' in census_data.columns:
            total_nc = census_data[census_data['Country'] != 'Citizen'].shape[0]
            working_nc = census_data[
                (census_data['Country'] != 'Citizen') & (census_data['Occupation'] != 'Unemployed')
            ].shape[0]
            percent = (working_nc / total_nc) * 100 if total_nc > 0 else 0
            st.subheader("🌍 Non-Citizens Working Percentage")
            st.write(f"{percent:.2f}% of non-citizens are employed.")
        else:
            st.error("❌ 'Country' or 'Occupation' column missing.")

    # ---- Orphans by Parents Category & Gender ----
    elif selected_report == "Orphans by Parents Category & Gender":
        if 'Parents_Present' in census_data.columns:
            orphan_cat = census_data.groupby(['Parents_Present', 'Gender']).size().reset_index(name='Count')
            st.subheader("🧒 Orphans by Parents Category & Gender")
            st.dataframe(orphan_cat)
        else:
            st.error("❌ 'Parents_Present' column not found.")

    # ---- Education Category & Gender Count ----
    elif selected_report == "Education Category & Gender Count":
        if {'Education', 'Gender'}.issubset(census_data.columns):
            edu_gender = census_data.groupby(['Education', 'Gender']).size().reset_index(name='Count')
            st.subheader("📘 Education Category-wise Gender Count")
            st.dataframe(edu_gender)
        else:
            st.error("❌ Required columns missing.")

else:
    st.info("👆 Please upload a CSV file to begin.")
