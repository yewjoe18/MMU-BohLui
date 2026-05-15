// 等待整个网页加载完毕后再执行魔法
document.addEventListener('DOMContentLoaded', function() {
    
    // 抓取页面上的表单和输入钱币的框框
    const expenseForm = document.querySelector('form');
    const amountInput = document.querySelector('input[name="amount"]');

    // 如果当前页面有这个表单，我们就给它装上“监控”
    if (expenseForm && amountInput) {
        expenseForm.addEventListener('submit', function(event) {
            
            // 拿到用户输入的钱
            const amount = parseFloat(amountInput.value);

            // 核心逻辑：如果不填钱，或者填的钱少于等于 0
            if (isNaN(amount) || amount <= 0) {
                
                // 1. 马上阻止表单提交（不让数据飞去 Yee Seng 的后端）
                event.preventDefault(); 
                
                // 2. 弹出一个友好的警告
                alert("Aiyo! The amount must be more than RM 0 lah! 别乱填~");
                
                // 3. 把输入框的边框变成显眼的红色，提醒用户改错
                amountInput.style.border = "2px solid red";
                amountInput.style.backgroundColor = "#ffe6e6"; // 背景变浅红
                
            } else {
                // 如果填对了，就把边框颜色变回正常（绿色代表通行）
                amountInput.style.border = "2px solid #28a745";
                amountInput.style.backgroundColor = "white";
            }
        });
    }
});