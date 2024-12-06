//$(document).ready(function(e) {
//    e.preventDefault();
//    $('#formSubmit').on('submit', function() {
//     // e.preventDefault(); // Prevent the page from reloading
//        var formData = $(this).serialize();
//    });
//});

console.log('random_drink', random_drink)

$(document).ready(function(e) {
    e.preventDefault();
    $('#formSubmit').on('submit', function() {
        // e.preventDefault(); // Prevent the page from reloading

        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: '/',  // URL to the random drink API
            data: formData,
            success: function(response) {
                var resultsDiv = $('#results');
                var currentDrinkIdInput = $('#current_drink_id');

                console.log('resultsDiv', resultsDiv)
                console.log('currentDrinkIdInput', currentDrinkIdInput)

                // Clear previous results
                resultsDiv.empty();

                // Get the new drink data
                var drink = response.random_drink;

                // Update the hidden field with the new drink ID
                currentDrinkIdInput.val(drink.id);

                // Display the new random drink data
                resultsDiv.append(
                    '<code class="openBrackets">{</code>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"id": </code>' +
                    '<code class="api_drink_name">' + drink.id + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"drink_name": </code>' +
                    '<code class="api_drink_name">' + drink.drink_name + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"slug": </code>' +
                    '<code class="api_drink_name">' + '"' + drink.slug + '"' + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"profile": </code>' +
                    '<code class="api_drink_name">' + '"' + drink.profile + '"' + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"base_alcohol": </code>' +
                    '<code class="api_drink_name">' +  '"' + drink.base_alcohol + '"' +  '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"ingredient_name": </code>' +
                    '[' + drink.ingredient_name.map((din) => (
                        '<code class="api_drink_name">' +  '\n"' + din + '"'  + '</code>'
                    )) + '\n]'
                     +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"garnish": </code>' +
                    '<code class="api_drink_name">' + '"' + drink.garnish + '"' + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"serving_glass": </code>' +
                    '<code class="api_drink_name">' + '"' + drink.serving_glass + '"' + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"mixing_direction": </code>' +
                    '<code class="api_drink_name api_mix_name">' + '"' + drink.mixing_direction + '"' + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"drink_type": </code>' +
                    '<code class="api_drink_name">' + '"' + drink.drink_type + '"' + '</code>' +
                    '</pre>' +
                    '<pre class="idBox">' +
                    '<code class="apiNameTitle">"must_know_drink": </code>' +
                    '<code class="api_drink_name">' + drink.must_know_drink + '</code>' +
                    '</pre>' +
                    '<code class="openBrackets">},</code>'
                );
            },
            error: function(xhr, status, error) {
                console.error('Error fetching random drink:', error);
            }
        });
    });
});


document.getElementById("json").textContent = JSON.parse(random_drink, undefined, 2);

<<<<<<< HEAD
function toggleRawJsonViewOnPage() {


        const checkbox = document.getElementById('show_raw_json_on_page_checkbox');
        const showRawJsonOnPage = checkbox.checked ? 'yes' : 'no';

        // Update the URL without refreshing the page
        const url = new URL(window.location.href);
        url.searchParams.set('show_raw_json_on_page', showRawJsonOnPage);

        // Redirect to the new URL
        window.location.href = url.toString();

    }


function toggleRawJsonView() {

=======
function toggleRawJsonView() {


>>>>>>> c8d208825f0cfc7c98b00ca54db87b520edc37d5
        const checkbox = document.getElementById('show_raw_json_checkbox');
        const showRawJson = checkbox.checked ? 'yes' : 'no';

        // Update the URL without refreshing the page
        const url = new URL(window.location.href);
        url.searchParams.set('show_raw_json', showRawJson);

        // Redirect to the new URL
        window.location.href = url.toString();
<<<<<<< HEAD

=======
>>>>>>> c8d208825f0cfc7c98b00ca54db87b520edc37d5
    }


// {% if show_raw_json %}checked{% endif %}