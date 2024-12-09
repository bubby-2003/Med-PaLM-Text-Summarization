document.getElementById("summarize").addEventListener("click", () => {
    const text = document.getElementById("text").value;
    const length = document.getElementById("length").value;
    const specialty = document.getElementById("specialty").value;
    const style = document.getElementById("style").value;

    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: text,
            length: length,
            specialty: specialty,
            style: style
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.summary) {
            document.getElementById("summary").innerText = data.summary;
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        alert("An error occurred: " + error);
    });
});
