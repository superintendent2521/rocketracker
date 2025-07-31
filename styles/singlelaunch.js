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
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
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
      `;
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
