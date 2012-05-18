function addSeconds(date, seconds) {
    var sum = date.getSeconds() + seconds;

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

var SessionSecurity = function() {
    // HTML element that should show to warn the user that his session will expire
    this.warningElement = $('#session_security_warning');

    // Callback that should display the user with a login prompt
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
    this.activity = function() {
        if (sessionSecurity.warningElement.is(':visible')) {
            console.log('activity forces tick');
            sessionSecurity.warningElement.hide();
            clearTimeout(sessionSecurity.timeout);
            sessionSecurity.tick();
        }
        sessionSecurity.lastActivity = new Date();
    }

    // Timed callback
    this.tick = function() {
        var now = new Date();
        var sinceActivity = Math.floor((now - sessionSecurity.lastActivity) / 1000)

        // Given the seconds elapsed since last activity, ask the server how
        // long to wait before another tick
        $.post(
            sessionSecurity.pingUrl, 
            {
                'sinceActivity': sinceActivity
            },
            function(data, textStatus, jqXHR) {
                var sinceActivity = parseInt(data);
                sessionSecurity.lastActivity = addSeconds(new Date(), sinceActivity * -1);
                console.log(sessionSecurity.lastActivity)

                expireIn = sessionSecurity.EXPIRE_AFTER - sinceActivity;
                warnIn = sessionSecurity.WARN_AFTER - sinceActivity;

                console.log(sinceActivity, expireIn, warnIn)

                if (expireIn <= 0) {
                    sessionSecurity.expire();
                } else if (warnIn <= 0) {
                    sessionSecurity.warn();
                    sessionSecurity.timeout = setTimeout(sessionSecurity.tick, 
                        expireIn * 1000);
                } else {
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

