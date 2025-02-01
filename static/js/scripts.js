document.addEventListener('DOMContentLoaded', function () {
    const toggleButtons = document.querySelectorAll('.toggle-complete');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.getAttribute('data-task-id');
            fetch(`/toggle_complete/${taskId}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    
                    location.reload();  
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});