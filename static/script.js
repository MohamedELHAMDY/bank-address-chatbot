const map = L.map('map').setView([33.9713, -6.8498], 7);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

fetch('data/bank_locations_geocoded.csv')  // Correct path
    .then(response => response.text())
    .then(csvData => {
        const data = L.CSV.parse(csvData); // You'll need to include a CSV parsing library
        data.forEach(row => {
            const lat = parseFloat(row.latitude);
            const lng = parseFloat(row.longitude);
            if (!isNaN(lat) && !isNaN(lng)) {
                L.marker([lat, lng]).addTo(map)
                    .bindPopup(`${row.NOM_BANQUE}<br>${row.NOM_AGENCE}<br>${row.ADRESSE}`);
            }
        });
    }); 
