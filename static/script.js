window.addEventListener('DOMContentLoaded', () => {

    // Realtime search results
    var input = document.querySelector('#search');

    input.addEventListener('input', async (e) => {

        if (!input) return;

        // Fetch url
        var response = await fetch('/search-rt?search=' + input.value);

        // Wait for response
        var result = await response.json();
        var html = '';

        // Show max 7 results
        result = result.slice(0, 7);

        // Create appropriate HTML
        for (var id in result) {

            // Only get movies and tv shows where poster is available
            if ((result[id].media_type == 'movie' || result[id].media_type == 'tv') && result[id].poster_path) {
                
                if (result[id].media_type == 'movie') {

                    var title = result[id].title.replace('<', '&lt;').replace('&', '&amp;');

                    // Using backticks and curly braces format
                    html += `<option onclick="window.location.href = '/movie/${result[id]["id"]}';">${title}</option>`;
                }
                else if (result[id].media_type == 'tv') {

                    var title = result[id].name.replace('<', '&lt;').replace('&', '&amp;');

                    // Using backticks and curly braces format
                    html += `<option onclick="window.location.href = '/movie/${result[id]["id"]}';">${title}</option>`;
                        
                }
            }
        }

        console.log(html)

        document.querySelector('#searchListOptions').innerHTML = html;

    });

    // Fetch post for movie/show
    var watchlist_form = document.querySelectorAll('.add-to-watchlist-form');
    
    // Add submit event to each form
    watchlist_form.forEach( (form) => {
        form.addEventListener('submit', async (e) => {
            console.log(form.elements[0].value);
            // Post movie_id to route

            form.classList.add('form-hidden');

            e.preventDefault();
        });
    });



});

