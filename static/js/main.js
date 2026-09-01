// notification.js
function requestNotificationPermission() {
    if ('Notification' in window) {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('Notification permission granted.');
            } else {
                console.log('Notification permission denied.');
            }
        });
    }
}

function showNotification(title, options) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, options);
    }
}

// Example usage
requestNotificationPermission();

// Assuming you're using Django's template rendering
// and you have a way to fetch notifications (e.g., via AJAX)
fetch('/get-notifications/')
    .then(response => response.json())
    .then(notifications => {
        notifications.forEach(notification => {
            showNotification('New Notification', {
                body: notification.message,
                icon: '/path/to/icon.png'
            });
        });
    });
