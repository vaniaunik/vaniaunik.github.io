document.getElementById("Heading").innerHTML = "Selamat Datang di DOM HTML";


function changeText() {
    document.getElementById("Heading2").innerHTML = "Angeline Vania Tjandra";
}

function removeText() {
    document.getElementById("Heading2").innerHTML = "";
}

function changeName(){
    let name = document.getElementById("name").value;
    document.getElementById("result").innerHTML = name;
}

function removeText(){
    document.getElementById("name").value = "";
    document.getElementById("result").innerHTML = "";
}