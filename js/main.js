function initMap() {
        new google.maps.Map(document.getElementById('map'), {
            center: {lat: {{lat}}, lng: {{lng}}},
            zoom: 16
          });
    }
