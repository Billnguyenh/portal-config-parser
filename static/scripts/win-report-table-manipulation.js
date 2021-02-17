const showLoadingSpinner = () => {
    var loadingSpinner = document.getElementById("loading-spinner")
    loadingSpinner.style.display = "block"
    loadingSpinner.style.margin = "auto"
}

const hideLoadingSpinner = () => {
    var loadingSpinner = document.getElementById("loading-spinner")
    loadingSpinner.style.display = "none"
}

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const updateHostCount = (tableId) => {
    let table, uniqueHosts, tableRows, count, hostCounter;
    table = document.getElementById(tableId);
    tableRows = table.getElementsByTagName("tr");
    uniqueHosts = []
    for (i = 1; i < tableRows.length; i++) {
        if (tableRows[i].style.display != "none"){
            hostname = tableRows[i].getElementsByTagName("td")[0].innerText;
            if (!uniqueHosts.includes(hostname)) {
                uniqueHosts.push(hostname);
            }
        }
    }
    count = uniqueHosts.length;

    hostCounter = table.getElementsByTagName("span")[0]

    hostCounter.innerHTML = count
}

const updateHostCountAllTables = () => {
    let idArr, tables, i;
    idArr = [];
    tables = document.getElementsByTagName("table");

    for (i = 0; i < tables.length; i++) {
        idArr.push(tables[i].id)
    }

    for (i = 0; i < idArr.length; i++) {
        let tableId = idArr[i];
        updateHostCount(tableId)
    }
}

const searchTable = async (searchBarId, tableId) => {
    await showLoadingSpinner()
    await sleep(10)
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById(searchBarId);
    filter = input.value.toUpperCase();
    table = document.getElementById(tableId);
    tr = table.getElementsByTagName("tr");
    
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td_col_1 = tr[i].getElementsByTagName("td")[0];
        td_col_2 = tr[i].getElementsByTagName("td")[1];
        td_col_3 = tr[i].getElementsByTagName("td")[2];
        if (td_col_3) {
            txtValue_col_1 = td_col_1.textContent || td_col_1.innerText 
            txtValue_col_2 = td_col_2.textContent || td_col_2.innerText
            txtValue_col_3 = td_col_3.textContent || td_col_3.innerText
            if (txtValue_col_1.toUpperCase().indexOf(filter) > -1 || txtValue_col_2.toUpperCase().indexOf(filter) > -1 || txtValue_col_3.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
        if (td_col_1 && td_col_2 && !td_col_3) {
            txtValue_col_1 = td_col_1.textContent || td_col_1.innerText 
            txtValue_col_2 = td_col_2.textContent || td_col_2.innerText
            if (txtValue_col_1.toUpperCase().indexOf(filter) > -1 || txtValue_col_2.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
            
        }
    }
    updateHostCount(tableId)
    hideLoadingSpinner()
}

const sortTableRowsByColumn = async (table, columnIndex, isAscending) => {
    const rows = Array.from(table.querySelectorAll('tbody > tr'));

    rows.sort( (rowX, rowY) => {
        const xValue = rowX.cells[columnIndex].textContent;
        const yValue = rowY.cells[columnIndex].textContent;
        let x, y;

        const xDate = new Date(xValue);
        const yDate = new Date(yValue);

        if (xDate != "Invalid Date" && yDate != "Invalid Date") {
            x = xDate;
            y = yDate;
        }
        else if (typeof(xValue) === "string" && typeof(yValue) === "string") {
            x = xValue.toLowerCase();
            y = yValue.toLowerCase();
        }

        if (isAscending) {
            if (x < y) {
                return -1;
            }
            if (x > y) {
                return 1;
            }
            return 0;
        }
        if (!isAscending) {
            if (x > y) {
                return -1;
            }
            if (x < y) {
                return 1;
            }
            return 0;
        }
    });

    for ( let row of rows ) {
        table.tBodies[0].appendChild(row);
    }
}

const onColumnHeaderClicked = async (event) => {
    const th = event.currentTarget; //HTMLTableCellElement
    const table = th.closest('table');
    const thIndex = Array.from(th.parentElement.children).indexOf(th);
    const isAscending = !('sort' in th.dataset) || th.dataset.sort != 'asc';
    
    await showLoadingSpinner()
    await sleep(10)

    sortTableRowsByColumn(table, thIndex, isAscending);

    const allTh = table.querySelectorAll('thead > tr > th');
    for (let th2 of allTh) {
        delete th2.dataset['sort'];
    }
    
    th.dataset['sort'] = isAscending ? 'asc' : 'desc';

    hideLoadingSpinner()
}

const enableTableEventListeners = () => {
    const reportSection = document.getElementById("report-section");
    const allTh = reportSection.getElementsByTagName("th");

    for (let th of allTh) {
        th.addEventListener('click', function(event) {
            onColumnHeaderClicked(event);
        });
    }
}

window.onload = updateHostCountAllTables();
window.onload = enableTableEventListeners();

