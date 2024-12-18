document.addEventListener("DOMContentLoaded", () => {
    const transactionForm = document.getElementById("transactionForm");
    const topUpForm = document.getElementById("topUpForm");

    transactionForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = {
            sender_id: document.querySelector('input[name="sender_id"]').value,
            receiver_username: document.querySelector('input[name="receiver_username"]').value,
            amount: parseFloat(document.querySelector('input[name="amount"]').value),
            description: document.querySelector('input[name="description"]').value || null,
        };

        try {
            const response = await fetch("/api/transactions", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", // Обязательно JSON
                },
                body: JSON.stringify(formData), // Преобразование в JSON
            });

            if (response.ok) {
                alert("Transaction successful!");
                window.location.reload();
            } else {
                const result = await response.json();
                console.error("Error:", result);
                alert("Error: " + (result.detail || "Unknown error"));
            }
        } catch (error) {
            console.error("Unexpected Error:", error);
            alert("An unexpected error occurred.");
        }
    });

    topUpForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const amount = parseFloat(document.querySelector('input[name="amount"]').value);

        if (amount <= 0) {
            alert("Amount must be greater than zero.");
            return;
        }

        try {
            const response = await fetch("/api/top-up", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ amount }),
            });

            if (response.ok) {
                const result = await response.json();
                alert("Balance topped up successfully!");
                document.getElementById("balance").innerText = result.new_balance;
                topUpForm.reset();
            } else {
                const error = await response.json();
                alert("Error: " + (error.detail || "Unknown error"));
            }
        } catch (error) {
            console.error("Unexpected Error:", error);
            alert("An unexpected error occurred.");
        }
    });
});




