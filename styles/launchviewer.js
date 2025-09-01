// Fetch and display launch data
async function fetchLaunches() {
    try {
        const response = await fetch('/api/getlaunches');
        if (response.status === 429) {
            document.getElementById('launch-cards').innerHTML = '<div class="error">ratelimit, slow down!</div>';
            return;
        }
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Handle response which might be wrapped in a message object
        const data = await response.json();

        // Extract launches array (either directly or from message property)
        const launches = Array.isArray(data) ? data :
                          (data.message && Array.isArray(data.message) ? data.message :
                          (data.launches && Array.isArray(data.launches) ? data.launches : []));

        displayLaunches(launches);
    } catch (error) {
        console.error('Error fetching launches:', error);
        document.getElementById('launch-cards').innerHTML = '<div class="error">Error loading launch data</div>';
    }
}

function displayLaunches(launches) {
    const container = document.getElementById('launch-cards');
    
    if (!Array.isArray(launches) || launches.length === 0) {
        container.innerHTML = '<div class="empty-message">No launches found</div>';
        return;
    }
    
    container.innerHTML = launches.map(launch => `
        <div class="fleet-item">
            <h3>Launch ${launch.launchDate} at ${launch.launchTime}</h3>
            <div class="fleet-stats">
                <div class="stat-item">
                    <span class="stat-label">Booster:</span>
                    <span class="stat-value">${launch.boosterNumber} (Flight #${launch.boosterFlightCount})</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Ship:</span>
                    <span class="stat-value">${launch.shipNumber} (Flight #${launch.shipFlightCount})</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Site:</span>
                    <span class="stat-value">${launch.launchSite}</span>
                </div>
            </div>
            ${launch.livestream ? `<a href="${launch.livestream}" target="_blank" class="mission-link">View Livestream</a>` : ''}
            <a href="/launch/${launch._id}" class="mission-link">View Details</a>
            <p style="font-size:0.6em;color:#888;margin:10px 0 0 0;line-height:1;">ID: ${launch._id}</p>
        </div>
    `).join('');
}

// Load launches when page loads
document.addEventListener('DOMContentLoaded', fetchLaunches);
