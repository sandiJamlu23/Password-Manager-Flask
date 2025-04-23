function createStrengthChart(score) {
    const ctx = document.getElementById('strengthChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [
                    getColorForScore(score),
                    '#e9ecef'
                ],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '70%',
            responsive: true,
            maintainAspectRatio: false,
            circumference: 180,
            rotation: 270,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function getColorForScore(score) {
    if (score < 25) return '#dc3545';
    if (score < 50) return '#ffc107';
    if (score < 75) return '#0dcaf0';
    return '#198754';
}

function updateStrengthMeter(password) {
    let score = 0;
    if (password.length >= 8) score += 25;
    if (password.match(/[A-Z]/)) score += 25;
    if (password.match(/[0-9]/)) score += 25;
    if (password.match(/[^A-Za-z0-9]/)) score += 25;
    
    createStrengthChart(score);
    
    const strengthText = document.getElementById('strengthText');
    if (score < 25) strengthText.textContent = 'Weak';
    else if (score < 50) strengthText.textContent = 'Fair';
    else if (score < 75) strengthText.textContent = 'Good';
    else strengthText.textContent = 'Strong';
}