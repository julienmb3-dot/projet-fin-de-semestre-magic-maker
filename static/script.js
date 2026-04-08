let score = 0
let time_played = 0
let level = 0

const defaultData = {"score" : 0, "time_played" : 0, "level" : 0}

let scoreDispaly = document.getElementById("score1234");
let cuillereBtn = document.getElementById("faireUneCuillèreBtn");

function verifyJSON(json) {
  try {
    const data = JSON.parse(json);   // ← lève une exception si le texte n’est pas du JSON valide
    return true;
  } catch (e) {
    return false;
  }
}

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
        if (verifyJSON(Response)) {
            return JSON.parse(Response);
        } else {
            return defaultData
        }
    }, rejected => {
        console.log(rejected.toString());
        return defaultData
    })
    console.log("time played = " + data.time_played);
    console.log("level = " + data.level);
    score = Number(data.score);
    time_played = Number(data.time_played);
    level = Number(data.level);
    scoreDispaly.textContent = score;
    
}

reloadScore();

function addToScore(number) {
    score = score + number;
    updateScore();
}


cuillereBtn.addEventListener("click", () => addToScore(1));