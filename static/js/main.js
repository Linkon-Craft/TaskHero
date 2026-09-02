console.log("TaskHero notification script loaded.");


// =====================================================
// TRACK NOTIFICATIONS ALREADY SHOWN
// =====================================================

let shownNotifications = new Set();


// =====================================================
// ENABLE BROWSER NOTIFICATIONS
// =====================================================

const notificationButton =
    document.getElementById("enable-notifications");


if (notificationButton) {

    notificationButton.addEventListener(
        "click",
        async function () {

            console.log("Notification button clicked.");

            if (!("Notification" in window)) {

                alert(
                    "Your browser does not support notifications."
                );

                return;
            }

            const permission =
                await Notification.requestPermission();

            console.log(
                "Notification permission:",
                permission
            );

            if (permission === "granted") {

                // Test that browser notifications work
                new Notification(
                    "TaskHero Notifications Enabled",
                    {
                        body:
                            "You will now receive TaskHero reminders."
                    }
                );

            } else {

                alert(
                    "Please allow notifications for TaskHero."
                );
            }
        }
    );
}


// =====================================================
// CHECK DJANGO NOTIFICATIONS
// =====================================================

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

        console.log(
            "Notifications received:",
            notifications
        );


        notifications.forEach(notification => {

            // Don't show the same notification
            // repeatedly during this browser session

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


            // Show the REAL Django notification

            if (
                "Notification" in window &&
                Notification.permission === "granted"
            ) {

                new Notification(
                    "TaskHero Reminder",
                    {
                        body: notification.message
                    }
                );

            }

        });

    })

    .catch(error => {

        console.error(
            "Notification check failed:",
            error
        );

    });
}


// =====================================================
// START NOTIFICATION CHECKING
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        // Check immediately after page loads

        checkNotifications();


        // Check every 30 seconds

        setInterval(
            checkNotifications,
            30000
        );

    }
);