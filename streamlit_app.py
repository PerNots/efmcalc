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
    cols = st.columns([2, 3, 3, 1])  # Adjust column sizes for better alignment
    with cols[0]:
        st.write(f"{drink}: {prices[drink]:.2f}")
    with cols[1]:
        if st.markdown(
            f"""
            <button style="width:100%; padding:0px; font-size:12px; cursor:pointer;" onclick="window.location.reload()">+</button>
            """,
            unsafe_allow_html=True,
        ):
            st.session_state.counts[drink] += 1
            if drink != "Pfand":
                update_pfand(1)
    with cols[2]:
        if st.markdown(
            f"""
            <button style="width:100%; padding:0px; font-size:12px; cursor:pointer;" onclick="window.location.reload()">-</button>
            """,
            unsafe_allow_html=True,
        ):
            if st.session_state.counts[drink] > 0:
                st.session_state.counts[drink] -= 1
                if drink != "Pfand":
                    update_pfand(-1)
    with cols[3]:
        st.write(f"{st.session_state.counts[drink]}")  # Display current count

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
