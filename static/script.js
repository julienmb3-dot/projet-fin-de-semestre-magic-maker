let score = 0
let time_played = 0
let state = 0

let scoreDispaly = document.getElementById("score1234");
let cuillereBtn = document.getElementById("faireUneCuillèreBtn");

function updateScore() {
    scoreDispaly.textContent = score.toString();
    fetch("/update_game", {
        method: "POST",
        
        "Content-Type": "application/json"   // indique que le corps est du JSON
        
        .then

        JSON.stringify({
            "score" : score,
            "time_played" : time_played,
            "state" : state
        }) // les données à envoyer
    })

}

function addToScore(number) {
    score = score + number
    updateScore()
}

updateScore()


cuillereBtn.addEventListener("click", () => addToScore(1))