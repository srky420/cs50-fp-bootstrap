window.addEventListener('DOMContentLoaded', () => {

    // Carousel slides
    var slides = document.querySelectorAll('.slide');
    if (slides.length > 0) {
        slides[Math.round(Math.random())].classList.add('active-slide');

        // Next slide
        document.querySelector('.carousel-btn.next').addEventListener('click', (e) => {
            nextSlide(slides);
        });

        // Prev slide
        document.querySelector('.carousel-btn.prev').addEventListener('click', (e) => {
            prevSlide(slides);  
        });
    }

    // Realtime search results
    var input = document.querySelector('#search');

    input.addEventListener('input', async (e) => {

        if (!input) return;

        document.querySelector('.search-result').style.opacity = '1';

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
                    html += `<li>
                                <form action="/movie/${result[id].id}" method="get">
                                    <input type="image" src="http://image.tmdb.org/t/p/w500/${result[id].poster_path}" alt="Poster">
                                </form>
                                <div>
                                    <a class="text-w" href="/movie/${result[id].id}"> ${title} </a>
                                    <p class="text-g"> Movie </p>
                                </div>
                            </li>`;
                }
                else if (result[id].media_type == 'tv') {

                    var title = result[id].name.replace('<', '&lt;').replace('&', '&amp;');

                    // Using backticks and curly braces format
                    html += `<li>
                                <form action="/show/${result[id].id}" method="get">
                                    <input type="image" src="http://image.tmdb.org/t/p/w500/${result[id].poster_path}" alt="Poster">
                                </form>
                                <div>
                                    <a class="text-w" href="/show/${result[id].id}"> ${title} </a>
                                    <p class="text-g"> Show </p>
                                </div>
                            </li>`;
                        
                }
            }
        }

        document.querySelector('.search-result > ul').innerHTML = html;

    });

    // Burger
    var burger = document.querySelector('.burger');
    burger.addEventListener('click', (e) => {
        document.querySelector('.nav-right').classList.toggle('nav-right-visible');
    });
});

// Activate next slide function
function nextSlide(slides) {
    
    var currentIndex = [...slides].indexOf(document.querySelector('.active-slide'));
    var newIndex = currentIndex + 1;

    if (newIndex > slides.length - 1) {
        newIndex = 0;
    }
    
    slides[currentIndex].classList.remove('active-slide');
    slides[newIndex].classList.add('active-slide');

    // Rest slideshow timer
    clearInterval(interval);
    interval = setInterval(nextSlide, 5000, slides);
}

// Activate previous slide function
function prevSlide(slides) {
    
    var currentIndex = [...slides].indexOf(document.querySelector('.active-slide'));
    var newIndex = currentIndex - 1;

    if (newIndex < 0) {
        newIndex = slides.length - 1;
    }
    
    slides[currentIndex].classList.remove('active-slide');
    slides[newIndex].classList.add('active-slide');

    // Rest slideshow timer
    clearInterval(interval);
    interval = setInterval(nextSlide, 5000, slides);
}


// Auto slideshow
var slides = document.querySelectorAll('.slide');
if (slides.length > 0) {
    var interval = setInterval(nextSlide, 5000, slides);
}