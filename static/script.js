window.addEventListener('DOMContentLoaded', () => {

    // Realtime search results
    var input = document.querySelector('#search');
    var search_result = document.querySelector('#search-result');

    input.addEventListener('input', async (e) => {

        if (!input) return;

        if (input.value === '') {
            search_result.style.opacity = '0';
        }
        else {
            search_result.style.opacity = '1';
        }

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
                    html += `<li class="d-flex flex-row my-1">
                                <form action="/movie/${result[id].id}" method="get">
                                    <input type="image" src="http://image.tmdb.org/t/p/w45/${result[id].poster_path}" alt="Poster" class="mx-2">
                                </form>
                                <div>
                                    <a class="text-decoration-none" href="/movie/${result[id].id}"> ${title} </a>
                                    <p class="text-muted"> Movie </p>
                                </div>
                            </li>`;
                }
                else if (result[id].media_type == 'tv') {

                    var title = result[id].name.replace('<', '&lt;').replace('&', '&amp;');

                    // Using backticks and curly braces format
                    html += `<li class="d-flex flex-row my-1">
                                <form action="/show/${result[id].id}" method="get">
                                    <input type="image" src="http://image.tmdb.org/t/p/w45/${result[id].poster_path}" alt="Poster" class="mx-2">
                                </form>
                                <div>
                                    <a class="text-decoration-none" href="/show/${result[id].id}"> ${title} </a>
                                    <p class="text-muted"> Show </p>
                                </div>
                            </li>`;
                        
                }
            }
        }

        document.querySelector('#search-result > ul').innerHTML = html;

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

// Switch tabs
function switchTabs(el) {
    // Switch tab classes
    var movies_tab = document.querySelector('#movies-tab');
    var shows_tab = document.querySelector('#shows-tab');

    if (el.classList.contains('active')) {
        return;
    }

    if (movies_tab.classList.contains('active')) {
        movies_tab.classList.remove('active');
        shows_tab.classList.add('active');
        document.querySelector('#shows-list').classList.remove('visually-hidden');
        document.querySelector('#movies-list').classList.add('visually-hidden');
    }
    else if (shows_tab.classList.contains('active')) {
        movies_tab.classList.add('active');
        shows_tab.classList.remove('active');
        document.querySelector('#shows-list').classList.add('visually-hidden');
        document.querySelector('#movies-list').classList.remove('visually-hidden');
    }
    
}
