document.getElementById("predictionForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {};

    // Convert form inputs to JSON
    formData.forEach((value, key) => {
        data[key] = isNaN(value) ? value : parseFloat(value);
    });

    console.log("📤 Sending data to server:", data);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const result = await response.json();
        console.log("📥 Received result:", result);

        if (result.prediction !== undefined) {
            const message = result.prediction === 1 ? "🚨 Heart Disease Present" : "✅ No Heart Disease";
            document.getElementById("result").innerHTML = `<strong>Prediction:</strong> ${message} (${result.probability})`;
        } else if (result.error) {
            document.getElementById("result").innerHTML = `<strong>Error:</strong> ${result.error}`;
        }
    } catch (error) {
        console.error("❌ Fetch error:", error);
        document.getElementById("result").innerHTML = `<strong>Error:</strong> ${error.message}`;
    }
});
