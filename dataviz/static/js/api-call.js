/* Project specific Javascript goes here. */

function ajaxCall(url, map){
  console.log(url);
  var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});

  $.ajax({
     url: url,
     data: {
        format: 'json'
     },
     error: function() {
        console.log('error');
     },
     dataType: 'json',
     success: function(data) {
       addPointsMap(data, map);

     },
     type: 'GET'
  });
}

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.violation_code) {
        layer.bindPopup(feature.properties.violation_code);
    }
}

function addPointsMap(data, map){
  var mapPoints = data.results;
  var myLayer = L.geoJson(mapPoints,{
      onEachFeature: onEachFeature} ).addTo(map);
}

function traffic_api_call(url, map){
  ajaxCall(url, map);
}


function map_init_basic(map, options) {
  console.log('js loaded');
  var url = '../api/v1/parkingviolations/?rp_plate_state=&violation_code=&holiday=1&body_style=&ticket_date_range_start=2013-12-01&ticket_date_range_end=2015-12-22&ticket_single_date=&ticket_day_of_week='
  traffic_api_call(url, map);
}
