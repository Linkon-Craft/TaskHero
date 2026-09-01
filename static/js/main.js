// =====================================================
// TASKHERO BROWSER NOTIFICATIONS
// =====================================================

let shownNotifications = new Set();


// -----------------------------------------------------
// Request browser notification permission
// -----------------------------------------------------

function requestNotificationPermission() {

    if (!("Notification" in window)) {

        console.log(
            "This browser does not support notifications."
        );

        return;
    }


    if (Notification.permission === "default") {

        Notification.requestPermission()
            .then(permission => {

                if (permission === "granted") {

                    console.log(
                        "TaskHero notifications enabled."
                    );

                } else {

                    console.log(
                        "TaskHero notifications denied."
                    );
                }

            })
            .catch(error => {

                console.error(
                    "Notification permission error:",
                    error
                );

            });
    }
}


// -----------------------------------------------------
// Show browser notification
// -----------------------------------------------------

function showNotification(title, options) {

    if (
        "Notification" in window &&
        Notification.permission === "granted"
    ) {

        new Notification(title, options);

    }
}


// -----------------------------------------------------
// Check Django notifications
// -----------------------------------------------------

function checkNotifications() {

    fetch("/get-notifications/", {

        method: "GET",

        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }

    })

    .then(response => {

        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );

        }

        return response.json();

    })

    .then(notifications => {

        notifications.forEach(notification => {

            // Prevent the same notification
            // from appearing repeatedly

            if (
                shownNotifications.has(
                    notification.id
                )
            ) {
                return;
            }


            shownNotifications.add(
                notification.id
            );


            showNotification(
                "TaskHero Reminder",
                {
                    body: notification.message,

                }
            );

        });

    })

    .catch(error => {

        console.error(
            "Notification check failed:",
            error
        );

    });
}


// -----------------------------------------------------
// Start notification system
// -----------------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    function () {

        requestNotificationPermission();


        // Check immediately

        checkNotifications();


        // Check every 30 seconds

        setInterval(
            checkNotifications,
            30000
        );

    }
);