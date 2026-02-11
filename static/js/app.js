// State Management
let currentFolder = null;
let currentTask = null;
let completedTasks = JSON.parse(localStorage.getItem('completedTasks') || '{}');

// DOM Elements
const exerciseMenu = document.getElementById('exerciseMenu');
const taskDescription = document.getElementById('taskDescription');
const sqlEditor = document.getElementById('sqlEditor');
const resultsContainer = document.getElementById('resultsContainer');
const rowCount = document.getElementById('rowCount');
const schemaContainer = document.getElementById('schemaContainer');
const toast = document.getElementById('toast');

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    loadExercises();

    // Add keyboard shortcut for running queries (Ctrl+Enter)
    sqlEditor.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            runQuery();
        }
    });
});

// Load all exercises from the server
async function loadExercises() {
    try {
        const response = await fetch('/api/exercises');
        const exercises = await response.json();
        renderExerciseMenu(exercises);
    } catch (error) {
        console.error('Failed to load exercises:', error);
        showToast('Failed to load exercises', 'error');
    }
}

// Render the exercise menu with folders and tasks
function renderExerciseMenu(exercises) {
    exerciseMenu.innerHTML = exercises.map(folder => `
        <div class="exercise-folder" data-folder-id="${folder.id}">
            <div class="folder-header" onclick="toggleFolder('${folder.id}')">
                <span class="folder-icon">▶</span>
                <span class="folder-name">${folder.name}</span>
                <span class="difficulty-badge ${folder.difficulty}">${folder.difficulty}</span>
            </div>
            <div class="task-list" id="tasks-${folder.id}">
                ${folder.tasks.map(task => `
                    <div class="task-item" 
                         data-task-id="${task.id}" 
                         onclick="selectTask('${folder.id}', '${task.id}')">
                        <span class="task-status ${isTaskCompleted(folder.id, task.id) ? 'completed' : ''}">
                            ${isTaskCompleted(folder.id, task.id) ? '✓' : ''}
                        </span>
                        <span class="task-name">${task.title}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

// Toggle folder expansion
function toggleFolder(folderId) {
    const taskList = document.getElementById(`tasks-${folderId}`);
    const folderHeader = taskList.previousElementSibling;

    taskList.classList.toggle('visible');
    folderHeader.classList.toggle('expanded');
}

// Check if a task is completed
function isTaskCompleted(folderId, taskId) {
    return completedTasks[`${folderId}/${taskId}`] === true;
}

// Mark a task as completed
function markTaskCompleted(folderId, taskId) {
    completedTasks[`${folderId}/${taskId}`] = true;
    localStorage.setItem('completedTasks', JSON.stringify(completedTasks));

    // Update UI
    const taskItem = document.querySelector(
        `.exercise-folder[data-folder-id="${folderId}"] .task-item[data-task-id="${taskId}"] .task-status`
    );
    if (taskItem) {
        taskItem.classList.add('completed');
        taskItem.textContent = '✓';
    }
}

// Select a task
async function selectTask(folderId, taskId) {
    currentFolder = folderId;
    currentTask = taskId;

    // Update active state in menu
    document.querySelectorAll('.task-item').forEach(item => {
        item.classList.remove('active');
    });
    const activeItem = document.querySelector(
        `.exercise-folder[data-folder-id="${folderId}"] .task-item[data-task-id="${taskId}"]`
    );
    if (activeItem) {
        activeItem.classList.add('active');
    }

    // Expand the folder if not already
    const taskList = document.getElementById(`tasks-${folderId}`);
    const folderHeader = taskList.previousElementSibling;
    if (!taskList.classList.contains('visible')) {
        taskList.classList.add('visible');
        folderHeader.classList.add('expanded');
    }

    // Load task details
    try {
        const response = await fetch(`/api/task/${folderId}/${taskId}`);
        const data = await response.json();

        renderTaskDescription(data.task);
        renderSchema(data.db_structure);

        // Clear editor and results
        sqlEditor.value = '';
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">🔍</span>
                <p>Run a query to see results</p>
            </div>
        `;
        rowCount.textContent = '';

    } catch (error) {
        console.error('Failed to load task:', error);
        showToast('Failed to load task', 'error');
    }
}

// Render task description
function renderTaskDescription(task) {
    let html = `
        <h3>${task.title}</h3>
        <p>${task.description}</p>
    `;

    if (task.hint) {
        html += `<div class="task-hint">💡 <strong>Hint:</strong> ${task.hint}</div>`;
    }

    taskDescription.innerHTML = html;
}

// Render database schema
function renderSchema(structure) {
    if (!structure || structure.length === 0) {
        schemaContainer.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📁</span>
                <p>No schema available</p>
            </div>
        `;
        return;
    }

    schemaContainer.innerHTML = structure.map(table => `
        <div class="schema-table">
            <div class="schema-table-header">
                <span class="icon">📋</span>
                ${table.name}
            </div>
            <div class="schema-columns">
                ${table.columns.map(col => `
                    <div class="schema-column">
                        <span class="column-name">${col.name}</span>
                        <span class="column-type">${col.type || 'TEXT'}</span>
                        ${col.pk ? '<span class="pk-badge">PK</span>' : ''}
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

// Run SQL query
async function runQuery() {
    const query = sqlEditor.value.trim();

    if (!query) {
        showToast('Please enter a SQL query', 'error');
        return;
    }

    if (!currentFolder) {
        showToast('Please select a task first', 'error');
        return;
    }

    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                folder_id: currentFolder,
                query: query
            })
        });

        const data = await response.json();

        if (data.success) {
            renderResults(data.columns, data.rows);
            rowCount.textContent = `${data.row_count} row${data.row_count !== 1 ? 's' : ''}`;
        } else {
            resultsContainer.innerHTML = `
                <div class="error-message">
                    ❌ ${data.error}
                </div>
            `;
            rowCount.textContent = '';
        }
    } catch (error) {
        console.error('Failed to execute query:', error);
        showToast('Failed to execute query', 'error');
    }
}

// Render query results as a table
function renderResults(columns, rows) {
    if (!columns || columns.length === 0) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">✅</span>
                <p>Query executed successfully (no results)</p>
            </div>
        `;
        return;
    }

    let html = `
        <table class="results-table">
            <thead>
                <tr>
                    ${columns.map(col => `<th>${col}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
                ${rows.map(row => `
                    <tr>
                        ${columns.map(col => `<td>${row[col] !== null ? row[col] : '<em>NULL</em>'}</td>`).join('')}
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    resultsContainer.innerHTML = html;
}

// Verify the solution
async function verifyTask() {
    const query = sqlEditor.value.trim();

    if (!query) {
        showToast('Please enter a SQL query', 'error');
        return;
    }

    if (!currentFolder || !currentTask) {
        showToast('Please select a task first', 'error');
        return;
    }

    try {
        const response = await fetch('/api/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                folder_id: currentFolder,
                task_id: currentTask,
                query: query
            })
        });

        const data = await response.json();

        if (data.correct) {
            markTaskCompleted(currentFolder, currentTask);
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Failed to verify solution:', error);
        showToast('Failed to verify solution', 'error');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastIcon = toast.querySelector('.toast-icon');
    const toastMessage = toast.querySelector('.toast-message');

    toast.className = `toast ${type}`;
    toastIcon.textContent = type === 'success' ? '✓' : '✗';
    toastMessage.textContent = message;

    toast.classList.add('visible');

    setTimeout(() => {
        toast.classList.remove('visible');
    }, 3000);
}
