const API_BASE = "http://127.0.0.1:5000/api";

// Test backend
async function checkBackend() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();

        console.log("StudyHive Backend:", data);
    } catch (error) {
        console.error("Backend connection failed:", error);
    }
}


// Register user
const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Account created successfully!");
                registerForm.reset();
                window.location.href = "login.html";
            } else {
                alert(data.message);
            }

        } catch (error) {
            alert("Unable to connect to the server.");
            console.error(error);
        }
    });
}


checkBackend();