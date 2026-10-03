//CONSTANTS

const SearchLimit = 100

function Setup() {
    const SearchLimitInsert = document.getElementById("SearchLimiterInsert");
    SearchLimitInsert.textContent = `Searching for ${SearchLimit} most recent`;   
}

window.onload = function() {
    Setup();
}