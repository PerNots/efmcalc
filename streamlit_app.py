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
}

prices_anti = {
    "Wasser": 3.50,
    "Cola": 3.50,
    "Spezi": 3.50,
    "Apfel": 3.50,
    "RedBull": 4.50,
}

prices_notanti = {
    "Bier": 5.00,
    "Radler": 5.00,
    "Jever": 3.50,
    "WeißweinSch":6.00,
}

prices_hard = {
    "WhiskyCola":8.50,
    "GinTonic": 8.50,
    "WodkaRedBull": 4.50,
    "JägerRedBull": 9.50,
    "Jäger":2.50,
    "FangDieNuss":2.50,
}

prices_pfand = {
    "Pfand zurück": 2.00
} # for pfand NO minimum value, for the others minimum value = 0
# Initialize session state for drink counts


if "counts" not in st.session_state:
    st.session_state.counts = {drink: 0 for drink in prices}
if "pfand_total" not in st.session_state:
    st.session_state.pfand_total = 0  # This tracks the total Pfand charged

# Render UI
st.title("efm Getränke-Preis-Rechner")

# Update total Pfand automatically based on the total count of drinks
def calculate_pfand():
    total_pfand = 0
    for drink, count in st.session_state.counts.items():
        if drink not in ("Pfand", "Jäger", "FangDieNuss"):  # Exclude these drinks from counting towards Pfand
            total_pfand += count * 2  # 2€ of Pfand per drink
    return total_pfand

# Display drink buttons in a mobile-friendly layout
with st.form(key="drinkform",clear_on_submit=True):
    for drink in prices:
        cols = st.columns(2)  # Adjust column sizes [1, 1]
        with cols[0]:
            st.markdown(f"<small>{drink}</small>", unsafe_allow_html=True)
        with cols[1]:
            # Capture the current count and use it for the number input
            current_count = st.session_state.counts[drink]
            new_count = st.number_input(
                label="change",
                key=drink + "plus",
                step=1,
                min_value=0,
                label_visibility="collapsed",
                value=current_count
            )
            
            # Update session state for counts if there is a change
            if new_count != current_count:
                st.session_state.counts[drink] = new_count
    for drink in prices_pfand:
        cols = st.columns([1, 1])  # Adjust column sizes
        with cols[0]:
            st.markdown(f"<small>{drink}</small>", unsafe_allow_html=True)
        with cols[1]:
            # Capture the current count and use it for the number input
            pfand_back = st.number_input(
                label="change",
                key=drink + "plus",
                step=1,
                #min_value=0,
                #min_value=-st.session_state.pfand_total,  # Allow up to the current total Pfand for reduction
                label_visibility="collapsed",
                value=0
            )

    
    submitButton = st.form_submit_button(label='Rechnen')

# After form submission, calculate total and reset if needed
if submitButton:
    # Calculate total drinks cost
    total = 0
    for drink, count in st.session_state.counts.items():
        total += count * prices[drink]

    # Calculate Pfand and adjust based on user input (if any reduction is applied)
    st.session_state.pfand_total = calculate_pfand()  # Update Pfand based on counts
    adjusted_pfand = st.session_state.pfand_total + pfand_back*2  # Apply manual reduction

    # Display totals
    st.markdown(f"<h1 style='text-align: center; color: green;'>Total: {total + adjusted_pfand:.2f}€</h1>", unsafe_allow_html=True)

    # Display drink summary
    st.write("### Zusammenfassung")
    for drink, count in st.session_state.counts.items():
        if count > 0:
            st.write(f"{drink}: {count} x {prices[drink]:.2f}€ = {count * prices[drink]:.2f}€")
    
    # Display the total Pfand and Pfand zurück
    st.write(f"**Pfand**: {st.session_state.pfand_total} x 2€ = {st.session_state.pfand_total}€")
    if pfand_back != 0:
        st.write(f"**Pfand zurück**: {pfand_back} x 2€ = {pfand_back*2}€")
        #st.write(f"**Adjusted Pfand**: {adjusted_pfand} x 2€ = {adjusted_pfand}€")

    # Reset counts and Pfand for the next calculation
    st.session_state.counts = {drink: 0 for drink in prices}  # Reset counts after calculation
    st.session_state.pfand_total = 0  # Reset Pfand total for the next calculation



st.subheader("")
st.subheader("info")
st.write("Knöpfe drücken um Getränke hinzuzufügen oder abzuziehen.")
st.write("Pfand wird automatisch hinzugefügt und muss manuell wieder abgezogen werden falls nicht fällig. Dies ist durch negative Beträge in 'Pfand zurück' möglich.")
st.write("Bsp.: Kunde kommt mit 2 leeren Bechern Bier und will ein Neues (-> Bier auf +1, Pfand auf -1 und eine Pfandmarke geben lassen)")
