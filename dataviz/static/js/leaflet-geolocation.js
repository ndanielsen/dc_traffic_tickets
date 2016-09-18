/* Project specific Javascript goes here. */

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.violation_code) {
        layer.bindPopup(feature.properties.violation_code);
    }
}

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}



function map_init_basic(map, options) {
  console.log('js loaded');
		function onLocationFound(e) {
			var radius = e.accuracy / 2;

			L.marker(e.latlng).addTo(map)
				.bindPopup("You are within " + radius + " meters from this point").openPopup();

			L.circle(e.latlng, radius).addTo(map);
		}

		function onLocationError(e) {
			alert(e.message);
		}

		map.on('locationfound', onLocationFound);
		map.on('locationerror', onLocationError);

		map.locate({setView: true, maxZoom: 16});

}
