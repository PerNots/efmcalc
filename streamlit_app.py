# efm Calculator to easily calculate prices to be paid for orders

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(layout="wide")
st.title("efm Getränke-Rechner")

# Dict containing drinks and prices
emoji_list = [
    "💧", "🥤", "🥤🍊", "🍎", "🐂", "🍺", "🚴", "🍺🚗", "🍷", "🥃🥤", 
    "🥒", "🍸🐂", "🎯🐂", "🎯", "🥜", "🔴"
]

prices = {
    "Wasser": 3.50,
    "Cola": 3.50,
    "Spezi": 3.50,
    "Apfel": 3.50,
    "RedBull": 4.50,
    "Bier": 5.00,
    "Radler": 5.00,
    "Jever": 3.50,
    "WeißweinSchorle": 6.00,
    "WhiskyCola": 8.50,
    "GinTonic": 8.50,
    "WodkaRedBull": 4.50,
    "JägerRedBull": 9.50,
    "SHOT Jäger": 2.50,
    "SHOT Nuss": 2.50,
    "Pfanderlass": -2.00
}

# Initial DataFrame that will be displayed as interactive Table
data = {
    'Icon': emoji_list,
    'Name': list(prices.keys()),
    'Menge': [0] * len(prices),  # Initialize Amount as 0 for each item
}

# Store the initial data in session_state if it's not already set
# Counter used to force-update the table via reset-button
if 'counter' not in st.session_state:
    st.session_state.counter = 0 
# df holding the current entries
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(data)

# JavaScript code to create a number input field in the grid via two buttons 
# and the current number displayed in between
number_input_renderer = JsCode("""
class NumberInputRenderer {
    init(params) {
        this.params = params;

        // Create a container div
        this.eGui = document.createElement('div');
        this.eGui.style.display = 'flex';
        this.eGui.style.alignItems = 'center';
        
        // Create the 'Decrease' button
        this.decreaseButton = document.createElement('button');
        this.decreaseButton.innerText = '-';
        this.decreaseButton.style.marginRight = '5px';
        this.decreaseButton.style.width = '40px';  // Set the width of the button
        
        // Create the value display
        this.valueDisplay = document.createElement('span');
        this.valueDisplay.innerText = params.value;
        this.valueDisplay.style.marginRight = '5px';
        
        // Create the 'Increase' button
        this.increaseButton = document.createElement('button');
        this.increaseButton.innerText = '+';
        this.increaseButton.style.width = '40px';  // Set the width of the button

        // Append buttons and value display to the container
        this.eGui.appendChild(this.decreaseButton);
        this.eGui.appendChild(this.valueDisplay);
        this.eGui.appendChild(this.increaseButton);

        // Add event listeners for the buttons
        this.decreaseButton.addEventListener('click', () => this.changeValue(-1));
        this.increaseButton.addEventListener('click', () => this.changeValue(1));
    }

    changeValue(delta) {
        let currentValue = parseFloat(this.valueDisplay.innerText);
        let newValue = currentValue + delta;
        
        // Update the display and the grid value
        this.valueDisplay.innerText = newValue;
        this.params.node.setDataValue(this.params.column.colId, newValue);
    }

    getGui() {
        return this.eGui;
    }

    destroy() {
        this.decreaseButton.removeEventListener('click', this.changeValue);
        this.increaseButton.removeEventListener('click', this.changeValue);
    }
}
""")

# Configure AgGrid and set options
gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
gb.configure_column('Menge', 
                    editable=True, 
                    #autoSize=True,
                    width=100,
                    sortable = False,
                    filterable = False, 
                    cellRenderer=number_input_renderer
                    )  # Number input
gb.configure_column('Name', 
                    #autoSize=True, 
                    width = 40,
                    sortable=False, 
                    filterable=False)
gb.configure_column('Icon', 
                    width = 4,
                    maxwidth = 4,
                    #autoSize=True, 
                    sortable=False, 
                    filterable=False)
gb.configure_grid_options(update_mode="VALUE_CHANGED", 
                          suppressMovableColumns=True,
                          domLayout='autoHeight', #adjust gridheight to columns
                          height = 800,
                          suppressAutoSize=False,
                          headerHeight=0,
                          )  # Prevent auto update

# Reset button placed above the table
if st.button("Tabelle zurücksetzen"):
    # Reset Amounts to 0 in the DataFrame
    st.session_state.df['Menge'] = [0] * len(st.session_state.df)
    # Increment the session state counter to force the AgGrid to refresh
    st.session_state.counter += 1

# Create AgGrid interface
ag = AgGrid(
    st.session_state.df,
    gridOptions=gb.build(),
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
    key=f"aggrid_{st.session_state.counter}"
)

# Button to trigger calculation
if st.button("Berechnen"):
    # Refresh the grid data manually
    new_data = ag['data']
    
    # Calculate the total sum based on the updated 'Amount' column and 'prices' dict
    total_sum = 0
    pfand_in_bill=0
    pfand_return=0
    pfandfree =0
    for i, row in new_data.iterrows():
        if row['Name'] not in ("Pfanderlass", "SHOT Jäger", "SHOT Nuss"):  # Exclude these drinks from counting towards Pfand
            name = row['Name']
            Menge = row['Menge']
            total_sum += Menge * prices.get(name, 0)  # Multiply with the price from the dict
            total_sum += Menge * 2 # adding pfand to the drinks that have it
            pfand_in_bill += Menge # number of pfand paid by customer (number of red chips handed out)
        elif row['Name']=="Pfanderlass":
            name = row['Name']
            Menge = row['Menge']
            total_sum += Menge * (-2) # calculate pfand back
            pfand_return += Menge # number of pfand refunded (number of red chips received)
        elif row['Name'] in ("SHOT Jäger", "SHOT Nuss"):
            name = row['Name']
            Menge = row['Menge']
            total_sum += Menge * prices.get(name, 0) # calculate price without pfand
            pfandfree += Menge # number of pfandfree drinks
    
    # Display the total
    if (pfand_in_bill-pfand_return>=0):
        st.write(f"Total: {total_sum:.2f} EUR --- {pfand_in_bill-pfand_return} rote Marken ausgeben")
    else:
        st.write(f"Total: {total_sum:.2f} EUR --- {pfand_return-pfand_in_bill} rote Marken geben lassen")


    st.subheader("Details")
    for i in range(len(new_data)):
    # Check if the 'Menge' for each row is not zero
        if new_data['Menge'][i] != 0:
            name = new_data['Name'][i]  # Get the 'Name' for the current row
            Menge = new_data['Menge'][i]  # Get the 'Menge' for the current row
            single_price = prices.get(name, 0)  # Get the price from the 'prices' dict
            st.write(f"{name}:   {Menge} * {single_price:.2f}€ = {(Menge * single_price):.2f}€")
    st.write(f"Pfand:   {pfand_in_bill} * 2.00€ = {(pfand_in_bill*2):.2f}€")
    st.write("")
    #st.write(f"{pfand_return} rote Marken von Kunden geben lassen.")
    #st.write(f"{pfand_in_bill} rote Marken ausgeben.")

st.subheader("Info")
st.write("Pfand wird automatisch hinzugefügt und muss manuell wieder abgezogen werden falls nicht fällig. Dies ist durch Zahlen in 'Pfanderlass' möglich.")
st.write("Bsp.: Kunde kommt mit 2 leeren Bechern Bier und will ein Neues (-> Bier auf 1, Pfanderlass auf 2 und eine Pfandmarke geben lassen)")
st.write("Bsp.: Kunde kommt mit 2 leeren Bechern Bier und will 3 Neue (-> Bier auf 3, Pfanderlass auf 2 und eine rote Marke ausgeben)")