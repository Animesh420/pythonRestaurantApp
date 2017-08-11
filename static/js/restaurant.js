function handleOnEdit(e, rest_id, menu_id) {
    var id = e.getAttribute('id');

    listItem = document.getElementById(`list${menu_id}`);
    name = document.getElementById(`name${menu_id}`).innerHTML;
    price = document.getElementById(`price${menu_id}`).innerHTML;
    course = document.getElementById(`course${menu_id}`).innerHTML;
    description = document.getElementById(`description${menu_id}`).innerHTML;

    $(`#editmyModal${menu_id}`).modal('show');
}

function handleOnDelete(e, rest_id, menu_id) {
    $(`#delmyModal${menu_id}`).modal('show');
}
function showReviewModal() {
    // $(`#reviews${rest_id}`).modal('show');
    var element = document.getElementById(`reviews${rest_id}`);
    element.modal('show')
};

function initMap(loc) {
    if (loc !== undefined) {


        var uluru = { lat: loc.lat, lng: loc.lng };
        var LatLngList = [
            new google.maps.LatLng(loc.lat, loc.lng)
        ],
            latlngbounds = new google.maps.LatLngBounds();

        LatLngList.forEach(function (latLng) {
            latlngbounds.extend(latLng);
        });

        var map = new google.maps.Map(document.getElementById(loc.id), {
            center: uluru,
            zoom:5

        });

        map.addListener('click', function () {

            console.log('i am being clicked');
            $(`#${loc.id}`).modal("hide");
        });

        var marker = new google.maps.Marker({
            position: uluru,
            map: map
        });

        // map.panTo(marker.getPosition());
        // map.setZoom(4);
        // map.fitBounds(latlngbounds);
    }
}
function getReviews(e, rest_id) {
    var id = e.getAttribute('id');
    if (id != 'map') {
        url_review = `http://localhost:8080/reviews/${rest_id}`;
    }
    else {
        url_review = `http://localhost:8080/map/${rest_id}`;
    }
    var ty = $(`#reviews${rest_id}`)
    $this = this;
    that = this;
    var reviews = null;
    $.ajax(
        {
            url: url_review,
            idType: id,
            mapLoader: that.initMap,
            type: 'GET',
            success: function (result) {

                let thislat = result.data.lat;
                let thislng = result.data.lng;
                if (this.idType != 'map') {
                    reviews = result.data.review;
                    var list = document.getElementById('rev');
                    while (list.hasChildNodes()) {
                        list.removeChild(list.firstChild);
                    }
                    for (var key in reviews) {
                        if (reviews.hasOwnProperty(key)) {
                            var val = reviews[key];
                            var node = document.createElement('li');
                            node.innerHTML = val;
                            list.appendChild(node)
                        }
                    }
                }
                else {
                    var loc = { lat: thislat, lng: thislng, id: `reviews${rest_id}` };
                    $(`#reviews${rest_id}`).css({
                        "width": "100 %",
                        "height": "400px",
                        "background-color": "grey"
                    });
                    this.mapLoader(loc);
                }
                $(`#reviews${rest_id}`).modal('show');

            }
            ,
            error: function (err) { console.log(err); }
        }
    );



}