document.getElementById('requirementForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const requirements = document.getElementById('requirements').value;
    const data = { requirements: requirements };
    const spinnerWrapper = document.getElementById('spinnerWrapper');

    // Show spinner wrapper
    spinnerWrapper.style.display = 'flex';
    requirements.disabled = true; // Disable the textarea

    fetch('/api/session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        // Hide spinner and re-enable the textarea
        spinnerWrapper.style.display = 'none';
        requirements.disabled = false;
        window.location.href = data.web_pages[0].url;
    })
    .catch((error) => {
        console.error('Error:', error);

        // Hide spinner and re-enable the textarea in case of error
        spinnerWrapper.style.display = 'none';
        requirements.disabled = false;
    });
});
