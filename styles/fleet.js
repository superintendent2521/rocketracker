// Fleet Viewer JavaScript
document.addEventListener('DOMContentLoaded', function() {
    loadFleetData();
});

async function loadFleetData() {
    try {
        const response = await fetch('/api/getlaunches');
        if (!response.ok) {
            throw new Error('Failed to fetch launch data');
        }
        
        const launches = await response.json();
        processFleetData(launches);
    } catch (error) {
        console.error('Error loading fleet data:', error);
        showError('Failed to load fleet data. Please try again later.');
    }
}

function processFleetData(launches) {
    const boosters = new Map();
    const ships = new Map();
    
    // Process all launches to gather unique boosters and ships
    launches.forEach(launch => {
        // Process boosters
        const boosterNum = launch.boosterNumber;
        if (boosterNum) {
            if (!boosters.has(boosterNum)) {
                boosters.set(boosterNum, {
                    id: boosterNum,
                    flightCount: 0,
                    missions: [],
                    launchSites: new Set()
                });
            }
            const booster = boosters.get(boosterNum);
            booster.flightCount = Math.max(booster.flightCount, launch.boosterFlightCount || 0);
            booster.missions.push({
                id: launch._id,
                date: launch.launchDate,
                time: launch.launchTime,
                site: launch.launchSite
            });
            booster.launchSites.add(launch.launchSite);
        }
        
        // Process ships
        const shipNum = launch.shipNumber;
        if (shipNum) {
            if (!ships.has(shipNum)) {
                ships.set(shipNum, {
                    id: shipNum,
                    flightCount: 0,
                    missions: [],
                    launchSites: new Set()
                });
            }
            const ship = ships.get(shipNum);
            ship.flightCount = Math.max(ship.flightCount, launch.shipFlightCount || 0);
            ship.missions.push({
                id: launch._id,
                date: launch.launchDate,
                time: launch.launchTime,
                site: launch.launchSite
            });
            ship.launchSites.add(launch.launchSite);
        }
    });
    
    // Sort by flight count (descending)
    const sortedBoosters = Array.from(boosters.values())
        .sort((a, b) => b.flightCount - a.flightCount);
    
    const sortedShips = Array.from(ships.values())
        .sort((a, b) => b.flightCount - a.flightCount);
    
    renderFleetData(sortedBoosters, sortedShips);
}

function renderFleetData(boosters, ships) {
    renderFleetSection('boosters-list', boosters, 'Booster');
    renderFleetSection('ships-list', ships, 'Ship');
}

function renderFleetSection(containerId, items, type) {
    const container = document.getElementById(containerId);
    
    if (items.length === 0) {
        container.innerHTML = `
            <div class="empty-message">
                No ${type.toLowerCase()}s found in the database.
            </div>
        `;
        return;
    }
    
    const imgSrc = type === 'Booster' ? '/img/booster.jpg' : '/img/ship.jpg';
    
    container.innerHTML = items.map(item => `
        <div class="fleet-item">
        
            <!-- badge pulled up to card level -->
            <span class="id-badge">${item.id}</span>
        
            <div class="fleet-header">
                <div>
                    <h3>${type} ${item.id}</h3>
                </div>
                <img
                    src="${imgSrc}"
                    alt="${type} generic"
                    class="fleet-image"
                >
            </div>
            
            <div class="fleet-stats">
                <div class="stat-item">
                    <span class="stat-label">Total Flights:</span>
                    <span class="stat-value">${item.flightCount}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Launch Sites:</span>
                    <span class="stat-value">${Array.from(item.launchSites).join(', ') || 'N/A'}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Missions:</span>
                    <span class="stat-value">${item.missions.length}</span>
                </div>
            </div>
            
            <a
                href="/fleet/${type.toLowerCase()}/${encodeURIComponent(item.id)}"
                class="mission-link"
            >View Details</a>
        </div>
    `).join('');
}



function showError(message) {
    const boostersList = document.getElementById('boosters-list');
    const shipsList = document.getElementById('ships-list');
    
    boostersList.innerHTML = `<div class="error">${message}</div>`;
    shipsList.innerHTML = `<div class="error">${message}</div>`;
}

// Add active class to current nav item
document.addEventListener('DOMContentLoaded', function() {
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
});
