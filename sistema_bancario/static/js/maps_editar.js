function initMap(){
    var directionsDisplay;
    inicializar(14.586388500,-90.552813200);

    function inicializar(latitud,longitud)
    {
        //alert("algo");
        var latlng1 = new google.maps.LatLng(document.getElementById('id_lat_origen').value,
                                             document.getElementById('id_long_origen').value);
        var mapa = new google.maps.Map(document.getElementById('mapa_origen'), {
          center: latlng1,
          zoom: 16,
          mapTypeid: google.maps.MapTypeId.ROADMAP
        });
        var marker1 = new google.maps.Marker({
          position: latlng1,
          draggable: true,
          title: 'Origen',
          map: mapa
        });

        var latlng2 = new google.maps.LatLng(document.getElementById('id_lat_dest').value,
                                             document.getElementById('id_long_dest').value);

        var marker2 = new google.maps.Marker({
          position: latlng2,
          draggable: true,
          title: 'Destino',
          map: mapa
        });

        google.maps.event.addListener(marker1, 'position_changed', function(){
            getmarkerCoordenadas(marker1,marker2)
        });

        google.maps.event.addListener(marker2, 'position_changed', function(){
            getmarkerCoordenadas(marker1,marker2)
        });

        directionsDisplay = new google.maps.DirectionsRenderer();
        directionsDisplay.setMap(mapa);

        var lat_origen=document.getElementById('id_lat_origen').value;
        var long_origen=document.getElementById('id_long_origen').value;
        var lat_dest=document.getElementById('id_lat_dest').value;
        var long_dest=document.getElementById('id_long_dest').value;

        var directionsService = new google.maps.DirectionsService();
        var request = {
            origin: new google.maps.LatLng(lat_origen,  long_origen),
            destination: new google.maps.LatLng(lat_dest,  long_origen),
            travelMode: 'DRIVING'
        };
        directionsService.route(request, function(result, status) {
        if (status == 'OK') {
          directionsDisplay.setDirections(result);
          directionsDisplay.setOptions( { suppressMarkers: true , preserveViewport: true} );
        }
        });

         //AUTOCOMPLETE
        var input = /** @type {!HTMLInputElement} */(
            document.getElementById('auto_complete'));

        mapa.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.bindTo('bounds', mapa);

        autocomplete.setComponentRestrictions(
            {'country': ['gt']});

        var infowindow = new google.maps.InfoWindow();
        var marker = new google.maps.Marker({
          map: mapa,
          anchorPoint: new google.maps.Point(0, -29)
        });

        autocomplete.addListener('place_changed', function() {
          infowindow.close();
          marker.setVisible(false);
          var place = autocomplete.getPlace();
          if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
          }

          // If the place has a geometry, then present it on a map.
          if (place.geometry.viewport) {
            mapa.fitBounds(place.geometry.viewport);
          } else {
            mapa.setCenter(place.geometry.location);
            mapa.setZoom(17);  // Why 17? Because it looks good.
          }
          marker.setIcon(/** @type {google.maps.Icon} */({
            url: place.icon,
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(35, 35)
          }));
          marker.setPosition(place.geometry.location);
          marker.setVisible(true);

          var address = '';
          if (place.address_components) {
            address = [
              (place.address_components[0] && place.address_components[0].short_name || ''),
              (place.address_components[1] && place.address_components[1].short_name || ''),
              (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
          }

          infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
          infowindow.open(mapa, marker);
        });
    }

    function getmarkerCoordenadas(marker1,marker2)
    {
        var markerCoordenadasOrigen = marker1.getPosition();
        var a = document.getElementById('id_lat_origen');
        a.value = markerCoordenadasOrigen.lat();
        var b = document.getElementById('id_long_origen');
        b.value = markerCoordenadasOrigen.lng();

        var markerCoordenadasDestino = marker2.getPosition()
        var c = document.getElementById('id_lat_dest');
        c.value = markerCoordenadasDestino.lat();
        var d = document.getElementById('id_long_dest');
        d.value = markerCoordenadasDestino.lng();

        console.log("("+a.value+","+b.value+")->("+c.value+","+d.value+")");

        var origin = {lat: markerCoordenadasOrigen.lat(), lng: markerCoordenadasOrigen.lng()};
        var destination = {lat:  markerCoordenadasDestino.lat(), lng:  markerCoordenadasDestino.lng()}

        var service = new google.maps.DistanceMatrixService();
        service.getDistanceMatrix(
          {
            origins: [origin],
            destinations: [destination],
            travelMode: 'DRIVING',
            unitSystem: google.maps.UnitSystem.METRIC,
            avoidHighways: false,
            avoidTolls: false,
          }, function(response,status){ callback(response,status) });

        var directionsService = new google.maps.DirectionsService();
        var request = {
            origin: new google.maps.LatLng(markerCoordenadasOrigen.lat(),  markerCoordenadasOrigen.lng()),
            destination: new google.maps.LatLng(markerCoordenadasDestino.lat(),  markerCoordenadasDestino.lng()),
            travelMode: 'DRIVING'
        };
        directionsService.route(request, function(result, status) {
        if (status == 'OK') {
          directionsDisplay.setDirections(result);
          directionsDisplay.setOptions( { suppressMarkers: true , preserveViewport: true} );
        }
        });
    }

    function set_line(lat_origen,long_origen,lat_dest,long_dest){
        alert("new line");
        var directionsService = new google.maps.DirectionsService();
        var request = {
            origin: new google.maps.LatLng(lat_origen,  long_origen),
            destination: new google.maps.LatLng(lat_dest,  long_origen),
            travelMode: 'DRIVING'
        };
        directionsService.route(request, function(result, status) {
        if (status == 'OK') {
          directionsDisplay.setDirections(result);
          directionsDisplay.setOptions( { suppressMarkers: true , preserveViewport: true} );
        }
        });
    }

    function callback(response, status){
        //Status correcto
        if (status == 'OK') {
            var distancia = response.rows[0].elements[0].distance.value;
            //console.log((distancia/1000));
            var e = document.getElementById('id_precio');
            e.value = ((distancia/1000)*7.5).toFixed(2);
        }else{
            console.log('Error was: ' + status);
        }
    }

}