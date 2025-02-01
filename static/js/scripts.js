 document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons = document.querySelectorAll(".toggle-complete");

    toggleButtons.forEach(button => {
        button.addEventListener('click', function () {
            let taskID = this.getAttribute('data-task-id');
            fetch(`/toggle_complete/${taskID}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload(); 
                } else {
                    alert('Failed to update task');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
 });
