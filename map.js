//initialize map
var map = L.map("map").setView([32.8, -116.9], 10);

//remove deafault 'Leaflet' attribution
map.attributionControl.setPrefix()

//set tile layer
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

//initialize marker cluster group
var markers = L.markerClusterGroup();

//get geojson records of photo metadata
$.getJSON("photo_data.geojson", function(json_data){
    //console.log(json_data)
    //create new layer from geojson data records
    var json_layer = L.geoJson(json_data, {
        //for each record in the data...
        onEachFeature: function (feature, layer) {
            //...create and bind a popup
            var popup_prop = L.popup({ minWidth:400 })
                    .setContent('Name: ' + feature.properties.Name + '<br>' + 
                                'Date: ' + feature.properties.Date + '<br>' + 
                                'Time: ' + feature.properties.Time + '<br>' + 
                                'Lat: ' + feature.properties.Lat + '<br>' + 
                                'Lon: ' + feature.properties.Lon + '<br>' + 
                                'Path: ' + feature.properties.RelP + '<br>' + 
                                'Photo:' + '<br>' +
                                '<a href=' + "http://192.168.1.94:8000/" + feature.properties.RelP + ' target=' + "_blank" + ' rel=' + "noopener noreferrer" + '>' + '<img src=' + "http://192.168.1.94:8000/" + feature.properties.RelP + ' style=' + "width:400px;" + '>' + '</a>'
                    )
            layer.bindPopup(popup_prop)
        }
    });
    //add the json layer to the cluster markers object
    markers.addLayer(json_layer);
});
//add the cluster marker object to the map
map.addLayer(markers);