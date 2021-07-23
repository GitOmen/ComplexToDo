const API_URL = 'http://127.0.0.1:5000'

export const STATUSES = {
    SCHEDULED: "Scheduled",
    IN_PROGRESS: "In Progress",
    FINISHED: "Finished"
}

export async function fetchTask(id) {
    return await (await fetch(`${API_URL}/tasks/${id}`)).json();
}

export async function fetchAllTasks() {
    return await (await fetch(`${API_URL}/tasks`)).json();
}

export async function createTask(data) {
    return await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    });
}

export async function updateTask(data) {
    return await fetch(`${API_URL}/tasks/${data.id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    });
}

export async function removeTask(id) {
    return await fetch(`${API_URL}/tasks/${id}`, {
        method: 'DELETE',
    });
}
