function analyze() {
  const tasks = JSON.parse(document.getElementById("tasks").value);
  const strategy = document.getElementById("strategy").value;

  fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tasks, strategy })
  })
    .then(res => res.json())
    .then(data => {
      const ul = document.getElementById("result");
      ul.innerHTML = "";
      data.forEach(task => {
        let cls = "low";
        if (task.score > 7) cls = "high";
        else if (task.score > 4) cls = "medium";

        const li = document.createElement("li");
        li.className = cls;
        li.innerText = `${task.title} → Score: ${task.score}`;
        ul.appendChild(li);
      });
    })
    .catch(err => {
  console.error(err);
  alert("Error analyzing tasks. Check console.");
});
}