function initMap() {
    const uluru = { lat: 18.9258, lng: 72.8313 };
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 18,
      center: uluru,
    });
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
    });
  }
  window.initMap = initMap;
  