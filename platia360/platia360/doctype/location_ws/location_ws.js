// Copyright (c) 2025, Platia360 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Location WS", {
    // 1. Existing function for Reverse Geocoding (Marker -> Address)
    location: function(frm) {
        let mapdata = JSON.parse(cur_frm.doc.location).features[0];
        if (mapdata && mapdata.geometry.type == 'Point') {
            let lat = mapdata.geometry.coordinates[1];
            let lon = mapdata.geometry.coordinates[0];
            frappe.call({
                type: "GET",
                url: `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=11`,
                callback: function(r) {
                    console.log(r);
                    frm.set_value('latitude', r.lat);
                    frm.set_value('longitude', r.lon);
                    frm.set_value('address', r.display_name);
                    frm.set_value('city', r.address.city);
                    frm.set_value('county', r.address.county);
                    frm.set_value('state', r.address.state);
                    frm.set_value('country', r.address.country);
                }
            })
        }
    },

    // 2. New function for Forward Geocoding (Address -> Marker)
    // This function runs when the 'search_button' is clicked.
    search_button: function(frm) {
        const search_term = frm.doc.search_location_name;

        if (!search_term) {
            frappe.msgprint(__('Please enter a location name to search.'));
            return;
        }

        frappe.call({
            type: "GET",
            // Use Nominatim Search API
            url: `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(search_term)}&format=jsonv2&limit=1`,
            callback: function(response) {
                console.log(response[0]);
                // response.message contains the JSON array from the API
                if (response[0]) {
                    const search_result = response[0];
                    const lat = search_result.lat;
                    const lon = search_result.lon;

                    // Construct the GeoJSON object for the Map field
                    const geojson = {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "properties": {
                                    "name": search_result.display_name
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        parseFloat(lon), // Longitude (X) is first
                                        parseFloat(lat)  // Latitude (Y) is second
                                    ]
                                }
                            }
                        ]
                    };

                    // Set the GeoJSON string in the 'location' Map field
                    frm.set_value('location', JSON.stringify(geojson))
                        .then(() => {
                            frm.set_value('search_location_name', '');
                            frm.trigger('location'); 
                        });

                } else {
                    frappe.msgprint(__('Location not found for: ') + search_term);
                }
            },
            error: function() {
                frappe.msgprint(__('An error occurred during the search.'));
            }
        });
    },
});
