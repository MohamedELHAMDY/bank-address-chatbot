async function searchBank() {
    let bankName = document.getElementById("bankName").value;
    let locality = document.getElementById("locality").value;

    let response = await fetch('data/addresses.json');
    let data = await response.json();

    let result = data.find(bank => 
        bank.BANQUE.toLowerCase() === bankName.toLowerCase() && 
        bank.LOCALITE.toLowerCase() === locality.toLowerCase()
    );

    document.getElementById("result").innerText = result ? 
        `🏦 ${result.BANQUE} - ${result.NOM GUICHET} 📍 ${result.ADRESSE GUICHET}` : 
        "❌ No matching bank found.";
}
