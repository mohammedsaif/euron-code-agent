// Adapted from LucioFex/Simple-Web-Calculator (MIT)

(function () {
    "use strict";

    var currentInput = "0";
    var previousInput = "";
    var operator = null;
    var shouldResetScreen = false;

    var screenBottom = document.getElementById("screen-bottom-display");
    var screenTop = document.getElementById("screen-top-display");

    function updateScreen() {
        screenBottom.textContent = currentInput;
    }

    function appendNumber(num) {
        if (currentInput === "0" && num !== ".") {
            currentInput = num;
        } else if (num === "." && currentInput.indexOf(".") !== -1) {
            return;
        } else {
            currentInput += num;
        }
        updateScreen();
    }

    function calculate(a, op, b) {
        var numA = parseFloat(a);
        var numB = parseFloat(b);
        if (isNaN(numA) || isNaN(numB)) return "Error";
        switch (op) {
            case "+": return numA + numB;
            case "-": return numA - numB;
            case "*": return numA * numB;
            case "/":
                if (numB === 0) return "Error";
                return numA / numB;
            default: return "Error";
        }
    }

    function handleOperator(nextOp) {
        if (operator !== null && !shouldResetScreen) {
            currentInput = String(calculate(previousInput, operator, currentInput));
        }
        previousInput = currentInput;
        operator = nextOp;
        shouldResetScreen = true;
        screenTop.textContent = previousInput + " " + operatorSymbol(nextOp);
    }

    function operatorSymbol(op) {
        switch (op) {
            case "+": return "+";
            case "-": return "\u2212";
            case "*": return "\u00d7";
            case "/": return "\u00f7";
            default: return op;
        }
    }

    function handleEqual() {
        if (operator === null) return;
        var result = calculate(previousInput, operator, currentInput);
        currentInput = String(result);
        operator = null;
        previousInput = "";
        shouldResetScreen = false;
        screenTop.textContent = "";
        updateScreen();
    }

    function handleClear() {
        currentInput = "0";
        previousInput = "";
        operator = null;
        shouldResetScreen = false;
        screenTop.textContent = "";
        updateScreen();
    }

    function handleDelete() {
        if (currentInput.length === 1 || currentInput === "Error") {
            currentInput = "0";
        } else {
            currentInput = currentInput.slice(0, -1);
        }
        updateScreen();
    }

    function handlePercent() {
        var num = parseFloat(currentInput);
        if (isNaN(num)) return;
        currentInput = String(num / 100);
        updateScreen();
    }

    /* Wire up buttons */
    var numbers = document.querySelectorAll(".number");
    for (var i = 0; i < numbers.length; i++) {
        (function (btn) {
            btn.addEventListener("click", function () {
                if (shouldResetScreen) {
                    currentInput = "";
                    shouldResetScreen = false;
                }
                appendNumber(btn.id);
            });
        })(numbers[i]);
    }

    document.getElementById("add").addEventListener("click", function () { handleOperator("+"); });
    document.getElementById("subtract").addEventListener("click", function () { handleOperator("-"); });
    document.getElementById("multiply").addEventListener("click", function () { handleOperator("*"); });
    document.getElementById("divide").addEventListener("click", function () { handleOperator("/"); });
    document.getElementById("equal").addEventListener("click", handleEqual);
    document.getElementById("clear-all").addEventListener("click", handleClear);
    document.getElementById("del").addEventListener("click", handleDelete);
    document.getElementById("percent").addEventListener("click", handlePercent);

    /* Keyboard support */
    document.addEventListener("keydown", function (e) {
        var key = e.key;
        if (key >= "0" && key <= "9") {
            if (shouldResetScreen) { currentInput = ""; shouldResetScreen = false; }
            appendNumber(key);
        } else if (key === ".") {
            if (shouldResetScreen) { currentInput = ""; shouldResetScreen = false; }
            appendNumber(".");
        } else if (key === "+") { handleOperator("+"); }
        else if (key === "-") { handleOperator("-"); }
        else if (key === "*") { handleOperator("*"); }
        else if (key === "/") { e.preventDefault(); handleOperator("/"); }
        else if (key === "%") { handlePercent(); }
        else if (key === "Enter" || key === "=") { handleEqual(); }
        else if (key === "Backspace") { handleDelete(); }
        else if (key === "Escape" || key === "Delete") { handleClear(); }
    });
})();
