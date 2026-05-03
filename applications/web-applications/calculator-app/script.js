class Calculator {
    constructor() {
        this.display = document.getElementById('display');
        this.currentValue = '0';
        this.previousValue = '';
        this.operator = '';
        this.shouldResetDisplay = false;
        
        this.updateDisplay();
    }

    updateDisplay() {
        this.display.textContent = this.currentValue;
    }

    clearDisplay() {
        this.currentValue = '0';
        this.previousValue = '';
        this.operator = '';
        this.shouldResetDisplay = false;
        this.updateDisplay();
    }

    appendNumber(number) {
        if (this.shouldResetDisplay) {
            this.currentValue = '';
            this.shouldResetDisplay = false;
        }
        
        if (this.currentValue === '0') {
            this.currentValue = number;
        } else if (this.currentValue.length < 12) { // Limit display length
            this.currentValue += number;
        }
        
        this.updateDisplay();
    }

    appendDecimal() {
        if (this.shouldResetDisplay) {
            this.currentValue = '0';
            this.shouldResetDisplay = false;
        }
        
        if (!this.currentValue.includes('.')) {
            this.currentValue += '.';
        }
        
        this.updateDisplay();
    }

    appendOperator(op) {
        if (this.operator && !this.shouldResetDisplay) {
            this.calculate();
        }
        
        this.previousValue = this.currentValue;
        this.operator = op;
        this.shouldResetDisplay = true;
    }

    deleteLastDigit() {
        if (this.currentValue.length > 1) {
            this.currentValue = this.currentValue.slice(0, -1);
        } else {
            this.currentValue = '0';
        }
        
        this.updateDisplay();
    }

    calculate() {
        if (!this.operator || !this.previousValue) return;
        
        const prev = parseFloat(this.previousValue);
        const current = parseFloat(this.currentValue);
        let result;
        
        switch (this.operator) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '*':
                result = prev * current;
                break;
            case '/':
                if (current === 0) {
                    this.showError('Cannot divide by zero');
                    return;
                }
                result = prev / current;
                break;
            default:
                return;
        }
        
        // Handle floating point precision
        result = Math.round(result * 100000000) / 100000000;
        
        // Handle very large numbers
        if (Math.abs(result) > 999999999999) {
            this.showError('Number too large');
            return;
        }
        
        this.currentValue = result.toString();
        this.operator = '';
        this.previousValue = '';
        this.shouldResetDisplay = true;
        this.updateDisplay();
    }

    showError(message) {
        this.display.textContent = message;
        this.currentValue = '0';
        this.previousValue = '';
        this.operator = '';
        this.shouldResetDisplay = true;
        
        setTimeout(() => {
            this.updateDisplay();
        }, 2000);
    }
}

// Global functions for button onclick handlers
let calculator;

function clearDisplay() {
    calculator.clearDisplay();
}

function appendNumber(number) {
    calculator.appendNumber(number);
}

function appendDecimal() {
    calculator.appendDecimal();
}

function appendOperator(operator) {
    calculator.appendOperator(operator);
}

function deleteLastDigit() {
    calculator.deleteLastDigit();
}

function calculate() {
    calculator.calculate();
}

// Initialize calculator when page loads
document.addEventListener('DOMContentLoaded', function() {
    calculator = new Calculator();
    
    // Add keyboard support
    document.addEventListener('keydown', function(event) {
        const key = event.key;
        
        if (key >= '0' && key <= '9') {
            appendNumber(key);
        } else if (key === '.') {
            appendDecimal();
        } else if (key === '+' || key === '-' || key === '*' || key === '/') {
            appendOperator(key);
        } else if (key === 'Enter' || key === '=') {
            event.preventDefault();
            calculate();
        } else if (key === 'Escape' || key === 'c' || key === 'C') {
            clearDisplay();
        } else if (key === 'Backspace') {
            deleteLastDigit();
        }
    });
    
    // Add touch feedback for mobile
    const buttons = document.querySelectorAll('.button');
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('touchend', function() {
            this.style.transform = '';
        });
    });
});