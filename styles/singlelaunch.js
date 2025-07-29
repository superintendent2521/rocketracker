// New way: pluck final segment of /launch/<id>
const launchId = window.location.pathname.split('/').pop();

if (!launchId) {
  document.getElementById('launch-detail').innerText = 'missing launch id';
} else {
  fetch(`/api/getlaunches/${launchId}`)
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(launch => {
      document.getElementById('launch-detail').innerHTML = `
        <h3>Launch ${launch.launchDate} at ${launch.launchTime}</h3>
        <p><strong>Booster:</strong> ${launch.boosterNumber} (Flight #${launch.boosterFlightCount})</p>
        <p><strong>Ship:</strong> ${launch.shipNumber} (Flight #${launch.shipFlightCount})</p>
        <p><strong>Site:</strong> ${launch.launchSite}</p>
        ${launch.livestream ? `<p><a href="${launch.livestream}" target="_blank">View Livestream</a></p>` : ''}
      `;
    })
    .catch(() => {
      document.getElementById('launch-detail').innerText = 'failed to load launch';
    });
}