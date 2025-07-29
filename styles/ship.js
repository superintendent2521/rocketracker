// Ship Detail Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    loadShipDetails();
});

async function loadShipDetails() {
    try {
        // Extract ship ID from URL
        const pathParts = window.location.pathname.split('/');
        const shipId = pathParts[pathParts.length - 1];
        
        if (!shipId) {
            throw new Error('No ship ID provided');
        }
        
        // Fetch specific ship missions
        const response = await fetch(`/api/mission/ship/${encodeURIComponent(shipId)}`);
        if (!response.ok) {
            throw new Error('Failed to fetch ship data');
        }
        
        const shipLaunches = await response.json();
        
        if (shipLaunches.length === 0) {
            showError('Ship not found');
            return;
        }
        
        renderShipDetails(shipId, shipLaunches);
        
    } catch (error) {
        console.error('Error loading ship details:', error);
        showError('Failed to load ship details. Please try again later.');
    }
}

function renderShipDetails(shipId, launches) {
    // Sort launches by date (newest first)
    launches.sort((a, b) => new Date(b.launchDate) - new Date(a.launchDate));
    
    // Calculate statistics
    const stats = {
        totalFlights: Math.max(...launches.map(l => l.shipFlightCount || 0)),
        totalMissions: launches.length,
        launchSites: [...new Set(launches.map(l => l.launchSite))],
        firstLaunch: launches[launches.length - 1],
        lastLaunch: launches[0]
    };
    
    // Render header
    const header = document.getElementById('ship-header');
    header.innerHTML = `
        <h1>Ship ${shipId}</h1>
        <div class="ship-id">Flight-Proven Ship</div>
    `;
    
    // Render statistics
    const statsContainer = document.getElementById('ship-stats');
    statsContainer.innerHTML = `
        <div class="stat-card">
            <span class="stat-number">${stats.totalFlights}</span>
            <span class="stat-label">Total Flights</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">${stats.totalMissions}</span>
            <span class="stat-label">Total Missions</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">${stats.launchSites.length}</span>
            <span class="stat-label">Launch Sites</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">${stats.firstLaunch ? new Date(stats.firstLaunch.launchDate).toLocaleDateString() : 'N/A'}</span>
            <span class="stat-label">First Launch</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">${stats.lastLaunch ? new Date(stats.lastLaunch.launchDate).toLocaleDateString() : 'N/A'}</span>
            <span class="stat-label">Latest Launch</span>
        </div>
    `;
    
    // Render missions
    const missionsContainer = document.getElementById('missions-list');
    missionsContainer.innerHTML = launches.map(launch => `
        <div class="mission-card">
            <h3>Mission ${launch.missionName || 'Unknown'}</h3>
            <div class="mission-details">
                <div class="mission-detail">
                    <strong>Date:</strong> ${new Date(launch.launchDate).toLocaleDateString()}
                </div>
                <div class="mission-detail">
                    <strong>Time:</strong> ${launch.launchTime || 'TBD'}
                </div>
                <div class="mission-detail">
                    <strong>Site:</strong> ${launch.launchSite || 'Unknown'}
                </div>
                <div class="mission-detail">
                    <strong>Flight:</strong> ${launch.shipFlightCount || 1}
                </div>
                <div class="mission-detail">
                    <strong>Status:</strong> ${launch.launchStatus || 'Unknown'}
                </div>
            </div>
        </div>
    `).join('');
}

function showError(message) {
    const header = document.getElementById('ship-header');
    const stats = document.getElementById('ship-stats');
    const missions = document.getElementById('missions-list');
    
    header.innerHTML = `<div class="error">${message}</div>`;
    stats.innerHTML = '';
    missions.innerHTML = '';
}
