import streamlit as st

# Drink prices
prices = {
    "Wasser": 3.50,
    "Cola": 3.50,
    "Spezi": 3.50,
    "Apfel": 3.50,
    "RedBull": 4.50,
    "Bier": 5.00,
    "Radler": 5.00,
    "Jever": 3.50,
    "WeißweinSch":6.00,
    "WhiskyCola":8.50,
    "GinTonic": 8.50,
    "WodkaRedBull": 4.50,
    "JägerRedBull": 9.50,
    "Jäger":2.50,
    "FangDieNuss":2.50,
    "Pfand": 2.00
}

# Add custom CSS to control column layout
st.markdown(
    """
    <style>
    /* Force columns to stay side by side */
    .stButton > button {
        margin: 0;  /* Remove extra margin */
        padding: 4px; /* Adjust padding for compact buttons */
    }
    .stColumn {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 10px; /* Adjust spacing between items */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for drink counts
if "counts" not in st.session_state:
    st.session_state.counts = {drink: 0 for drink in prices}

# Render UI
st.title("efm Getränke-Preis-Rechner")

# Update total Pfand automatically
def update_pfand(increment):
    st.session_state.counts["Pfand"] += increment

# Display drink buttons in a mobile-friendly layout
for drink in prices:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
            <div style="flex: 3;">{drink}: {prices[drink]:.2f}</div>
            <div style="flex: 3;">
                <button style="width:100%; padding:0px; font-size:12px; cursor:pointer;" onclick="window.location.reload()">+</button>
            </div>
            <div style="flex: 3;">
                <button style="width:100%; padding:0px; font-size:12px; cursor:pointer;" onclick="window.location.reload()">-</button>
            </div>
            <div style="flex: 1; text-align: center;">{st.session_state.counts[drink]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

total = 0
for drink, count in st.session_state.counts.items():
    total += count * prices[drink]

st.markdown(f"<h1 style='text-align: center; color: green;'>Total: {total:.2f}€</h1>", unsafe_allow_html=True)


# Display totals
st.write("### Zusammenfassung")

for drink, count in st.session_state.counts.items():
    if count > 0:
        st.write(f"{drink}: {count} x {prices[drink]:.2f}€ = {count * prices[drink]:.2f}€")

st.subheader("")
st.subheader("info")
st.write("Knöpfe drücken um Getränke hinzuzufügen oder abzuziehen.")
st.write("Pfand wird automatisch hinzugefügt und muss manuell wieder abgezogen werden falls nicht fällig.")
