async function displayLaunches() {
  // Create output element if it doesn't exist
  let outputElement = document.getElementById('output');
  if (!outputElement) {
    outputElement = document.createElement('pre');
    outputElement.id = 'output';
    document.body.appendChild(outputElement);
  }

  try {
    const response = await fetch('/api/getlaunches');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    
    const data = await response.json();
    const cleanedMessage = data.message
      .replace(/ObjectId\('[^']+'\)/g, '""')
      .replace(/'/g, '"');
    
    const launches = JSON.parse(cleanedMessage);
    
    const formattedText = launches.map(launch => 
      `Booster ${launch.boosterNumber} (Flight ${launch.boosterFlightCount})
       Ship ${launch.shipNumber} (Flight ${launch.shipFlightCount})
       Launch: ${launch.launchDate} at ${launch.launchTime}
       Site: ${launch.launchSite}
       -------------------------`
    ).join('\n');

    outputElement.textContent = formattedText;
  } catch (error) {
    console.error('Error:', error);
    outputElement.textContent = 'Error loading data: ' + error.message;
  }
}

document.addEventListener('DOMContentLoaded', displayLaunches);