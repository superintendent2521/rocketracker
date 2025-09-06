// Booster Detail Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    loadBoosterDetails();
});

async function loadBoosterDetails() {
    try {
        // Extract booster ID from URL
        const pathParts = window.location.pathname.split('/');
        const boosterId = pathParts[pathParts.length - 1];
        
        if (!boosterId) {
            throw new Error('No booster ID provided');
        }
        
        // Fetch specific booster missions
        const response = await fetch(`/api/mission/booster/${encodeURIComponent(boosterId)}`);
        if (response.status === 429) {
            showError('ratelimit, slow down!');
            return;
        }
        if (!response.ok) {
            throw new Error('Failed to fetch booster data');
        }

        const boosterLaunches = await response.json();
        
        if (boosterLaunches.length === 0) {
            showError('Booster not found');
            return;
        }
        
        renderBoosterDetails(boosterId, boosterLaunches);
        
    } catch (error) {
        console.error('Error loading booster details:', error);
        showError('Failed to load booster details. Please try again later.');
    }
}

function renderBoosterDetails(boosterId, launches) {
    // Sort launches by date (newest first)
    launches.sort((a, b) => new Date(b.launchDate) - new Date(a.launchDate));
    
    // Calculate statistics
    const stats = {
        totalFlights: Math.max(...launches.map(l => l.boosterFlightCount || 0)),
        totalMissions: launches.length,
        launchSites: [...new Set(launches.map(l => l.launchSite))],
        firstLaunch: launches[launches.length - 1],
        lastLaunch: launches[0]
    };
    
    // Render header
    const header = document.getElementById('booster-header');
    header.innerHTML = `
        <h1>Booster ${boosterId}</h1>
        <div class="booster-id">Flight-Proven Booster</div>
    `;
    
    // Render statistics
    const statsContainer = document.getElementById('booster-stats');
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
                    <strong>Flight:</strong> ${launch.boosterFlightCount || 1}
                </div>
                <div class="mission-detail">
                    <strong>Status:</strong> ${launch.launchStatus || 'Unknown'}
                </div>
            </div>
        </div>
    `).join('');
}

function showError(message) {
    const header = document.getElementById('booster-header');
    const stats = document.getElementById('booster-stats');
    const missions = document.getElementById('missions-list');
    
    header.innerHTML = `<div class="error">${message}</div>`;
    stats.innerHTML = '';
    missions.innerHTML = '';
}
