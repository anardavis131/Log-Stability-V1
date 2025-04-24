import streamlit as st
import requests

st.set_page_config(page_title="Log Stability Assistant", page_icon="🌲")
st.title("🌲 Log Stability Assistant")

st.markdown("Fill out the form below to check log stability based on USDA & ELJ guidelines.")

length = st.number_input("Log Length (ft)", 1.0, 200.0, value=40.0)
diameter = st.number_input("Diameter (ft)", 0.1, 10.0, value=1.7)
burial = st.number_input("Burial Depth (ft)", 0.0, 20.0, value=2.5)
flow = st.number_input("Flow Velocity (ft/s)", 0.0, 30.0, value=11.0)
orientation = 90
wood_density = 53
ballast_density = 120
surcharge = st.number_input("Sediment Cap Depth (ft)", 0.0, 10.0, value=0.5)
soil_friction = st.slider("Soil Friction Angle (°)", 20, 45, value=35)
species = st.selectbox("Wood Species", ["DouglasFir", "RedAlder", "WesternRedCedar"])
rootwad = st.radio("Rootwad Included?", ["Yes", "No"]) == "Yes"

if st.button("Submit"):
    api_url = "https://www.wolframcloud.com/obj/anardavis131/logStabilityTool"
    payload = {
        "length": length,
        "diameter": diameter,
        "burialDepth": burial,
        "flowVelocity": flow,
        "orientationDeg": orientation,
        "woodDensity": wood_density,
        "rootwad": rootwad,
        "soilFriction": soil_friction,
        "ballastDensity": ballast_density,
        "surchargeDepth": surcharge,
        "species": species
    }

    with st.spinner("Calculating..."):
        response = requests.post(api_url, json=payload)
        if response.ok:
            data = response.json()

            st.success("✅ Calculation complete.")
            st.subheader("Pass/Fail Results")
            st.json(data["Results"]["PassFail"])

            st.subheader("Factors of Safety")
            st.json(data["Equations"])

            st.subheader("Design Recommendations")
            for rec in data["Recommendations"]:
                st.markdown(f"- {rec}")
        else:
            st.error("❌ API call failed. Check inputs or try again.")
