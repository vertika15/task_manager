document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://localhost:8000";

  const loginModal = document.getElementById("loginModal");
  const loginForm = document.getElementById("loginForm");
  const loginMessage = document.getElementById("loginMessage");
  const mainContent = document.getElementById("mainContent");
  const logoutButton = document.getElementById("logoutButton");

  const addTaskForm = document.getElementById("addTaskForm");
  const getTaskForm = document.getElementById("getTaskForm");
  const addCategoryForm = document.getElementById("addCategoryForm");

  // Helper: Get the stored token from localStorage
  const token = () => localStorage.getItem("token");

  // Show/hide modal
  const showLoginModal = () => (loginModal.style.display = "flex");
  const hideLoginModal = () => (loginModal.style.display = "none");

  // Show/hide main content
  const showMainContent = () => mainContent.classList.remove("hidden");
  const hideMainContent = () => mainContent.classList.add("hidden");

  // Function to clear token and reload page
  const logout = () => {
    localStorage.removeItem("token"); // Delete token from localStorage
    window.location.reload(); // Reload the page to reset state
  };

  // Function to check authentication on page load
  const checkAuthentication = () => {
    const authToken = token();
    if (!authToken) {
      showLoginModal();
      hideMainContent();
    } else {
      hideLoginModal();
      showMainContent();
    }
  };

  // Login form submission handler
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent form submission from reloading the page

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
      const response = await fetch(`${API_BASE}/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const result = await response.json();

      if (!response.ok) throw new Error(result.detail || "Login failed");

      localStorage.setItem("token", result.access_token); // Save token
      loginMessage.textContent = "✅ Login successful!";
      loginMessage.className = "success";

      hideLoginModal();
      showMainContent();
    } catch (error) {
      loginMessage.textContent = `❌ ${error.message}`;
      loginMessage.className = "error";
    }
  });

  // Add Task Handler
  // Add Task Handler
addTaskForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(addTaskForm);
  const taskData = Object.fromEntries(formData);

  try {
    // Send the taskData with the additional fields to the API
    const response = await fetch(`${API_BASE}/tasks/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token()}`,
      },
      body: JSON.stringify(taskData), // Include all form data
    });

    const result = await response.json();

    if (!response.ok) throw new Error(result.detail || "Failed to add task");
    alert("Task added successfully!");
    addTaskForm.reset(); // Clear the form
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
});

  // Get Task by ID Handler
  getTaskForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(getTaskForm);
    const taskId = formData.get("taskId");
    const userId = formData.get("userId"); // Get User ID from the form

    try {
      const response = await fetch(`${API_BASE}/tasks/${taskId}?userId=${userId}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token()}`,
        },
      });

      const result = await response.json();

      if (!response.ok) throw new Error(result.detail || "Task not found");

      alert(`Task Retrieved: \n${JSON.stringify(result, null, 2)}`);
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  });

  // Expose this to index, once fixed
const getMyTasksForm = document.getElementById("getMyTasksForm");

getMyTasksForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // Prevent page reload on form submission

  const formData = new FormData(getMyTasksForm);
  const userId = formData.get("userId");

  try {
    const response = await fetch(`${API_BASE}/tasks/my_tasks?user_id=${userId}`, {
  method: "GET",
  headers: {
    Authorization: `Bearer ${token()}`,
  },
});

    const result = await response.json();

    if (!response.ok) throw new Error(result.detail || "Failed to fetch tasks");

    // Display tasks in a formatted way (you can enhance this as needed)
    if (result.length === 0) {
      alert("No tasks found for the provided user ID.");
    } else {
      const tasks = result
        .map(
          (task) =>
            `Task ID: ${task.task_id}, Name: ${task.task_name}, Description: ${task.task_description || "N/A"}`
        )
        .join("\n");

      alert(`Your Tasks:\n\n${tasks}`);
    }
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
});

  // Add Category Handler
addCategoryForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(addCategoryForm);
  const categoryData = Object.fromEntries(formData); // Convert form data to an object

  try {
    const response = await fetch(`${API_BASE}/categories/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token()}`,
      },
      body: JSON.stringify(categoryData), // Includes categoryName and category_description
    });

    const result = await response.json();

    if (!response.ok) throw new Error(result.detail || "Failed to add category");

    alert("Category added successfully!");
    addCategoryForm.reset(); // Clear the form
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
});

  // Logout button listener
  logoutButton.addEventListener("click", logout);

  // Check authentication status after DOM loads
  checkAuthentication();
});