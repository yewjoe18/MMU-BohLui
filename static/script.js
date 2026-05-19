// SHOW CURRENT DATE
window.onload = function () {

    let today = new Date();

    let date = today.toDateString();

    let dateText = document.getElementById("current-date");

    if (dateText) {
        dateText.innerHTML = "Today's Date: " + date;
    }

};


// ================================
// FORM VALIDATION
// ================================

function validateForm() {

    let amount = document.getElementById("amount").value;

    let description = document.getElementById("description").value;

    let category = document.getElementById("category").value;


    // EMPTY CHECK
    if (amount === "") {

        alert("Please enter expense amount.");

        return false;
    }


    // NEGATIVE VALUE CHECK
    if (amount <= 0) {

        alert("Expense amount must be greater than RM 0.");

        return false;
    }


    // DESCRIPTION CHECK
    if (description.length < 3) {

        alert("Description must contain at least 3 characters.");

        return false;
    }


    // CATEGORY CHECK
    if (category === "") {

        alert("Please select a category.");

        return false;
    }


    // SUCCESS MESSAGE
    alert("Expense added successfully!");

    return true;
}


// ================================
// CHARACTER COUNTER
// ================================

function countCharacters() {

    let description = document.getElementById("description").value;

    let counter = document.getElementById("char-count");

    counter.innerHTML =
        description.length + " characters entered";

}


// ================================
// INPUT HIGHLIGHT EFFECT
// ================================

function highlightInput(element) {

    element.style.border = "2px solid #2563eb";

}


function removeHighlight(element) {

    element.style.border = "1px solid #ccc";

}


// ================================
// RESET CONFIRMATION
// ================================

function confirmReset() {

    let result = confirm(
        "Are you sure you want to clear the form?"
    );

    if (result === true) {

        document.getElementById("expense-form").reset();

        document.getElementById("char-count").innerHTML =
            "0 characters entered";
    }

}


// ================================
// MMU BohLui JavaScript
// ================================


// SHOW CURRENT DATE
window.onload = function () {

    let today = new Date();

    let date = today.toDateString();

    let currentDate =
        document.getElementById("current-date");

    if (currentDate) {

        currentDate.innerHTML =
            "Today's Date: " + date;
    }

};


// ================================
// FORM VALIDATION
// ================================

function validateForm() {

    let amount =
        document.getElementById("amount").value;

    let description =
        document.getElementById("description").value;

    // EMPTY CHECK
    if (amount === "") {

        alert("Please enter expense amount.");

        return false;
    }

    // NEGATIVE VALUE CHECK
    if (amount <= 0) {

        alert("Expense amount must be greater than 0.");

        return false;
    }

    // DESCRIPTION LENGTH CHECK
    if (description.length < 3) {

        alert(
            "Description must contain at least 3 characters."
        );

        return false;
    }

    // SUCCESS
    alert("Expense added successfully!");

    return true;
}


// ================================
// CHARACTER COUNTER
// ================================

function countCharacters() {

    let description =
        document.getElementById("description").value;

    let counter =
        document.getElementById("char-count");

    counter.innerHTML =
        description.length + " characters entered";
}


// ================================
// INPUT HIGHLIGHT
// ================================

function highlightInput(element) {

    element.style.border =
        "2px solid #2563eb";
}


function removeHighlight(element) {

    element.style.border =
        "1px solid #ccc";
}


// ================================
// RESET FORM
// ================================

function confirmReset() {

    let result = confirm(
        "Are you sure you want to clear the form?"
    );

    if (result === true) {

        document.getElementById("expense-form").reset();

        document.getElementById("char-count")
            .innerHTML = "0 characters entered";
    }

}
