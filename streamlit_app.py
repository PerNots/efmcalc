import streamlit as st

st.set_page_config(layout="wide")

st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

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
    "Pfanderlass":-2.00,
}

prices_adj = {
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

# Form layout with alternating column backgrounds
with st.form(key="drinkform", clear_on_submit=True):
    for drink in prices_adj:
        cols = st.columns([1, 3], vertical_alignment="center")  # Adjust column sizes [1, 3]
        with cols[0]:
            st.write(f"{drink}")
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
        cols = st.columns([1, 3], vertical_alignment="center")  # Adjust column sizes
        with cols[0]:
            st.write(f"{drink}")
        with cols[1]:
            # Capture the current count and use it for the number input
            pfand_back = st.number_input(
                label="change",
                key=drink + "plus",
                step=1,
                label_visibility="collapsed",
                value=0
            )

    submitButton = st.form_submit_button(label='Rechnen')


# After form submission, calculate total and reset if needed
if submitButton:
    # Calculate total drinks cost
    total = 0
    for drink, count in st.session_state.counts.items():
        total += count * prices_adj[drink]

    # Calculate Pfand and adjust based on user input (if any reduction is applied)
    st.session_state.pfand_total = calculate_pfand()  # Update Pfand based on counts
    adjusted_pfand = st.session_state.pfand_total + pfand_back*2  # Apply manual reduction

    # Display totals
    st.markdown(f"<h1 style='text-align: center; color: green;'>Total: {total + adjusted_pfand:.2f}€</h1>", unsafe_allow_html=True)

    # Display drink summary
    st.write("### Zusammenfassung")
    for drink, count in st.session_state.counts.items():
        if count > 0:
            st.write(f"{drink}: {count} x {prices_adj[drink]:.2f}€ = {count * prices_adj[drink]:.2f}€")
    
    # Display the total Pfand and Pfand zurück
    st.write(f"**Pfand**: {st.session_state.pfand_total} x 2€ = {st.session_state.pfand_total}€")
    if pfand_back != 0:
        st.write(f"**Pfand zurück**: {pfand_back} x 2€ = {pfand_back*2}€")
        #st.write(f"**Adjusted Pfand**: {adjusted_pfand} x 2€ = {adjusted_pfand}€")

    # Reset counts and Pfand for the next calculation
    st.session_state.counts = {drink: 0 for drink in prices_adj}  # Reset counts after calculation
    st.session_state.pfand_total = 0  # Reset Pfand total for the next calculation



st.subheader("")
st.subheader("info")
st.write("Knöpfe drücken um Getränke hinzuzufügen oder abzuziehen.")
st.write("Pfand wird automatisch hinzugefügt und muss manuell wieder abgezogen werden falls nicht fällig. Dies ist durch negative Beträge in 'Pfand zurück' möglich.")
st.write("Bsp.: Kunde kommt mit 2 leeren Bechern Bier und will ein Neues (-> Bier auf +1, Pfand auf -1 und eine Pfandmarke geben lassen)")
st.write("")
st.write("Falls die Kacheln unter den Getränkenamen erscheinen, kann die Website im Browser herausgezoomt werden. Leider passt sich die app dynamisch an die Bildschirmgröße an.")
st.image("https://i.imgur.com/WyGVqkT.png")




import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# Initial DataFrame
data = {
    'Name': list(prices.keys()),
    'Amount': [0] * len(prices),  # Initialize Amount as 0 for each item
}

# Store the initial data in session_state if it's not already set
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(data)

# JavaScript code to create a number input field in the grid
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



# Configure AgGrid
gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
gb.configure_column('Amount', 
                    editable=True, 
                    autoSize=True,
                    sortable = False,
                    filterable = False, 
                    cellRenderer=number_input_renderer
                    )  # Number input
#gb.configure_column('Name', width=200)  # Set the width for 'Name' column
#gb.configure_column('Amount', width=150)  # Set the width for 'Amount' column
gb.configure_column('Name', 
                    autoSize=True, 
                    sortable=False, 
                    filterable=False)
gb.configure_grid_options(update_mode="NO_UPDATE", 
                          suppressMovableColumns=True,
                          domLayout='autoHeight', #adjust gridheight to columns
                          suppressAutoSize=True,
                          )  # Prevent auto update

# Reset button placed above the table
if st.button("Reset All to 0"):
    # Reset Amounts to 0 in the DataFrame and update session_state
    st.session_state.df['Amount'] = [0] * len(st.session_state.df)
    st.rerun()  # Trigger rerun to update the table

# Create AgGrid interface
ag = AgGrid(
    st.session_state.df,
    gridOptions=gb.build(),
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
)

# Button to trigger calculation
if st.button("Calculate Total"):
    # Refresh the grid data manually
    new_data = ag['data']
    
    # Calculate the total sum based on the updated 'Amount' column and 'prices' dict
    total_sum = 0
    pfand_in_bill=0
    pfand_return=0
    pfandfree =0
    for i, row in new_data.iterrows():
        if row['Name'] not in ("Pfanderlass", "Jäger", "FangDieNuss"):  # Exclude these drinks from counting towards Pfand
            name = row['Name']
            amount = row['Amount']
            total_sum += amount * prices.get(name, 0)  # Multiply with the price from the dict
            total_sum += amount * 2 # adding pfand to the drinks that have it
            pfand_in_bill += amount # number of pfand paid by customer (number of red chips handed out)
        elif row['Name']=="Pfanderlass":
            name = row['Name']
            amount = row['Amount']
            total_sum += amount * (-2) # calculate pfand back
            pfand_return += amount # number of pfand refunded (number of red chips received)
        elif row['Name'] in ("Jäger", "FangDieNuss"):
            name = row['Name']
            amount = row['Amount']
            total_sum += amount * prices.get(name, 0)
            pfandfree += amount # number of pfandfree
    
    # Display the total
    if (pfand_in_bill-pfand_return>=0):
        st.write(f"Total: {total_sum:.2f} EUR --- {pfand_in_bill-pfand_return} rote Marken ausgeben")
    else:
        st.write(f"Total: {total_sum:.2f} EUR --- {pfand_return-pfand_in_bill} rote Marken geben lassen")


    st.subheader("Details")
    for i in range(len(new_data)):
    # Check if the 'Amount' for each row is not zero
        if new_data['Amount'][i] != 0:
            name = new_data['Name'][i]  # Get the 'Name' for the current row
            amount = new_data['Amount'][i]  # Get the 'Amount' for the current row
            single_price = prices.get(name, 0)  # Get the price from the 'prices' dict
            st.write(f"{name}:   {amount} * {single_price} = {amount * single_price}€")
    st.write(f"Pfand:   {pfand_in_bill} * 2€ = {pfand_in_bill*2}€")
    st.write("")
    st.write(f"{pfand_return} rote Marken von Kunden geben lassen.")
    st.write(f"{pfand_in_bill} rote Marken ausgeben.")

st.subheader("Info")
st.write("Pfand wird automatisch hinzugefügt und muss manuell wieder abgezogen werden falls nicht fällig. Dies ist durch Zahlen in 'Pfanderlass' möglich.")
st.write("Bsp.: Kunde kommt mit 2 leeren Bechern Bier und will ein Neues (-> Bier auf 1, Pfanderlass auf 2 und eine Pfandmarke geben lassen)")
st.write("Bsp.: Kunde kommt mit 2 leeren Bechern Bier und will 3 Neue (-> Bier auf 3, Pfanderlass auf 2 und eine rote Marke ausgeben)")