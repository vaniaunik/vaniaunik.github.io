function countValue(){
    const numberInput = document.getElementById("numberInput").value;
    let message ="";
    let numberInputToInt = parseInt(numberInput);

    if (numberInputToInt >= 10){
        message = "Nilai lebih dari atau sama dengan 10";
    }
    else {
        message = "Nilai kurang dari 10"
    }
    if (numberInputToInt <0){
        message = "Nilai negatif"
    }
    document.getElementById("result").innerHTML = message;
}