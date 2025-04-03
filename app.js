// Base API URLs
const BASE_URL = "http://localhost:8000";
const TASK_API = `${BASE_URL}/tasks`;
const USER_API = `${BASE_URL}/users`;
const TASK_HISTORY_API = `${BASE_URL}/task-history`;
const CATEGORY_API = `${BASE_URL}/categories`;

// Auth Token (You would retrieve this upon login and store it, e.g., in localStorage or a cookie)
let authToken = localStorage.getItem("authToken");

// Generic function to make authenticated requests
function authenticatedFetch(url, options = {}) {
  if (!authToken) {
    console.error("User not authenticated. Please log in.");
    return;
  }

  options.headers = options.headers || {};
  options.headers["Authorization"] = `Bearer ${authToken}`;
  return fetch(url, options).then((response) => {
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    return response.json();
  });
}

// =============================================================
// 1. User Management API
// =============================================================

function loginUser(email, password) {
  fetch(`${USER_API}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Explicitly set Content-Type
    },
    body: JSON.stringify({ email, password }), // Properly stringify the payload
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to log in. Check credentials.");
      }
      return response.json();
    })
    .then((data) => {
      // Store the token and inform the user
      authToken = data.access_token;
      localStorage.setItem("authToken", authToken);
      console.log("Login successful:", data);
      document.getElementById("login-message").textContent = "Logged in successfully!";
    })
    .catch((error) => {
      console.error("Error logging in:", error);
      document.getElementById("login-message").textContent = "Login failed. Check credentials.";
    });
}

// Register User
function registerUser(name, email, password) {
  fetch(`${USER_API}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  })
    .then((response) => response.json())
    .then((data) => console.log("User registered successfully:", data))
    .catch((error) => console.error("Error registering user:", error));
}

// Update User
function updateUser(userId, name, email, password) {
  authenticatedFetch(`${USER_API}/update/${userId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  })
    .then((data) => console.log("User updated successfully:", data))
    .catch((error) => console.error("Error updating user:", error));
}

// Delete User
function deleteUser(userId) {
  authenticatedFetch(`${USER_API}/delete/${userId}`, { method: "DELETE" })
    .then((data) => console.log(data.message))
    .catch((error) => console.error("Error deleting user:", error));
}

// =============================================================
// 2. Task Management API
// =============================================================

// Fetch Tasks
function fetchTasks() {
  authenticatedFetch(TASK_API)
    .then((tasks) => {
      // Render tasks in your UI
      console.log("Fetched tasks:", tasks);
    })
    .catch((error) => console.error("Error fetching tasks:", error));
}

// Add New Task
function addTask(taskName, taskDescription, userId, dueDate, priority, categoryId) {
  authenticatedFetch(`${TASK_API}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      task_name: taskName,
      task_description: taskDescription,
      user_id: userId,
      due_date: dueDate,
      priority: priority,
      category_id: categoryId,
    }),
  })
    .then((data) => console.log("Task added successfully:", data))
    .catch((error) => console.error("Error adding task:", error));
}

// Update Task
function updateTask(taskId, updates) {
  authenticatedFetch(`${TASK_API}/update/${taskId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates),
  })
    .then((data) => console.log("Task updated successfully:", data))
    .catch((error) => console.error("Error updating task:", error));
}

// Delete Task
function deleteTask(taskId) {
  authenticatedFetch(`${TASK_API}/delete/${taskId}`, { method: "DELETE" })
    .then((data) => console.log(data.message))
    .catch((error) => console.error("Error deleting task:", error));
}

// Execute Task
function executeTask(taskId) {
  authenticatedFetch(`${TASK_API}/execute/${taskId}`)
    .then((data) => console.log("Task executed successfully:", data))
    .catch((error) => console.error("Error executing task:", error));
}

// =============================================================
// 3. Task History
// =============================================================

// Fetch Task History
function fetchTaskHistory() {
  authenticatedFetch(TASK_HISTORY_API)
    .then((taskHistory) => console.log("Task history fetched:", taskHistory))
    .catch((error) => console.error("Error fetching task history:", error));
}

// Fetch Task History by Task ID
function fetchTaskHistoryByTaskId(taskId, userId) {
  authenticatedFetch(`${TASK_HISTORY_API}/task/${taskId}`)
    .then((history) => console.log("Task history for task:", history))
    .catch((error) => console.error("Error fetching task history:", error));
}

// =============================================================
// 4. Category Management API
// =============================================================

// Fetch Categories
function fetchCategories() {
  authenticatedFetch(CATEGORY_API)
    .then((categories) => console.log("Fetched categories:", categories))
    .catch((error) => console.error("Error fetching categories:", error));
}

// Add Category
function addCategory(categoryName, categoryDescription, userId) {
  authenticatedFetch(`${CATEGORY_API}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      category_name: categoryName,
      category_description: categoryDescription,
      user_id: userId,
    }),
  })
    .then((data) => console.log("Category added successfully:", data))
    .catch((error) => console.error("Error adding category:", error));
}

// Update Category
function updateCategory(categoryId, name, description, userId) {
  authenticatedFetch(`${CATEGORY_API}/update/${categoryId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      category_name: name,
      category_description: description,
      user_id: userId,
    }),
  })
    .then((data) => console.log("Category updated successfully:", data))
    .catch((error) => console.error("Error updating category:", error));
}

// Delete Category
function deleteCategory(categoryId, userId) {
  authenticatedFetch(`${CATEGORY_API}/delete/${categoryId}`, {
    method: "DELETE",
  })
    .then((data) => console.log(data.message))
    .catch((error) => console.error("Error deleting category:", error));
}

// =============================================================
// Initialize the App
// =============================================================

function initializeApp() {
  const isAuthenticated = !!authToken;
  if (isAuthenticated) {
    console.log("User authenticated. Fetching tasks...");
    fetchTasks();
  } else {
    console.log("User not authenticated. Please log in.");
  }
}

// Initialize app when the page loads
initializeApp();