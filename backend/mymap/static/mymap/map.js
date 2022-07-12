//{ % load static % }
let map = L.map('map').locate({
    setView: true,
    maxZoom: 19,
    enableHighAccuracy: true,
}).on("locationfound", (e) => map.setView(e.latlng, 16)).on("locationerror", () => map.setView([50.586276, 5.560470], 14));

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    zoom: 16,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let popup = L.popup();

console.log();

var greenIcon = L.icon({
    iconUrl: 'mymap/images/marker.png',
    //shadowUrl: "{% static 'mymap/images/marker.png' %}",

    iconSize: [24, 28.5], // size of the icon
    //shadowSize: [0, 0], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    //shadowAnchor: [0, 0], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

L.marker([48.5, 0.5], {
    icon: greenIcon
}).addTo(map);

/*function loadPopupsZoom(e) {
    //load popups relative to the zoom
}
map.on('viewreset', loadPopupsZoom)*/


/*function loadPopupsMove(e) {
    //load popups relative to the move
}
map.on('moveend', loadPopupsMove)*/

/*let popup = L.popup()
    .setLatLng([parseFloat('{{ lat }}'), parseFloat('{{ lon }}')])
    .setContent("I am a standalone popup.")
    .openOn(map);*/

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);