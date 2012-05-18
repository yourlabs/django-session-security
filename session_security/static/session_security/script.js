// Simple function that adds a number of seconds to a Date object.
//
// Example usage::
//
//     d = new Date();
//     addSeconds(d, 120);
//
// Make d 2 minutes later
function addSeconds(date, seconds) {
    var sum = date.getSeconds() + seconds;

    // @todo: reverse the number of minutes depending on seconds
    if (sum > 59) {
        date.setMinutes(date.getMinutes() + 1)
        date.setSeconds(sum - 60);
    } else if (sum < 1) {
        date.setMinutes(date.getMinutes() - 1)
        date.setSeconds(sum + 60);
    } else {
        date.setSeconds(sum);
    }

    return date;
}

// An global instance of SessionSecurity is instanciated as such by the default
// setup (all.html)::
//
//     sessionSecurity = new SessionSecurity();
//     sessionSecurity = $.extend(SessionSecurity, {
//         // define overrides here
//     });
//     sessionSecurity.initialize()
var SessionSecurity = function() {
    // HTML element that should show to warn the user that his session will
    // expire
    this.warningElement = $('#session_security_warning');

    // Callback called when the session expired
    this.expire = function() {
        $.get(this.LOGOUT_URL, function() {
            document.location.href = sessionSecurity.LOGIN_URL + '?next=' + document.location.pathname;
        });
    }

    // Callback that should display the warning
    this.warn = function() {
        this.warningElement.fadeIn();
    }

    // Callback for activity events, mouse move, keyboard move, scroll ...
    // Beware: it is bind as function, which means that 'this' is out of scope,
    // use sessionSecurity global variable instead
    this.activity = function() {
        // Update last activity datetime
        sessionSecurity.lastActivity = new Date();

        // If we're in warning period
        if (sessionSecurity.warningElement.is(':visible')) {
            // Hide the warning to unlock the page
            sessionSecurity.warningElement.hide();
            // Cancel the next programed tick
            clearTimeout(sessionSecurity.timeout);
            // Tick now, to upload last activity time to the server
            sessionSecurity.tick(true);
        }
    }

    this.tick = function(activity) {
        var now = new Date();
        var sinceActivity = activity ? Math.floor((now - sessionSecurity.lastActivity) / 1000) : -1;

        // Given the seconds elapsed since last activity, ask the server how
        // long to wait before another tick
        $.get(
            sessionSecurity.pingUrl, 
            {
                'sinceActivity': sinceActivity,
                'csrfmiddlewaretoken': sessionSecurity.token,
            },
            function(data, textStatus, jqXHR) {
                if (sinceActivity != parseInt(data)) {
                    var sinceActivity = parseInt(data);
                    sessionSecurity.lastActivity = addSeconds(new Date(), sinceActivity * -1);
                }
                console.log('last activity', sessionSecurity.lastActivity)
                console.log('since activity', sinceActivity)

                expireIn = sessionSecurity.EXPIRE_AFTER - sinceActivity;
                warnIn = sessionSecurity.WARN_AFTER - sinceActivity;
                console.log('calculates warn after', warnIn)
                console.log('calculates expire after', expireIn)

                if (expireIn <= 0) {
                    sessionSecurity.expire();
                } else if (warnIn <= 0) {
                    sessionSecurity.warn();
                    var next = expireIn;
                    if (next / 2 != next && next / 2 > 0) {
                        next = next / 2;
                    }
                    if (next < 1) {
                        console.log('force next to 1');
                        next = 1;
                    }
                    sessionSecurity.timeout = setTimeout(sessionSecurity.tick, 
                        next * 1000);
                } else {
                    sessionSecurity.warningElement.hide();
                    sessionSecurity.timeout = setTimeout(sessionSecurity.tick, 
                        warnIn * 1000);
                }
            }
        );
    }

    this.initialize = function() {
        // precalculate WARN_BEFORE
        this.WARN_BEFORE = this.EXPIRE_AFTER - this.WARN_AFTER;
        
        // Initiate this.lastActivity
        this.lastActivity = new Date();

        // try to monitor for activity in the page
        $('*').scroll(this.activity);
        $('*').keyup(this.activity);
        $('*').click(this.activity);

        this.timeout = setTimeout(sessionSecurity.tick, this.WARN_AFTER*1000);
    }
}

