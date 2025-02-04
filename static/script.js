document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('daysInput').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent form submission if inside a form
            generatePlan();
        }
    });
});

function generatePlan() {
    const days = document.getElementById('daysInput').value;
    const goal = document.getElementById('goalInput').value;  // Get the selected goal

    fetch('/generate_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            days: days,
            goal: goal  // Include goal in the POST request
        })
    })
    .then(response => response.json())
    .then(data => {
        const outputDiv = document.getElementById('planOutput');
        if (data.error) {
            outputDiv.innerHTML = `<p>${data.error}</p>`;
        } else {
            outputDiv.innerHTML = `<p>Your ${days}-day workout plan is:</p><ul>${data.plan.map(day => `<li>${day}</li>`).join('')}</ul>`;
        }
    })
    .catch(error => console.error('Error:', error));
}
