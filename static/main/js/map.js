// This example adds hide() and show() methods to a custom overlay's prototype.
// These methods toggle the visibility of the container <div>.
// overlay to or from the map.


let map, infoWindow;





function initMap() {

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: { lat: 34.433907, lng: -119.809291 },
    mapTypeId: google.maps.MapTypeId.SATELLITE,
    streetViewControl: true

  });

  const ctaLayer = new google.maps.KmlLayer({
    url: '/static/main/images/q2.kmz',
    map: map,
  });

  infoWindow = new google.maps.InfoWindow();
  const bounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(34.3313407, -120.2913263),
    new google.maps.LatLng(34.5593061, -119.3617093)
  );

  // location button
  const locationButton = document.createElement("button");

  locationButton.textContent = "to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(locationButton);
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

          infoWindow.setPosition(pos);
          infoWindow.setContent("User Location");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });

  // kml Overlay
  var kmlsrc = '/static/main/images/q2.kmz';

    var kmzLayer = new google.maps.KmlLayer(kmlsrc, {
      suppressInfoWindows: true,
      preserveViewport: false,
      map: map
    });
     console.log(kmzLayer)
 kmzLayer.setMap(map);


  // Custom Overlay
  let image = "/static/main/images/ih.png" ;

  class USGSOverlay extends google.maps.OverlayView {
    bounds;
    image;
    div;
    constructor(bounds, image) {
      super();
      this.bounds = bounds;
      this.image = image;
    }
    /**
     * onAdd is called when the map's panes are ready and the overlay has been
     * added to the map.
     */
    onAdd() {
      this.div = document.createElement("div");
      this.div.style.borderStyle = "none";
      this.div.style.borderWidth = "0px";
      this.div.style.position = "absolute";

      // Create the img element and attach it to the div.
      const img = document.createElement("img");
      img.src = this.image;
      img.style.width = "100%";
      img.style.height = "100%";
      img.style.position = "absolute";
      this.div.appendChild(img);

      // Add the element to the "overlayLayer" pane.
      const panes = this.getPanes();

      panes.overlayLayer.appendChild(this.div);
    }
    draw() {
      // We use the south-west and north-east
      // coordinates of the overlay to peg it to the correct position and size.
      // To do this, we need to retrieve the projection from the overlay.
      const overlayProjection = this.getProjection();
      // Retrieve the south-west and north-east coordinates of this overlay
      // in LatLngs and convert them to pixel coordinates.
      // We'll use these coordinates to resize the div.
      const sw = overlayProjection.fromLatLngToDivPixel(
        this.bounds.getSouthWest()
      );
      const ne = overlayProjection.fromLatLngToDivPixel(
        this.bounds.getNorthEast()
      );

      // Resize the image's div to fit the indicated dimensions.
      if (this.div) {
        this.div.style.left = sw.x + "px";
        this.div.style.top = ne.y + "px";
        this.div.style.width = ne.x - sw.x + "px";
        this.div.style.height = sw.y - ne.y + "px";
      }
    }
    /**
     * The onRemove() method will be called automatically from the API if
     * we ever set the overlay's map property to 'null'.
     */
    onRemove() {
      if (this.div) {
        this.div.parentNode.removeChild(this.div);
        delete this.div;
      }
    }
    /**
     *  Set the visibility to 'hidden' or 'visible'.
     */
    hide() {
      if (this.div) {
        this.div.style.visibility = "hidden";
      }
    }
    show() {
      if (this.div) {
        this.div.style.visibility = "visible";
      }
    }
    toggle() {
      if (this.div) {
        if (this.div.style.visibility === "hidden") {
          this.show();
        } else {
          this.hide();
        }
      }
    }
    toggleDOM(map) {
      if (this.getMap()) {
        this.setMap(null);
      } else {
        this.setMap(map);
      }
    }
  }

  const overlay = new USGSOverlay(bounds, image);

  overlay.setMap(map);

  const toggleButton = document.createElement("button");

  toggleButton.textContent = "Toggle";
  toggleButton.classList.add("custom-map-control-button");

//  const toggleDOMButton = document.createElement("button");

//  toggleDOMButton.textContent = "Toggle DOM Attachment";
//  toggleDOMButton.classList.add("custom-map-control-button");
  toggleButton.addEventListener("click", () => {
    overlay.toggle();
  });
//  toggleDOMButton.addEventListener("click", () => {
//    overlay.toggleDOM(map);
//  });
//  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(toggleDOMButton);
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(toggleButton);
}



function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}


window.initMap = initMap;