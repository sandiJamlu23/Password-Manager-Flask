document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const strengthCircle = document.getElementById('strength-circle');
    const strengthPercentage = document.getElementById('strength-percentage');
    const strengthMeterText = document.getElementById('strength-meter-text');
    const reqLength = document.getElementById('req-length');
    const reqUppercase = document.getElementById('req-uppercase');
    const reqLowercase = document.getElementById('req-lowercase');
    const reqNumber = document.getElementById('req-number');
    const reqSpecial = document.getElementById('req-special');
    
    const circleCircumference = 2 * Math.PI * 45; // 2πr
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const strength = calculatePasswordStrength(password);
        
        // Update circular progress
        const offset = circleCircumference - (strength / 100) * circleCircumference;
        if (strengthCircle) {
            strengthCircle.style.strokeDashoffset = offset;
        }
        
        // Update percentage text
        strengthPercentage.textContent = `${strength}%`;
        
        // Update strength description and color
        let strengthColor, strengthDesc;
        
        if (strength < 30) {
            strengthColor = '#dc3545'; // red (danger)
            strengthDesc = 'Weak';
            strengthMeterText.className = 'alert alert-danger';
        } else if (strength < 60) {
            strengthColor = '#f0ad4e'; // orange (warning)
            strengthDesc = 'Moderate';
            strengthMeterText.className = 'alert alert-warning';
        } else if (strength < 80) {
            strengthColor = '#5bc0de'; // blue (info)
            strengthDesc = 'Good';
            strengthMeterText.className = 'alert alert-info';
        } else {
            strengthColor = '#5cb85c'; // green (success)
            strengthDesc = 'Strong';
            strengthMeterText.className = 'alert alert-success';
        }
        
        strengthCircle.style.stroke = strengthColor;
        strengthMeterText.textContent = `Password strength: ${strengthDesc}`;
        
        // Update requirements
        updateRequirement(reqLength, password.length >= 8);
        updateRequirement(reqUppercase, /[A-Z]/.test(password));
        updateRequirement(reqLowercase, /[a-z]/.test(password));
        updateRequirement(reqNumber, /[0-9]/.test(password));
        updateRequirement(reqSpecial, /[^A-Za-z0-9]/.test(password));
    });
    
    function calculatePasswordStrength(password) {
        if (!password) return 0;
        
        let score = 0;
        
        // Basic length score
        if (password.length > 0) {
            score += Math.min(password.length * 4, 25); // Max 25 points for length
        }
        
        // Character type scores
        const typesCount = [
            /[A-Z]/.test(password), // uppercase
            /[a-z]/.test(password), // lowercase
            /[0-9]/.test(password), // numbers
            /[^A-Za-z0-9]/.test(password) // special chars
        ].filter(Boolean).length;
        
        score += typesCount * 15; // 15 points per character type
        
        // Complexity bonus
        if (typesCount >= 3 && password.length >= 8) {
            score += 20;
        }
        
        // Middle numbers or symbols
        const middleChars = password.slice(1, -1).match(/[0-9!@#$%^&*()]/g);
        if (middleChars) {
            score += middleChars.length * 2;
        }
        
        // Cap at 100
        return Math.min(Math.round(score), 100);
    }
    
    function updateRequirement(element, isValid) {
        if (isValid) {
            element.querySelector('.check').textContent = '✅';
        } else {
            element.querySelector('.check').textContent = '❌';
        }
    }
});