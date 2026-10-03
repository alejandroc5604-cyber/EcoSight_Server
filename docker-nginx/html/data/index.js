const SearchLimit = 100


async function fetchUserData() {
  const url = 'http://0.0.0.0:8000/ReturnJSONData?limit=100';
  
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Fetched from ', url, ": ", data);
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

function UpdateTable(){
    const data = fetchUserData();
    console.log(data);
    // 2. Target the container where the table will live
    const container = document.getElementById("table-container");

    // 3. Create the <table> element
    const table = document.createElement("table");

    // 4. Create the Header Row (<th>)
    const headerRow = document.createElement("tr");
    const headers = ["Item", "Quantity", "Price"];

    headers.forEach(headerText => {
    const th = document.createElement("th");
    th.textContent = headerText;
    headerRow.appendChild(th);
    });
    table.appendChild(headerRow); // Add the header row to the table

    // 5. Create the Data Rows (<td>)
    data.forEach(product => {
    const row = document.createElement("tr");

    // Loop through the object properties and create a cell for each
    Object.values(product).forEach(text => {
        const td = document.createElement("td");
        td.textContent = text;
        row.appendChild(td);
    });

    table.appendChild(row); // Add the data row to the table
    });

    // 6. Append the completed table to your HTML page
    container.appendChild(table);
};



window.onload = function() {
    UpdateTable();
}