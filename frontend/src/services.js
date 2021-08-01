const API_URL = 'http://127.0.0.1:5000'

export const DEFAULT_STATUS = "SCHEDULED"

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

export async function fetchTaskList(id) {
    return await (await fetch(`${API_URL}/lists/${id}`)).json();
}

export async function fetchTaskListTasks(id) {
    return await (await fetch(`${API_URL}/lists/${id}/tasks`)).json();
}

export async function fetchAllTaskLists() {
    return await (await fetch(`${API_URL}/lists`)).json();
}

export async function createTaskList(data) {
    return (await fetch(`${API_URL}/lists`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })).json();
}

export async function updateTaskList(data) {
    return (await fetch(`${API_URL}/lists/${data.id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })).json();
}

export async function removeTaskList(id) {
    return await fetch(`${API_URL}/lists/${id}`, {
        method: 'DELETE',
    });
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
