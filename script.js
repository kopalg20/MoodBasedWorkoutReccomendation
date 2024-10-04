const apiKey = 'AIzaSyAo5R3FhcE2wY8CgQmrRZd7yxM9ipKntJo'; // Replace with your YouTube API key

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

// Capture the search input and suggestions
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
                searchInput.value = option; // Fill the input with the clicked suggestion
                suggestionsContainer.innerHTML = ''; // Clear suggestions
                searchYouTube(option); // Initiate search
            });
            suggestionsContainer.appendChild(suggestionItem);
        });
    }
});

// Handle search form submission
document.getElementById('youtube-search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    const query = searchInput.value;
    if (query) {
        searchYouTube(query);
    }
});

// Search YouTube
function searchYouTube(query) {
    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&type=video&q=${encodeURIComponent(query)}&key=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayResults(data.items);
        })
        .catch(error => console.error('Error:', error));
}

// Display video results
function displayResults(videos) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    videos.forEach(video => {
        // Skip non-video results
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