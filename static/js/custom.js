/**
 * Custom JavaScript for Task Manager application
 */

// Initialize tooltips when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all elements that have the data-bs-toggle="tooltip" attribute
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    
    // Initialize tooltips on all matching elements
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    console.log('Tooltips initialized successfully');
});

