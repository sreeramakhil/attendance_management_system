// auth.js — include this in every protected page
const API = `http://${window.location.hostname}:5000`;

// Global Fetch Interceptor to automatically add X-Teacher-Username header
const originalFetch = window.fetch;
window.fetch = async function (url, options = {}) {
  const teacher = localStorage.getItem("teacher_username");
  if (teacher && url.toString().startsWith(API)) {
    if (!options.headers) options.headers = {};
    if (options.headers instanceof Headers) {
      options.headers.set("X-Teacher-Username", teacher);
    } else {
      options.headers["X-Teacher-Username"] = teacher;
    }
  }
  options.credentials = "include"; // Keep session support active
  return originalFetch(url, options);
};

// Check login on every page load using localStorage fallback
async function checkAuth() {
  const teacher = localStorage.getItem("teacher_username");
  
  if (!teacher) {
    // If not logged in and not on login page, redirect to login
    if (!window.location.href.includes("login.html")) {
      window.location.href = "login.html";
    }
    return null;
  }
  
  // Show teacher name in nav
  const el = document.getElementById("teacher-name");
  if (el) el.textContent = "Logged in as: " + teacher;
  return teacher;
}

// Logout function
async function logout() {
  localStorage.removeItem("teacher_username");
  try {
    await fetch(`${API}/logout`, { method: "POST" });
  } catch(e) {}
  window.location.href = "login.html";
}

// Run on every page load
checkAuth();