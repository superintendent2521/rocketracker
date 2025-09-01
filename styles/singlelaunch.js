// New way: pluck final segment of /launch/<id>
const launchId = window.location.pathname.split('/').pop();

if (!launchId) {
  document.getElementById('launch-detail').innerHTML = `
    <div class="fleet-item">
      <h3>Error</h3>
      <p class="error">Missing launch ID</p>
    </div>
  `;
} else {
  fetch(`/api/getlaunches/${launchId}`)
    .then(r => {
      if (r.status === 429) {
        document.getElementById('launch-detail').innerHTML = `
          <div class="fleet-item">
            <h3>Error</h3>
            <p class="error">ratelimit, slow down!</p>
          </div>
        `;
        return Promise.reject('ratelimit');
      }
      return r.ok ? r.json() : Promise.reject(r.status);
    })
    .then(launch => {
      document.getElementById('launch-detail').innerHTML = `
        <div class="fleet-item">
          <h3>Launch ${launch.launchDate} at ${launch.launchTime}</h3>
          <div class="fleet-stats">
            <div class="stat-item">
              <span class="stat-label">Booster:</span>
              <span class="stat-value">${launch.boosterNumber} (Flight ${launch.boosterFlightCount})</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Ship:</span>
              <span class="stat-value">${launch.shipNumber} (Flight ${launch.shipFlightCount})</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Launch Site:</span>
              <span class="stat-value">${launch.launchSite}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Date:</span>
              <span class="stat-value">${launch.launchDate}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Time:</span>
              <span class="stat-value">${launch.launchTime}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Launch ID:</span>
              <span class="stat-value">${launch._id}</span>
            </div>
          </div>
          ${launch.livestream ? `<a href="${launch.livestream}" target="_blank" class="mission-link">View Livestream</a>` : ''}
          <a href="/viewer" class="mission-link">Back to Launch Viewer</a>
        </div>
        <div id="missions-section" style="margin-top: 2rem;">
          <h3>Missions</h3>
          <div id="missions-list">Loading missions...</div>
        </div>
      `;
      
      // Load missions for this launch
      loadMissions();
    })
    .catch(() => {
      document.getElementById('launch-detail').innerHTML = `
        <div class="fleet-item">
          <h3>Error</h3>
          <p class="error">Failed to load launch data</p>
          <a href="/viewer" class="mission-link">Back to Launch Viewer</a>
        </div>
      `;
    });
}

async function loadMissions() {
  try {
    const response = await fetch(`/api/missions/${launchId}`);
    if (response.status === 429) {
      document.getElementById('missions-list').innerHTML = '<p>ratelimit, slow down!</p>';
      return;
    }
    const missions = await response.json();

    const missionsList = document.getElementById('missions-list');

    if (missions.length === 0) {
      missionsList.innerHTML = `
        <p>No missions reported for this launch yet.</p>
        <a href="/missions/reporter" class="mission-link">Add Mission</a>
      `;
    } else {
      missionsList.innerHTML = missions.map(mission => `
        <div class="fleet-item" style="margin-bottom: 1rem;">
          <h4>${mission.mission_category.charAt(0).toUpperCase() + mission.mission_category.slice(1)} Mission</h4>
          <div class="fleet-stats">
            ${mission.starlink_count ? `<div class="stat-item"><span class="stat-label">Starlink Satellites:</span><span class="stat-value">${mission.starlink_count}</span></div>` : ''}
            ${mission.payload_description ? `<div class="stat-item"><span class="stat-label">Payload:</span><span class="stat-value">${mission.payload_description}</span></div>` : ''}
            ${mission.destination ? `<div class="stat-item"><span class="stat-label">Destination:</span><span class="stat-value">${mission.destination}</span></div>` : ''}
            ${mission.additional_notes ? `<div class="stat-item"><span class="stat-label">Notes:</span><span class="stat-value">${mission.additional_notes}</span></div>` : ''}
            <div class="stat-item"><span class="stat-label">Reported:</span><span class="stat-value">${new Date(mission.timestamp).toLocaleString()}</span></div>
          </div>
        </div>
      `).join('');

      missionsList.innerHTML += `<a href="/missions/reporter" class="mission-link">Add Another Mission</a>`;
    }
  } catch (error) {
    console.error('Error loading missions:', error);
    document.getElementById('missions-list').innerHTML = '<p>Error loading missions.</p>';
  }
}
