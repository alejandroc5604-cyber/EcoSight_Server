


const map = L.map('map').setView([-1.2864, 36.8172], 12);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        attribution: '&copy; OpenStreetMap contributors'
    }
).addTo(map);

L.marker([-1.2864, 36.8172])
    .addTo(map)
    .bindPopup('Example detection')
    .openPopup();