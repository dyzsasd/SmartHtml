document.addEventListener('DOMContentLoaded', function() {
    const checkInterval = 1000; // Check every 1 second
    const apiUrl = document.querySelector('meta[name="get-session-url"]').getAttribute('content');
    const demoUrl = document.querySelector('meta[name="demo-url"]').getAttribute('content');

    function checkTaskStatus() {
        fetch(apiUrl) // Use the URL from the meta tag
            .then(response => response.json())
            .then(data => {
                if (data.is_processing === 'completed') {
                    window.location.href = demoUrl; // Redirect to the demo page
                }
            })
            .catch(error => console.error('Error:', error));
    }

    setInterval(checkTaskStatus, checkInterval);
});