document.addEventListener('DOMContentLoaded', function() {
    const starsContainer = document.getElementById('stars-background');
    const starCount = 150
    console.log(starCount)
    const stars = [];
       // Create stars
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = Math.random() * 3 + 1 + 'px';
        star.style.height = star.style.width;
        star.style.backgroundColor = 'white';
        star.style.position = 'absolute';
        star.style.borderRadius = '50%';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.boxShadow = '0 0 ' + (Math.random() * 10 + 5) + 'px white';
        starsContainer.appendChild(star);
        stars.push({
            element: star,
            x: parseFloat(star.style.left),
            y: parseFloat(star.style.top),
            originalX: parseFloat(star.style.left),
            originalY: parseFloat(star.style.top),
            speedX: (Math.random() - 0.5) * 0.05, // Slower movement
            speedY: (Math.random() - 0.5) * 0.05, // Slower movement
            size: parseFloat(star.style.width)
        });
    }
    
    // Animation loop
    function animateStars() {
        stars.forEach(star => {
            // Update position
            star.x += star.speedX;
            star.y += star.speedY;
            
            // Wrap around edges
            if (star.x > 100) star.x = 0;
            if (star.x < 0) star.x = 100;
            if (star.y > 100) star.y = 0;
            if (star.y < 0) star.y = 100;
            
            // Apply new position
            star.element.style.left = star.x + '%';
            star.element.style.top = star.y + '%';
        });
        
        requestAnimationFrame(animateStars);
    }
    
    // Mouse movement effect
    document.addEventListener('mousemove', function(e) {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        stars.forEach(star => {
            const distX = mouseX - (star.x / 100);
            const distY = mouseY - (star.y / 100);
            const distance = Math.sqrt(distX * distX + distY * distY);
            
            if (distance < 0.3) { // Increased detection radius
                const force = (0.3 - distance) * 10; // Stronger force
                const moveX = distX * force * 30; // Increased movement
                const moveY = distY * force * 30; // Increased movement
                
                star.element.style.transform = `translate(${moveX}px, ${moveY}px)`;
            } else {
                star.element.style.transform = 'translate(0, 0)';
            }
        });
    });
    
    // Start animation
    animateStars();
});