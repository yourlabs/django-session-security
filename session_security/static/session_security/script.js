// Simple function that adds a number of seconds to a Date object.
//
// Example usage, to add two seconds to a date:
//
//     d = new Date();
//     addSeconds(d, 120);
function addSeconds(date, seconds) {
    var sum = date.getSeconds() + seconds;
    date.setSeconds(sum);
    return date;
}

// An **global instance** of `SessionSecurity` is instanciated as such by the
// default setup (all.html):
//
//     sessionSecurity = new SessionSecurity();
//     sessionSecurity = $.extend(SessionSecurity, {
//         // define overrides here
//     });
//     sessionSecurity.initialize()
var SessionSecurity = function() {
    // **HTML element** that should show to warn the user that his session will
    // expire.
    this.warningElement = $('#session_security_warning');

    // **Callback** for when session expires.
    this.expire = function() {
        $.get(this.LOGOUT_URL, function() {
            var url = sessionSecurity.LOGIN_URL + '?next=' + document.location.pathname;
            $('body').html('Your session has expired. <a href="' + url + '">Login again</a>');
        });
    }

    // **Callback** that should display the warning.
    this.warn = function() {
        this.warningElement.fadeIn();
    }

    // **Callback** for activity events, mouse move, keyboard move, scroll ...
    // 
    // **Beware**: it is bind as function, which means that `this` will **not**
    // refer to the SessionSecurity instance. Use `sessionSecurity` global
    // variable instead of `this`.
    this.activity = function() {
        sessionSecurity.lastActivity = new Date();

        if (sessionSecurity.warningElement.is(':visible')) {
            sessionSecurity.warningElement.hide();

            // Cancel the next programed tick.
            clearTimeout(sessionSecurity.timeout);
            // Tick now, to upload last activity time to the server.
            sessionSecurity.tick(true);
        }
    }

    this.tick = function(activity) {
        var now = new Date();
        if (activity) {
            // Was called from `activity()`, update the server's
            // `last_activity`.
            var sinceActivity = Math.floor((now - sessionSecurity.lastActivity)
                / 1000);
        } else {
            // Was called to warn or expire, don't update the server.
            var sinceActivity = -1;
        }

        $.get(
            sessionSecurity.pingUrl, 
            {
                'sinceActivity': sinceActivity,
                'csrfmiddlewaretoken': sessionSecurity.token,
            },
            function(data, textStatus, jqXHR) {
                // If `sinceActivity` is different between the server and the
                // client:
                if (sinceActivity != parseInt(data)) {
                    var sinceActivity = parseInt(data);
                    sessionSecurity.lastActivity = addSeconds(new Date(), sinceActivity * -1);
                }

                // Pre-calculate in how many seconds to warn or expire using
                // `sinceActivity` which might have been updated (see above).
                expireIn = sessionSecurity.EXPIRE_AFTER - sinceActivity;
                warnIn = sessionSecurity.WARN_AFTER - sinceActivity;

                if (expireIn <= 0) {
                    // No time left before expiration.
                    sessionSecurity.expire();
                } else if (warnIn <= 0) {
                    // No time left before warning.
                    sessionSecurity.warn();

                    // As time goes by, we want to poll the server for last
                    // activity updates (maybe done in another browser tab)
                    // more often:
                    //
                    // - If the session should
                    //   **expire in 5 seconds**, then we want to **poll in 2**,
                    // - If the session should **expire in 2 seconds**, then we
                    //   want to **poll in 1**.
                    var next = expireIn / 2;

                    next = next < 1 ? 1 : next;

                    sessionSecurity.timeout = setTimeout(sessionSecurity.tick, 
                        next * 1000);
                } else {
                    // Apparently there is still time, tick at the next
                    // expected warning time, before displaying the warning.
                    sessionSecurity.warningElement.hide();
                    sessionSecurity.timeout = setTimeout(sessionSecurity.tick, 
                        warnIn * 1000);
                }
            }
        );
    }

    this.initialize = function() {
        // Initiate `this.lastActivity`.
        this.lastActivity = new Date();

        // Try to monitor for activity in the page.
        $(document).scroll(this.activity);
        $(document).keyup(this.activity);
        $(document).mousemove(this.activity);
        $(document).click(this.activity);

        // Tick when warning time is expected.
        this.timeout = setTimeout(sessionSecurity.tick, this.WARN_AFTER*1000);
    }
}

