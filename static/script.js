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

    // Fetch post for adding/removing movies
    // For adding movies
    var add_movie_form = document.querySelectorAll('.add-movie-form');

    add_movie_form.forEach( (form) => {
        form.addEventListener('submit', async (e) => {
            console.log(form.elements[0].value, 'add');

            form.classList.add('form-hidden');

            var header = {
                method: 'POST'
            }

            fetch('/add-movie/' + form.elements[0].value, header)
            .then( (res) => res.json() )
            .then( (data) => {
                    console.log(data)
                    console.log(form.nextSibling.nextElementSibling);
                    form.nextSibling.nextElementSibling.classList.remove('form-hidden');
                }
            );

            e.preventDefault();
        });
    });

    // For removing movies
    var remove_movie_form = document.querySelectorAll('.remove-movie-form');

    remove_movie_form.forEach( (form) => {
        form.addEventListener('submit', async (e) => {
            console.log(form.elements[0].value, 'remove');

            form.classList.add('form-hidden');

            var header = {
                method: 'POST'
            }

            fetch('/remove-movie/' + form.elements[0].value, header)
            .then( (res) => res.json() )
            .then( (data) => {
                    console.log(data)
                    console.log(form.previousSibling.previousElementSibling);
                    form.previousSibling.previousElementSibling.classList.remove('form-hidden');
                }
            );

            e.preventDefault();
        });
    });

    // For adding shows
    var add_show_form = document.querySelectorAll('.add-show-form');

    add_show_form.forEach( (form) => {
        form.addEventListener('submit', async (e) => {
            console.log(form.elements[0].value, 'add');

            form.classList.add('form-hidden');

            var header = {
                method: 'POST'
            }

            fetch('/add-show/' + form.elements[0].value, header)
            .then( (res) => res.json() )
            .then( (data) => {
                    console.log(data)
                    console.log(form.nextSibling.nextElementSibling);
                    form.nextSibling.nextElementSibling.classList.remove('form-hidden');
                }
            );

            e.preventDefault();
        });
    });

    // For adding shows
    var remove_show_form = document.querySelectorAll('.remove-show-form');

    remove_show_form.forEach( (form) => {
        form.addEventListener('submit', async (e) => {
            console.log(form.elements[0].value, 'add');

            form.classList.add('form-hidden');

            var header = {
                method: 'POST'
            }

            fetch('/remove-show/' + form.elements[0].value, header)
            .then( (res) => res.json() )
            .then( (data) => {
                    console.log(data)
                    console.log(form.previousSibling.previousElementSibling);
                    form.previousSibling.previousElementSibling.classList.remove('form-hidden');
                }
            );

            e.preventDefault();
        });
    });

});

/* If browser back button was used, flush cache */

window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload();
    }
};
