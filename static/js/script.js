const apiKey = 'AIzaSyAo5R3FhcE2wY8CgQmrRZd7yxM9ipKntJo';

// List of predefined search options
const searchOptions = [
    'Zumba',
    'Dance',
    'Body-Weight exercise',
    'Pilates',
    'Guided-visualization meditation',
    'Body Scan',
    'Mindfulness Meditation',
    'Gratitude Meditation',
    'Love-kindness Meditation',
    'breathe awareness','hatha yoga','vinyasa flow','power yoga','light streching','yin yoga','triangle pose','seated twist','sphinx pose','child pose','cat cow pose','restorative yoga'

];

const searchInput = document.getElementById('search-query');
const suggestionsContainer = document.getElementById('suggestions');

searchInput.addEventListener('input', function() {
    const query = this.value.toLowerCase();
    suggestionsContainer.innerHTML = '';

    if (query) {
        const filteredOptions = searchOptions.filter(option => option.toLowerCase().includes(query));
        
        filteredOptions.forEach(option => {
            const suggestionItem = document.createElement('div');
            suggestionItem.textContent = option;
            suggestionItem.className = 'suggestion-item';
            suggestionItem.addEventListener('click', () => {
                searchInput.value = option;
                suggestionsContainer.innerHTML = '';
                searchYouTube(option);
            });
            suggestionsContainer.appendChild(suggestionItem);
        });
    }
});

document.getElementById('youtube-search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = searchInput.value;
    if (query) {
        searchYouTube(query);
    }
});

function searchYouTube(query) {
    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&type=video&q=${encodeURIComponent(query)}&key=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResults(data.items);
        })
        .catch(error => console.error('Error:', error));
}

function displayResults(videos) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    videos.forEach(video => {
        if (!video.id.videoId) return;
        
        const videoElement = `
            <div>
                <h3>${video.snippet.title}</h3>
                <iframe src="https://www.youtube.com/embed/${video.id.videoId}" frameborder="0" allowfullscreen></iframe>
            </div>
        `;
        resultsDiv.innerHTML += videoElement;
    });
}
function toggleOverlay(element) {
    var card = element.closest('.card');
    card.classList.toggle('active');
}
