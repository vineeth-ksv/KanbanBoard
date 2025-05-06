// Global card_ids variable - will be initialized from the template
let card_ids = [];

// Function to initialize card_ids from template data
function initCardIds(ids) {
    card_ids = ids;
}

// Function to handle category view card dropdowns
function showDropdown_cards(card_id) {
    // Close all other open dropdowns first
    closeAllDropdowns_cards();
    
    // Open the selected dropdown
    const dropdown = document.getElementById("myDropdown-c" + card_id);
    if (dropdown) {
        dropdown.classList.toggle("show");
    }
}

// Close all card dropdowns in category view
function closeAllDropdowns_cards() {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (let j = 0; j < dropdowns.length; j++) {
        var openDropdown = dropdowns[j];
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
        }
    }
}

// Function to update the completed checkbox based on the status dropdown
function updateCompletedStatus(cardId) {
    const statusDropdown = document.getElementById(`status-${cardId}`);
    const completedCheckbox = document.getElementById(`completed_status-${cardId}`);
    
    // If status is "Completed", check the completed checkbox
    if (statusDropdown && completedCheckbox) {
        if (statusDropdown.value === "Completed") {
            completedCheckbox.checked = true;
        } else {
            completedCheckbox.checked = false;
        }
    }
}

// Initialize Bootstrap 5 components and handle Bootstrap 5 dropdowns
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap 5 components
    if (typeof bootstrap !== 'undefined') {
        // Initialize modals
        var modalElements = [].slice.call(document.querySelectorAll('.modal'));
        modalElements.forEach(function(modalEl) {
            new bootstrap.Modal(modalEl);
        });
        
        // Initialize Bootstrap 5 dropdowns
        var dropdownElements = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));
        dropdownElements.forEach(function(dropdownEl) {
            new bootstrap.Dropdown(dropdownEl);
        });
    }
    
    // Initialize Bootstrap 4 components if jQuery is available
    if (typeof $ !== 'undefined') {
        // Bootstrap 4 modals will initialize automatically with jQuery
        $('[data-toggle="modal"]').modal({show: false});
    }
    
    // Set up event listeners for synchronizing status and completed checkbox
    if (card_ids && card_ids.length > 0) {
        card_ids.forEach(function(cardId) {
            const checkbox = document.getElementById(`completed_status-${cardId}`);
            const statusDropdown = document.getElementById(`status-${cardId}`);
            
            if (checkbox && statusDropdown) {
                checkbox.addEventListener('change', function() {
                    if (this.checked) {
                        statusDropdown.value = "Completed";
                    } else if (statusDropdown.value === "Completed") {
                        statusDropdown.value = "In-Progress";
                    }
                });
                
                // Initialize the relationship at page load
                updateCompletedStatus(cardId);
            }
        });
    }
});

// Single window.onclick event handler for the custom dropdowns in category view
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        closeAllDropdowns_cards();
    }
};

// Validate date for card deadline
function validateDate(id) {
    var UserDate = document.getElementById('card_deadline-'+id).value;
    var ToDate = new Date();

    if (new Date(UserDate).getTime() < ToDate.getTime()) {
        alert("The deadline cannot be before today's date");
        return false;
    }
    return true;
}