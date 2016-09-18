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
  //
  // var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
  // $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});
  //
  //
  // $.ajax({
  //    url: '../api/v1/parkingviolations/?rp_plate_state=DC&ticket_single_date=2013-12-24',
  //    data: {
  //       format: 'json'
  //    },
  //    error: function() {
  //       console.log('error');
  //    },
  //    dataType: 'json',
  //    success: function(data) {
  //       var mapPoints = data.results;
  //       var myLayer = L.geoJson(mapPoints,{
  //           onEachFeature: onEachFeature
  //     } ).addTo(map);
  //       // var usgs = L.tileLayer.wms("https://basemap.nationalmap.gov/ArcGIS/services/USGSImageryTopo/MapServer/WMSServer", {
  //       // layers:0,
  //       // format:'image/png',
  //       // transparent: true,
  //       // attribution: 'USGS',
  //       // }).addTo(map);
  //
  //
  //       var nexrad = L.tileLayer.wms("http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi", {
  //       layers: 'nexrad-n0r-900913',
  //       format:'image/png',
  //       transparent: true,
  //       attribution: 'Weather data © 2016 IEM Nexrad',
  //       }).addTo(map);
  //       //
  //       // var mymarker = L.marker([38.9046, -77.0238],
  //       //   {title: 'Center of map', alt:'The Big I', draggable:true}
  //       // );
  //       // var mymarker2 = L.marker([38.8046, -77.0238],
  //       //   {title: 'Another marker', alt:'The Big I', draggable:false}
  //       // );
  //       //
  //       //
  //       // var polygon = L.multiPolygon([
  //       //     [[38.9036, -77.0218], [38.9046, -77.1238], [38.9046, -77.0238]],
  //       //     [[38.9346, -77.1238],[38.9346, -77.0238],]
  //       //   ],
  //       //   {color:"blue", weight: 2})
  //       //
  //       // var mypopup = L.popup({keepInView: true, closeButtom: false}).setContent("<h1>we have same popup... </h1><p> because we are one group</p>");
  //       // var myLayerGroup = L.featureGroup([mymarker, polygon]).addTo(map).setStyle({color:"purple", opacity:5});
  //       //
  //       // mymarker2.bindPopup(mypopup);
  //       //
  //       // console.log('loaded');
  //       //
  //       // // Usage!
  //       // sleep(1500).then(() => {
  //       //     // Do something after the sleep!
  //       //   myLayerGroup.removeLayer(mymarker2);
  //       //
  //       //   console.log('removed mymarker2');
  //       // })
  //
  //     },
  //    type: 'GET',
  // });
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
    map.locate({setView: true, maxZoom: 13});

    // map.on('click', function(){alert('You clicked on the map')})

    // function clickLocation(e){
    //   var coord = e.latlng.toString().split(' ');
    //   var lat = coord[0].split('(');
    //   var lng = coord[1].split(')');
    //   alert("You clicked on the mat at LAT: " + lat[1] + "- LONG: " + lng[0])
    // }
    // map.on('click', clickLocation);

    map.on('click', function(e){L.marker(e.latlng, {draggable:true}).addTo(map)})


}
