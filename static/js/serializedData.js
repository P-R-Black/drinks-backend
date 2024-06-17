
$(document).ready(function() {
            $('#formSubmit').on('submit', function(e) {
                e.preventDefault(); // Prevent the page from reloading
                var formData = $(this).serialize();

                $.ajax({
                    type: 'POST',
                    url: '/',
                    data: formData,
                    success: function(response) {
                        var resultsDiv = $('#results');
                        var displayArea = $('.displayArea')
                        resultsDiv.empty(); // Clear previous results
                        var data = response.data;

                        data.forEach(function(item) {
                        displayArea.addClass('addBackgroundColor')
                            resultsDiv.append(
                                '<code class="openBrackets">{</code>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"id": </code>' +
                                '<code class="api_drink_name">' + item.id +'</code>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"drink_name": </code>' +
                                '<code class="api_drink_name">' + '"' + item.drink_name + '"' + '</code>' +
                                '</pre>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"slug": </code>' +
                                '<code class="api_drink_name">' + '"' + item.slug + '"' + '</code>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"profile": </code>' +
                                '<code class="api_drink_name">' + '"' + item.profile + '"' + '</code>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"base_alcohol": </code>' +
                                '<code class="api_drink_name">' + '[' + '"' + item.base_alcohol + '"' + ']' + '</code>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"ingredient_name": </code>' +
                                '<code class="api_drink_name">' + '[' + '"' + item.ingredient_name + '"' + ']' + '</code>' +
                                '</pre>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"garnish": </code>' +
                                '<code class="api_drink_name">' + '"' + item.garnish + '"' + '</code>' +
                                '</pre>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"serving_glass": </code>' +
                                '<code class="api_drink_name">' + '"' + item.serving_glass + '"' + '</code>' +
                                '</pre>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"mixing_direction": </code>' +
                                '<code class="api_drink_name api_mix_name">' + '"' + item.mixing_direction + '"' + '</code>' +
                                '</pre>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"drink_type": </code>' +
                                '<code class="api_drink_name">' + '"' + item.drink_type + '"' + '</code>' +
                                '</pre>' +
                                '</pre>' +
                                '<pre class="idBox">' +
                                '<code class="apiNameTitle">"must_know_drink": </code>' +
                                '<code class="api_drink_name">' + item.must_know_drink + '</code>' +
                                '</pre>' +

                                '<code class="openBrackets">},</code>'
                            );
                        });
                    }
                });
            });
        });

