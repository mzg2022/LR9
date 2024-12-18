document.getElementById("registerForm").addEventListener("submit", async (event) => {
    event.preventDefault(); // Останавливаем стандартное поведение формы
    const formData = new FormData(event.target); // Получаем данные из формы
    const data = Object.fromEntries(formData.entries()); // Преобразуем данные в объект

    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch("/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json", // Указываем, что данные будут в формате JSON
            },
            body: JSON.stringify(data), // Преобразуем объект в JSON для отправки
        });

        if (response.ok) {
            alert("Registration successful!"); // Показываем сообщение об успешной регистрации
            window.location.href = "/login"; // Перенаправляем пользователя на страницу логина
        } else {
            // Обрабатываем ошибку
            const error = await response.json();
            alert("Error: " + (error.detail || "Unknown error occurred")); // Показываем сообщение об ошибке
        }
    } catch (err) {
        // Обрабатываем сетевые ошибки
        console.error("Network error:", err);
        alert("Registration failed due to a network error!");
    }
});





