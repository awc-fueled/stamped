//initialize main map
// initial map function is from a Google developers example. 
// I've customized it to fit my needs here here.
//https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
function initialize() {
  var mapOptions = {
    //set lat long for nyc 
    center: new google.maps.LatLng(40.7200, -73.9900),
    zoom: 13,
    mapTypeId: google.maps.MapTypeId.ROADMAP
    
  };
  var map = new google.maps.Map(document.getElementById('map-canvas'),
    mapOptions);

  var defaultBounds = new google.maps.LatLngBounds(
  new google.maps.LatLng(40.7200, -74.0000),
  new google.maps.LatLng(40.7200, -73.9000));

  var options = {
  bounds: defaultBounds,
  types: ['establishment'],
  //rescrict results to US
  componentRestrictions: {country: 'US'}
  };


  var input = (document.getElementById('searchTextField'));
  var autocomplete = new google.maps.places.Autocomplete(input, options);

  autocomplete.bindTo('bounds', map);

  var infowindow = new google.maps.InfoWindow();
  var marker = new google.maps.Marker({
    map: map
  });

  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    //remove any pervious info on the map (if there is any) to get ready for a new query
    infowindow.close();
    marker.setVisible(false);
    input.className = '';
    var place = autocomplete.getPlace();

    if (!place.geometry) {
      // Inform the user that the place was not found and return.
      input.className = 'notfound';
      return;
    }

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);  // Why 17? Because it looks good.
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
    infowindow.open(map, marker);

    //var output_list = [place.name, address];
   

    //handle CSRF 

    //send map change to home_jQuery.js
/*    var csrftoken = $.cookie('csrftoken'); 
    var send_data = { 'name': place.name, 'address': address};
    $.post( '/results/', send_data, function (response){
        alert(response); 
        return send_data;

    } );*/

    var send_data = { 'name': place.name, 'address': address};
    
    var csrftoken = $.cookie('csrftoken'); 
    
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    } 
    
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                xhr.setRequestHeader("X-Requested-With","XMLHttpRequest");
            }
        }
    });


    $.ajax({ url: '/results/',
        type: 'POST',
        data: send_data,
        success: function(response, status, jqXHR) {
          $("#results").html(response);
          //console.log('success function resp');
          //console.log(jqXHR.getAllResponseHeaders());
        },
        error: function(obj, status, err) { alert(err); console.log(err); }
      });



  });
  
}


  
google.maps.event.addDomListener(window, 'load', initialize);