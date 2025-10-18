import streamlit as st
from src.agent import generate_recommendations
import pandas as pd

def main():
    try:
        st.write("App started")  # Debug print to confirm app runs

        st.title("Generative AI Agent for Environmental CO₂ Reduction")

        st.write("Enter your activity or upload a dataset to get sustainability recommendations.")

        query = st.text_input("Describe your activity (e.g., 'I drive 20 km daily using a petrol car'):")

        uploaded_file = st.file_uploader("Upload a CSV file with activities (optional)", type="csv")

        st.write("UI elements loaded")  # Debug print to confirm UI elements rendered

        if st.button("Get Recommendations"):
            if query:
                with st.spinner("Generating recommendations..."):
                    try:
                        response = generate_recommendations(query)
                        st.write("**Recommendations:**")
                        st.write(response)
                    except Exception as e:
                        st.error(f"Error generating recommendations: {e}")
            elif uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)
                    # Simple calculation, assume columns match
                    if 'Avg_CO2_Emission(kg/day)' in df.columns:
                        total_emission = df['Avg_CO2_Emission(kg/day)'].sum()
                        st.write(f"Total estimated CO2 emission from activities: {total_emission} kg/day")
                        # Perhaps generate general tips
                        response = generate_recommendations("general CO2 reduction tips")
                        st.write("**General Recommendations:**")
                        st.write(response)
                    else:
                        st.error("CSV must have 'Avg_CO2_Emission(kg/day)' column.")
                except Exception as e:
                    st.error(f"Error processing uploaded file: {e}")
            else:
                st.error("Please enter a query or upload a file.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
