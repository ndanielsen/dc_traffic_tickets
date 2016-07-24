var map = L.map('map').setView([38.911206,-77.028961], 12);
mapLink =
    '<a href="http://openstreetmap.org">OpenStreetMap</a>';
L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; ' + mapLink + ' Contributors',
    maxZoom: 18,
}).addTo(map);

var heat = L.heatLayer(mapPoints,{
    radius: 10,
    blur: 10,
    maxZoom: 17,
}).addTo(map);
