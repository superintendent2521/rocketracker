// Fetch and display specific launch data
async function fetchLaunch() {
    try {
        // Get launch ID from URL query parameter
        const urlParams = new URLSearchParams(window.location.search);
        const launchId = urlParams.get('id');
        
        if (!launchId) {
            document.getElementById('launch-detail').innerHTML = '<p>No launch ID specified</p>';
            return;
        }
        
        const response = await fetch(`/api/getlaunch/${launchId}`);
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Launch not found');
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        }
        
        const launch = await response.json();
        displayLaunch(launch);
    } catch (error) {
        console.error('Error fetching launch:', error);
        document.getElementById('launch-detail').innerHTML = `<p>Error loading launch data: ${error.message}</p>`;
    }
}

function displayLaunch(launch) {
    const container = document.getElementById('launch-detail');
    
    if (!launch) {
        container.innerHTML = '<p>No launch data available</p>';
        return;
    }
    
    container.innerHTML = `
        <div class="launch-detail-card">
            <h2>Launch on ${launch.launchDate} at ${launch.launchTime}</h2>
            <table>
                <tr>
                    <th>Booster</th>
                    <td>${launch.boosterNumber} (Flight #${launch.boosterFlightCount})</td>
                </tr>
                <tr>
                    <th>Ship</th>
                    <td>${launch.shipNumber} (Flight #${launch.shipFlightCount})</td>
                </tr>
                <tr>
                    <th>Launch Site</th>
                    <td>${launch.launchSite}</td>
                </tr>
                ${launch.livestream ? `
                <tr>
                    <th>Livestream</th>
                    <td><a href="${launch.livestream}" target="_blank">View Livestream</a></td>
                </tr>` : ''}
                <tr>
                    <th>Submitted</th>
                    <td>${launch.timestamp ? new Date(launch.timestamp).toLocaleString() : 'Unknown'}</td>
                </tr>
                <tr>
                    <th>Launch ID</th>
                    <td>${launch._id}</td>
                </tr>
            </table>
        </div>
    `;
}

// Load launch when page loads
document.addEventListener('DOMContentLoaded', fetchLaunch);