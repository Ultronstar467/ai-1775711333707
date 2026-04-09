```javascript
document.addEventListener('DOMContentLoaded', () => {
    const num1Input = document.getElementById('num1');
    const num2Input = document.getElementById('num2');
    const operatorSelect = document.getElementById('operator');
    const calculateBtn = document.getElementById('calculateBtn');
    const resultDisplay = document.getElementById('result');

    // Function to perform the calculation via API
    const performCalculation = async () => {
        const num1 = parseFloat(num1Input.value);
        const num2 = parseFloat(num2Input.value);
        const operator = operatorSelect.value;

        // Basic client-side validation
        if (isNaN(num1) || isNaN(num2)) {
            resultDisplay.textContent = 'Please enter valid numbers.';
            resultDisplay.style.color = 'var(--error-color)';
            return;
        }

        resultDisplay.textContent = 'Calculating...';
        resultDisplay.style.color = 'var(--secondary-text)';

        try {
            // Use relative path for the API endpoint
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num1: num1,
                    num2: num2,
                    operator: operator,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                resultDisplay.textContent = `${data.result}`;
                resultDisplay.style.color = 'var(--success-color)';
            } else {
                resultDisplay.textContent = `Error: ${data.error || 'Something went wrong.'}`;
                resultDisplay.style.color = 'var(--error-color)';
            }
        } catch (error) {
            console.error('Fetch error:', error);
            resultDisplay.textContent = 'Network error. Please try again.';
            resultDisplay.style.color = 'var(--error-color)';
        }
    };

    // Event listener for the calculate button
    calculateBtn.addEventListener('click', performCalculation);

    // Optional: Add event listeners to input fields for 'Enter' key press
    num1Input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performCalculation();
    });
    num2Input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performCalculation();
    });
    operatorSelect.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performCalculation();
    });
});
```

---