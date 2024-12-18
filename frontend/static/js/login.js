document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",  // Передаем данные формы
            },
            body: new URLSearchParams(data).toString(),  // Преобразуем данные в строку с параметрами
        });

        if (response.ok) {
            const result = await response.json();
            alert("Login successful!");
            // Сохраняем токен и перенаправляем пользователя в личный кабинет
            document.cookie = `access_token=${result.access_token}; path=/; HttpOnly; Secure`;
            window.location.href = "/dashboard";  // Перенаправляем на личный кабинет
        } else {
            const error = await response.json();
            alert("Error: " + error.detail);
        }
    } catch (err) {
        console.error(err);
        alert("Login failed!");
    }
});




