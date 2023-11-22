document.getElementById('requirementForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const requirements = document.getElementById('requirements').value;
    const data = { requirements: requirements };
    const spinner = document.getElementById('spinner');

    spinner.style.display = 'block';

    fetch('/api/session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        spinner.style.display = 'none';
        window.location.href = data.web_pages[0].url;
    })
    .catch((error) => {
        console.error('Error:', error);

        spinner.style.display = 'none';
    });
});
