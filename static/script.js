window.onload = function () {
    // ==========================================
    // 1. 你们原本的功能：显示日期
    // ==========================================
    let today = new Date();
    let date = today.toDateString();
    let dateText = document.getElementById("current-date");

    if (dateText) {
        dateText.innerHTML = "Today's Date: " + date;
    }

    // ==========================================
    // 2. 🌟 新增的功能：深色模式切换逻辑
    // ==========================================
    const themeToggleBtn = document.getElementById('themeToggle');
    const body = document.body;

    // 加入一个 if 判断，确保只有在有切换按钮的页面才执行，避免报错
    if (themeToggleBtn) {
        // 检查本地存储中是否有用户之前保存的主题设置
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme === 'dark') {
            body.classList.add('dark-mode');
            themeToggleBtn.innerText = '☀️ Light Mode';
        }

        // 当点击按钮时切换模式
        themeToggleBtn.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('theme', 'dark');
                themeToggleBtn.innerText = '☀️ Light Mode';
            } else {
                localStorage.setItem('theme', 'light');
                themeToggleBtn.innerText = '🌙 Dark Mode';
            }
        });
    }
};

// ==========================================
// 下面的 function 完全保持你们原本的样子，一字未动
// ==========================================

function validateAuthForm() {
    let name = document.getElementById("student_name").value;
    let email = document.getElementById("student_email").value;

    if (name.trim().length < 3) {
        alert("Student Name must be at least 3 characters long.");
        return false; 
    }

    let emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address (e.g., yourname@gmail.com).");
        return false; 
    }

    return true; 
}

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

function countCharacters() {
    let description = document.getElementById("description").value;
    let counter = document.getElementById("char-count");
    
    if (counter) {
        counter.innerHTML = description.length + " characters entered";
    }
}

function highlightInput(element) {
    element.style.border = "2px solid #2563eb";
}

function removeHighlight(element) {
    element.style.border = "1px solid #ccc";
}

function confirmReset() {
    let result = confirm("Are you sure you want to clear the form?");
    
    if (result === true) {
        document.getElementById("expense-form").reset();
        let counter = document.getElementById("char-count");
        if (counter) {
            counter.innerHTML = "0 characters entered";
        }
    }
}