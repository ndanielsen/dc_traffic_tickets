/* Project specific Javascript goes here. */

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.issues) {
        layer.bindPopup("<h2>" + feature.properties.name + "</h2>" + "<p>" + feature.properties.issues + "</p>");
    }
}

function styleFunction(feature){
  switch (feature.geometry.type) {
    case 'LineString':
      return {color: "red"};
      break;
    case 'Polygon':
      return {color: 'green', weight:1, fillOpacity:.1};
      break;

    case 'Feature':
      return {color: 'purple'};
      break;
  }
}



function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function static_ajax_request(url, map){



  var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});

  $.ajax({
     type: 'GET',
     url: url,
     data: {
        format: 'json'
     },
     error: function() {
        console.log('error');
     },
     dataType: 'json',
     success: function(data) {
       console.log(data);
       var geoJsonLayer = L.geoJson(data, {onEachFeature: onEachFeature, style: styleFunction}).addTo(map);
       function newStyle(){
         geoJsonLayer.setStyle({color: 'green'})
       }
        geoJsonLayer.on('mouseover', newStyle);
        geoJsonLayer.on('mouseout', function(e){geoJsonLayer.resetStyle(e.target)})
     }
   });
}





function map_init_basic(map, options) {
  console.log('js loaded');
  static_ajax_request('../static/data/dpw-parking-beats.geojson', map)


}
