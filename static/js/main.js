// Main JavaScript for Truth Behind the Tagline

document.addEventListener('DOMContentLoaded', function() {
    // Handle sample claim selection
    const sampleClaims = document.querySelectorAll('.sample-claim');
    sampleClaims.forEach(claim => {
        claim.addEventListener('click', function() {
            // Get data attributes
            const brand = this.getAttribute('data-brand');
            const tagline = this.getAttribute('data-tagline');
            const claimText = this.getAttribute('data-claim');
            
            // Fill the form
            document.getElementById('brand_name').value = brand;
            document.getElementById('tagline').value = tagline;
            document.getElementById('claim').value = claimText;
            
            // Scroll to form
            document.getElementById('brand_name').scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add animation to progress bars on results page
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        // Start with width 0
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        // Animate to target width
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = targetWidth;
        }, 300);
    });
});
