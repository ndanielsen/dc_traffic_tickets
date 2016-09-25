/* Project specific Javascript goes here. */

var mapPoints;

var map = L.map('map').setView([38.911206,-77.028961], 13);

mapLink =
    '<a href="http://openstreetmap.org">OpenStreetMap</a>';
L.tileLayer(
    'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; ' + mapLink + ' Contributors',
    maxZoom: 18,
}).addTo(map);


function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.violation_code) {
        layer.bindPopup(feature.properties.violation_code);
    }
}


var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
$.ajaxSetup({headers: {"X-CSRFToken": csrfToken, "Authorization": 'Token: 3574c6f4785f8a0f52420f2e256946f5eb912883'} });

$.ajax({
   url: '../api/v1/parkingviolations/?rp_plate_state=DC&ticket_single_date=2015-05-30',
   data: {
      format: 'json'
   },
   error: function() {
      console.log('error');
   },
   dataType: 'json',
   success: function(data) {
      var mapPoints = data.results;
      var myLayer = L.geoJson(mapPoints,{
          onEachFeature: onEachFeature
    } ).addTo(map);
   },
   type: 'GET'
});
