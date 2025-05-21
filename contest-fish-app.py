import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

st.set_page_config(page_title="Bass Tagging Tracker", layout="centered")
st.title("📌 Largemouth Bass Tagging Tracker")
st.subheader("Track all fish caught and tagged in the field!")

# Initialize cache/session
@st.cache_data(show_spinner=False)
def get_initial_data():
    return pd.DataFrame(columns=[
        "Technician", "Length (in)", "Weight (lbs)",
        "Tagged", "Tag Number", "Timestamp", "Date"
    ])

if "data" not in st.session_state:
    st.session_state.data = get_initial_data()

# --- Input Form ---
with st.form("catch_form", clear_on_submit=True):
    st.markdown("### 📝 Log a New Fish")
    tech = st.text_input("Technician Name")
    length = st.number_input("Length (inches)", min_value=0.0, step=0.1)
    weight = st.number_input("Weight (lbs) (optional)", min_value=0.0, step=0.1)
    tagged = st.checkbox("Tag Inserted?")

    tag_number = ""
    if tagged:
        tag_number = st.text_input("Tag Number (required if tagged)")

    submitted = st.form_submit_button("Log Catch")

    if submitted:
        if not tech or length <= 0:
            st.error("Please enter a name and valid fish length.")
        elif tagged and not tag_number.strip():
            st.error("Please enter a tag number for tagged fish.")
        else:
            new_entry = pd.DataFrame([{
                "Technician": tech.strip(),
                "Length (in)": length,
                "Weight (lbs)": weight if weight > 0 else None,
                "Tagged": tagged,
                "Tag Number": tag_number.strip() if tagged else None,
                "Timestamp": datetime.now(),
                "Date": date.today()
            }])
            st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
            st.success("Fish logged successfully! 🎣")

# --- Today's Data ---
df_today = st.session_state.data[st.session_state.data["Date"] == date.today()]

if not df_today.empty:
    st.markdown("## 📈 Field Results for Today")

    # Most fish caught
    fish_count = df_today['Technician'].value_counts().reset_index()
    fish_count.columns = ['Technician', 'Fish Caught']
    st.write("🎯 Most Fish Caught", fish_count)

    # Biggest fish
    biggest = df_today.sort_values("Length (in)", ascending=False).head(1)
    if not biggest.empty:
        st.write("🏆 Biggest Fish Tagged Today")
        st.metric(label=f"{biggest.iloc[0]['Technician']}", value=f"{biggest.iloc[0]['Length (in)']} inches")

    # Histogram of lengths
    st.markdown("### 📊 Length Distribution of Fish Caught")
    fig, ax = plt.subplots()
    ax.hist(df_today["Length (in)"], bins=10, edgecolor='black')
    ax.set_xlabel("Length (inches)")
    ax.set_ylabel("Number of Fish")
    ax.set_title("Length Frequency Histogram")
    st.pyplot(fig)

    # Raw table
    st.markdown("## 🗃️ Catch Log")
    st.dataframe(
        df_today[['Technician', 'Length (in)', 'Weight (lbs)', 'Tagged', 'Tag Number', 'Timestamp']],
        use_container_width=True
    )

    # Winners
    st.markdown("## 🏅 Today's Recognition")
    st.success(f"Most Fish: {fish_count.iloc[0]['Technician']} ({fish_count.iloc[0]['Fish Caught']} fish)")
    st.success(f"Lunker of the Day: {biggest.iloc[0]['Technician']} ({biggest.iloc[0]['Length (in)']} inches)")
else:
    st.info("No fish logged today yet. Let's tag some bass!")

