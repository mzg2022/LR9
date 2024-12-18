document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams(data),
        });

        if (response.ok) {
            alert("Login successful!");
            window.location.href = "/";
        } else {
            const error = await response.json();
            alert("Error: " + error.detail);
        }
    } catch (err) {
        console.error(err);
        alert("Login failed!");
    }
});