/* Project specific Javascript goes here. */

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.violation_code) {
        layer.bindPopup(feature.properties.violation_code);
    }
}

function map_init_basic(map, options) {
  console.log('js loaded');

  var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});


  $.ajax({
     url: '../api/v1/parkingviolations/?rp_plate_state=DC&ticket_single_date=2013-12-24',
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






}
