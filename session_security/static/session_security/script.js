var SessionSecurity = function() {
    // Show the dialog and create a timeout for ping() after WARN_BEFORE.
    // Because this warning should happen WARN_BEFORE seconds before actual
    // expiry.
    this.warn = function() {
        this.dialog.show();
        this.timeout = setTimeout(this.ping, this.WARN_BEFORE * 1000)
    }

    // Redirect to LOGOUT_URL?next=/current/url/
    this.expire = function() {
        document.location.href = this.LOGOUT_URL + '?next=' + document.location.href;
    }

    // Element that contains the modal dialog, which should contain a question
    // like 'Do you want to extend your session ?' and provide an element of
    // class 'yes' and another of class 'no'.
    this.dialog = $('#session_security_warning');

    this.initialize = function() {
        // When the user clicks 'Yes':
        // - hide the dialog that this.warn() has displayed, 
        // - remove the timeout that this.warn() has setup, 
        // - POST to ExtendSessionView,
        // - on POST success, set this.ping to run again later.
        this.dialog.find('.yes').click(function() {
            sessionSecurity.dialog.hide();
            clearTimeout(sessionSecurity.timeout);

            $.post(sessionSecurity.extendUrl, function(data, textStatus, jqXHR) {
                sessionSecurity.timeout = setTimeout(sessionSecurity.ping, 
                    (sessionSecurity.EXPIRE_AFTER - sessionSecurity.WARN_BEFORE) * 1000);
            });
        });
        
        // When the user clicks 'No', hide the dialog that this.warn() has displayed().
        this.dialog.find('.no').click(function() {
            sessionSecurity.dialog.hide();
        });

        // POST to PingView, which may return 3 kind of values:
        // - call expire() if 'expire' string was responded,
        // - call warn() if 'warn' string was responded,
        // - hide the dialog and set a timeout for ping after the number of
        //   responded seconds.
        this.ping = function() {
            $.post(sessionSecurity.pingUrl, function(data) {
                if (data == 'expire') {
                    sessionSecurity.expire();
                } else if (data == 'warn') {
                    sessionSecurity.warn();
                } else {
                    sessionSecurity.dialog.hide();
                    sessionSecurity.timeout = setTimeout(sessionSecurity.ping, 
                        parseInt(data) * 1000)
                }
            });
        }

        // At the end of SessionSecurity constructor, set ping() to run when
        // the user is supposed to be warned that his session will expire.
        this.timeout = setTimeout(this.ping, 
            (this.EXPIRE_AFTER - this.WARN_BEFORE) * 1000);
    }
}

