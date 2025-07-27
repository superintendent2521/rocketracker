async function displayLaunches() {
  const container = document.getElementById('launch-cards');
  if (!container) {
    console.error('Launch cards container not found');
    return;
  }

  try {
    const response = await fetch('/api/getlaunches');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    const cleanedMessage = data.message
      .replace(/ObjectId\('[^']+'\)/g, '""')
      .replace(/'/g, '"');
    
    const launches = JSON.parse(cleanedMessage);
    
    launches.forEach(launch => {
      const card = document.createElement('div');
      card.className = 'launch-card';
      
      const title = document.createElement('div');
      title.className = 'launch-title';
      title.textContent = `Booster ${launch.boosterNumber}-${launch.boosterFlightCount} | Ship ${launch.shipNumber}-${launch.shipFlightCount}`;
      
      const details = document.createElement('div');
      details.className = 'launch-details';
      details.innerHTML = `
        <div>${launch.launchSite}</div>
        <div>${launch.launchDate} at ${launch.launchTime}</div>
      `;
      
      card.appendChild(title);
      card.appendChild(details);
      container.appendChild(card);
    });

  } catch (error) {
    console.error('Error:', error);
    const errorElement = document.createElement('div');
    errorElement.textContent = 'Error loading data: ' + error.message;
    container.appendChild(errorElement);
  }
}

document.addEventListener('DOMContentLoaded', displayLaunches);