var statecodes = {AL: 'Alabama', AK: 'Alaska', AZ: 'Arizona', AR: 'Arkansas', CA: 'California', CO: 'Colorado', CT: 'Connecticut', DE: 'Delaware', DC: 'District of Columbia', FL: 'Florida', GA: 'Georgia', HI: 'Hawaii', ID: 'Idaho', IL: 'Illinois', IN: 'Indiana', IA: 'Iowa', KS: 'Kansas', KY: 'Kentucky', LA: 'Louisiana', ME: 'Maine', MD: 'Maryland', MA: 'Massachusetts', MI: 'Michigan', MN: 'Minnesota', MO: 'Missouri', MT: 'Montana', NE: 'Nebraska', NV: 'Nevada', NH: 'New Hampshire', NJ: 'New Jersey', NM: 'New Mexico', NY: 'New York', NC: 'North Carolina', ND: 'North Dakota', OH: 'Ohio', OK: 'Oklahoma', OR: 'Oregon', PA: 'Pennsylvania', RI: 'Rhode Island', SC: 'South Carolina', SD: 'South Dakota', TN: 'Tennessee', TX: 'Texas', UT: 'Utah', VT: 'Vermont', VA: 'Virginia', WA: 'Washington', WV: 'West Virginia', WI: 'Wisconsin', WY: 'Wyoming'}


jQuery(window).ready(function(){  
  navigator.geolocation.getCurrentPosition(handle_geolocation_query);  

});     

function handle_geolocation_query(position){  
  var lat = parseFloat(position.coords.latitude);
  var lng = parseFloat(position.coords.longitude);
  var latlng = new google.maps.LatLng(lat, lng);
  var geocoder = new google.maps.Geocoder();
  var stateCode;
  geocoder.geocode({'latLng': latlng}, function(results, status) {
    for (var i = 0; i < results.length; i++) {
      for (var j = 0; j < results[i].types.length; j++) {
        if (results[i].types[j] == "administrative_area_level_1") {
          address = results[i].formatted_address.split(",")[0]
          for (state in statecodes) {
            if (statecodes[state] == address) {
              stateCode = state;
            }
          }
        }
      }
    }
    
    $.ajax({
      url: '/votes?chamber=senate&state='+stateCode,
      success: function(data) {
      
        if (status == google.maps.GeocoderStatus.OK) {
         console.log(results);
      }


        $('body').html(data);
                  }
  });
  });
}

