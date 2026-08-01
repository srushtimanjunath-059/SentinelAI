async function analyzeTransaction() {

    let amount =
    document.getElementById("amount").value;

    let response =
    await fetch(
        `http://127.0.0.1:8000/analyze/${amount}`
    );

    let data = await response.json();

    document.getElementById("risk").innerHTML =
    data.risk_score + "%";

    if(data.risk_score >= 60){

        document.getElementById("status").innerHTML =
        "🚨 High Risk Transaction";

    } else {

        document.getElementById("status").innerHTML =
        "✅ Safe Transaction";

    }
}