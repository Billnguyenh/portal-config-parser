const showModal = (modalId) => {
    let modal = document.getElementById(modalId);
    modal.style.display = "block";
    document.body.style.overflow = "hidden";
}

const closeModal = (modalId) => {
    let modal = document.getElementById(modalId);
    modal.style.display = "none";
    document.body.style.overflow = "auto";
}

const updateHostMatchModal = (table) => {

    let old_host_match_ol = document.getElementById("host-match-ol");
    let old_host_nonmatch_ol = document.getElementById("host-nonmatch-ol");

    let new_host_match_ol = document.createElement('OL');
    let new_host_nonmatch_ol = document.createElement('OL');

    let matching_hosts = [];
    let nonmatching_hosts = [];

    let table_rows = table.getElementsByTagName("tr");

    for (let i = 1; i < table_rows.length; i++) {
        hostname = table_rows[i].getElementsByTagName("td")[0].innerText;
        if (!matching_hosts.includes(hostname)) {
            if (table_rows[i].style.display !== "none"){
                matching_hosts.push(hostname);
            }
        }
    }
    for (let i = 1; i < table_rows.length; i++) {
        hostname = table_rows[i].getElementsByTagName("td")[0].innerText;
        if (!matching_hosts.includes(hostname) && !nonmatching_hosts.includes(hostname)) {
            if (table_rows[i].style.display === "none"){
                nonmatching_hosts.push(hostname);
            }
        }
    }

    for (let i = 0; i < matching_hosts.length; i++) {
        let li = document.createElement("li");
        let text_node = document.createTextNode(matching_hosts[i]);
        li.appendChild(text_node);
        new_host_match_ol.appendChild(li)
    }
    
    for (let i = 0; i < nonmatching_hosts.length; i++) {
        let li = document.createElement("li");
        let text_node = document.createTextNode(nonmatching_hosts[i]);
        li.appendChild(text_node);
        new_host_nonmatch_ol.appendChild(li)
    }

    new_host_match_ol.setAttribute("id", "host-match-ol");
    new_host_nonmatch_ol.setAttribute("id", "host-nonmatch-ol");

    old_host_match_ol.parentNode.replaceChild(new_host_match_ol, old_host_match_ol);
    old_host_nonmatch_ol.parentNode.replaceChild(new_host_nonmatch_ol, old_host_nonmatch_ol);

}

const onHostCountBadgeClicked = (event) => {
    const hostCountSpan = event.currentTarget;
    const table = hostCountSpan.closest('table');
    updateHostMatchModal(table);
    showModal("host-match-modal");
}

const getParentTableId = (element) => {
    let parent = element.parentNode;
    let tagName = "table";
    while (parent) {
        if (parent.tagName && parent .tagName.toLowerCase() === tagName) {
            return parent .id;
        }
        else {
            parent = parent .parentNode;
        }
    }
}

const enableModalEventListeners = () => {
    const infoButtons = document.getElementsByClassName('info-button');
    const modals = document.getElementsByClassName('modal');
    const host_count_badges = document.getElementsByClassName('host-count-badge');
    
    //Enable info buttons with "showModal()"
    for (let i = 0; i < infoButtons.length; i++) {
        infoButtons[i].addEventListener('click', function(event) {
            let infoButtonId = event.target.id;
            let sectionIdPrefix = infoButtonId.replace("InfoBtn", "");
            let modalId = sectionIdPrefix.concat("Modal");
            showModal(modalId);
        })
    }
    //Enable modal X buttons with "closeModal()"
    for (let i = 0; i < modals.length; i++) {
        let modal = modals[i];
        let modalCloseBtn = modal.getElementsByClassName("close")[0];
        modalCloseBtn.addEventListener('click', function(event) {
            let modalId = modal.id;
            closeModal(modalId);
        })
    }

    //Enable click outside modal to "closeModal()"
    window.addEventListener('click', function(event) {
        if (event.target.className === "modal") {
            let modal = document.getElementById(event.target.id);
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }
    })

    //Enable Host Count Match and Non Match modal
    for (let i = 0; i < host_count_badges.length; i++) {
        host_count_badges[i].addEventListener('click', function(event) {
            onHostCountBadgeClicked(event);
        })
    }

}



window.onload = enableModalEventListeners()