function addition() {
let firstNumber = document.getElementById("firstNumber").value;
let secondNumber = document.getElementById("secondNumber").value;

hasil = parseInt(firstNumber) + parseInt(secondNumber);
document.getElementById("result").innerHTML = hasil;
}

function substraction() {
    let firstNumber = document.getElementById("firstNumber").value;
    let secondNumber = document.getElementById("secondNumber").value;
    
    hasil = parseInt(firstNumber) - parseInt(secondNumber);
    
    document.getElementById("result").innerHTML = hasil;
    }

    function multiplication() {
        let firstNumber = document.getElementById("firstNumber").value;
        let secondNumber = document.getElementById("secondNumber").value;
        
        hasil = parseInt(firstNumber) * parseInt(secondNumber);
        
        document.getElementById("result").innerHTML = hasil;
        }
    
    function division() {
            let firstNumber = document.getElementById("firstNumber").value;
            let secondNumber = document.getElementById("secondNumber").value;
            
            hasil = parseInt(firstNumber) / parseInt(secondNumber);
            
            document.getElementById("result").innerHTML = hasil;
            }

    function remove() {
        let firstNumber = document.getElementById("firstNumber").value;
        let secondNumber = document.getElementById("secondNumber").value;

        document.getElementById("firstNumber").value = "";
        document.getElementById("secondNumber").value = "";
        document.getElementById("result").innerHTML = "";
    }