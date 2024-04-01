let currentCategory = 'Daily'; // Default category

document.addEventListener('DOMContentLoaded', () => {
    changeCategory(currentCategory); // Initial category load
});

function changeCategory(category) {
    currentCategory = category;
    document.getElementById('subcategories').innerHTML = ''; // Reset subcategories
    if (category === 'Daily') {
        const subcategories = ['Animals', 'Home'];
        subcategories.forEach(sub => {
            let button = document.createElement('button');
            button.innerText = sub;
            button.onclick = () => fetchTasks(sub);
            document.getElementById('subcategories').appendChild(button);
        });
        fetchTasks(subcategories[0]); // Default to first subcategory
    } else if (category === 'Weekly') {
        fetchTasks(); // No subcategories for weekly
    }
}

function fetchTasks(subcategory = '') {
    // Replace `/tasks` with the correct endpoint to fetch tasks
    // Add query parameters as needed based on category and subcategory
    let url = `/tasks?category=${currentCategory}`;
    if (subcategory) url += `&subcategory=${subcategory}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tasksList = document.getElementById('tasks-list');
            tasksList.innerHTML = ''; // Clear existing tasks
            data.forEach(task => {
                let li = document.createElement('li');
                li.textContent = `${task.description} - Details: ${task.details || 'None'}`;
                tasksList.appendChild(li);
            });
        });
}

function addTask() {
    const description = document.getElementById('task-description').value;
    const details = document.getElementById('task-details').value;
    const order = parseInt(document.getElementById('task-order').value);
    const category = document.getElementById('task-category').value;
    const subcategory = document.getElementById('task-subcategory').value;
    const time_of_day = document.getElementById('time')

    const taskData = {
        description,
        details,
        order,
        category,
        subcategory
    };

    fetch('/task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Task added:', data);
        fetchTasks(); // Refresh the list of tasks
    });
}
