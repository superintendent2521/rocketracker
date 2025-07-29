// Fetch and display launch data
async function fetchLaunches() {
    try {
        const response = await fetch('/api/getlaunches');
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
        document.getElementById('launch-cards').innerHTML = '<p>Error loading launch data</p>';
    }
}
function displayLaunches(launches) {
    const container = document.getElementById('launch-cards');
    
    if (!Array.isArray(launches) || launches.length === 0) {
        container.innerHTML = '<p>No launches found</p>';
        return;
    }
    
    container.innerHTML = launches.map(launch => `
        <div class="launch-card">
            <h3>Launch ${launch.launchDate} at ${launch.launchTime}</h3>
            <p><strong>Booster:</strong> ${launch.boosterNumber} (Flight #${launch.boosterFlightCount})</p>
            <p><strong>Ship:</strong> ${launch.shipNumber} (Flight #${launch.shipFlightCount})</p>
            <p><strong>Site:</strong> ${launch.launchSite}</p>
            ${launch.livestream ? `<p><a href="${launch.livestream}" target="_blank">View Livestream</a></p>` : ''}
            <a href="/launch/${launch._id}" style="position:absolute;bottom:35px;right:15px;color:blue;text-decoration:none;font-size:0.8em;"><button>Details</button></a>
            <p style="position:absolute;bottom:3px;right:5px;font-size:0.6em;color:#888;margin:0;line-height:1;">ID: ${launch._id}</p>
        </div>
    `).join('');
}

// Load launches when page loads
document.addEventListener('DOMContentLoaded', fetchLaunches);