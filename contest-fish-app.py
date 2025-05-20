import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Bass Bash Tournament", layout="centered")
st.title("🎣 Bass Bash: Tagging Tournament")
st.subheader("Catch. Tag. Compete. Let the fun begin!")

# Initialize cache (persisted on session)
@st.cache_data(show_spinner=False)
def get_initial_data():
    return pd.DataFrame(columns=["Technician", "Length (in)", "Weight (lbs)", "Tagged", "Timestamp", "Date"])

if "data" not in st.session_state:
    st.session_state.data = get_initial_data()

# --- Input Form ---
with st.form("catch_form", clear_on_submit=True):
    tech = st.text_input("Your Name")
    length = st.number_input("Bass Length (in)", min_value=0.0, step=0.1)
    weight = st.number_input("Bass Weight (lbs) (optional)", min_value=0.0, step=0.1)
    tagged = st.checkbox("Tagged?")
    submit = st.form_submit_button("🎣 Log Catch")

    if submit:
        if tech and length > 0:
            new_entry = pd.DataFrame([{
                "Technician": tech.strip(),
                "Length (in)": length,
                "Weight (lbs)": weight if weight > 0 else None,
                "Tagged": tagged,
                "Timestamp": datetime.now(),
                "Date": date.today()
            }])
            st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
            st.success("Catch logged! 🎉")
        else:
            st.error("Please enter your name and a valid length.")

# --- Today's Data ---
df_today = st.session_state.data[st.session_state.data["Date"] == date.today()]

if not df_today.empty:
    st.markdown("## 🏁 Leaderboards")

    # Most Fish
    fish_count = df_today['Technician'].value_counts().reset_index()
    fish_count.columns = ['Technician', 'Fish Caught']
    st.write("🎯 Most Fish Caught", fish_count)

    # Biggest Bass
    biggest = df_today.sort_values("Length (in)", ascending=False).head(1)
    if not biggest.empty:
        st.write("💪 Biggest Bass Caught Today")
        st.metric(label=f"{biggest.iloc[0]['Technician']}", value=f"{biggest.iloc[0]['Length (in)']} inches")

    st.markdown("## 📋 All Catches")
    st.dataframe(df_today[['Technician', 'Length (in)', 'Weight (lbs)', 'Tagged', 'Timestamp']], use_container_width=True)

    # Winners
    st.markdown("## 🏆 Today's Winners")
    st.success(f"🥇 Most Fish: {fish_count.iloc[0]['Technician']} ({fish_count.iloc[0]['Fish Caught']} bass)")
    st.success(f"🐷 Biggest Bass: {biggest.iloc[0]['Technician']} ({biggest.iloc[0]['Length (in)']} inches)")
else:
    st.info("No catches logged today yet.")
