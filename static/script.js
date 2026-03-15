let score = 0

let scoreDispaly = document.getElementById("score1234");
let cuillereBtn = document.getElementById("faireUneCuillèreBtn");

function updateScore() {
    scoreDispaly.textContent = score.toString();
}

function addToScore(number) {
    score = score + number
    updateScore()
}

updateScore()

cuillereBtn.addEventListener("click", () => addToScore(1))