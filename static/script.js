let score = 0
let time_played = 0
let level = 0

let scoreDispaly = document.getElementById("score1234");
let cuillereBtn = document.getElementById("faireUneCuillèreBtn");


function updateScore() {
    scoreDispaly.textContent = score.toString();
    fetch("/update_game", {
        method : "POST",
        headers: {"Content-Type" : "application/json"}, // indique que le corps est du JSON
        
        body: JSON.stringify({
        "score" : score,
        "time_played" : time_played,
        "level" : level,
        })
    })
}

function reloadScore() {
    
    let data = fetch("/update_game", {method : "GET"}).then(Response => {
        return JSON.parse(Response);
    }, rejected => {
        console.log(rejected.toString())
    })
    console.log("time played = " + data.time_played.toString())
    console.log("level = " + data.level.toString())
    score = data.score 
    time_played = data.time_played
    level = data.level
    scoreDispaly.textContent = score.toString();
    
}

scoreDispaly.textContent = score.toString();

function addToScore(number) {
    score = score + number
    updateScore()
}


cuillereBtn.addEventListener("click", () => addToScore(1))