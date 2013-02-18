// Use 'yourlabs' as namespace.
if (window.yourlabs == undefined) window.yourlabs = {};

// Session security constructor. These are the required options:
//
// - pingUrl: url to ping with last activity in this tab to get global last
//   activity time,
// - warnAfter: number of seconds of inactivity before warning,
// - expireAfter: number of seconds of inactivity before expiring the session.
yourlabs.SessionSecurity = function(options) {
    // **HTML element** that should show to warn the user that his session will
    // expire.
    this.$warning = $('#session_security_warning');

    // Last recorded activity datetime.
    this.lastActivity = new Date();
   
    // Merge the options dict here.
    $.extend(this, options);

    // Bind common activity events to update this.lastActivity.
    $(document)
        .scroll($.proxy(this.activity, this))
        .keyup($.proxy(this.activity, this))
        .mousemove($.proxy(this.activity, this))
        .click($.proxy(this.activity, this))
   
    // Initialize timers.
    this.apply()
}

yourlabs.SessionSecurity.prototype = {
    // Called when there has been no activity for more than expireAfter
    // seconds.
    expire: function() {
        window.location.reload()
    },
    
    // Called when there has been no activity for more than warnAfter
    // seconds.
    showWarning: function() {
        this.$warning.fadeIn('slow');
    },
    
    // Called to hide the warning, for example if there has been activity on
    // the server side - in another browser tab.
    hideWarning: function() {
        this.$warning.hide();
    },

    // Called by click, scroll, mousemove, keyup.
    activity: function() {
        this.lastActivity = new Date();

        if (this.$warning.is(':visible')) {
            // Inform the server that the user came back manually, this should
            // block other browser tabs from expiring.
            this.ping();
        }

        this.hideWarning();
    },

    // Hit the PingView with the number of seconds since last activity.
    ping: function() {
        var idleFor = Math.floor((new Date() - this.lastActivity) / 1000);

        $.ajax(this.pingUrl, {
            data: {idleFor: idleFor},
            cache: false,
            success: $.proxy(this.pong, this),
            // In case of network error, we still want to hide potentially
            // confidential data !!
            error: $.proxy(this.apply, this),
            dataType: 'json',
            type: 'post',
        });
    },

    // Callback to process PingView response.
    pong: function(data) {
        if (data == 'logout') return this.expire();

        this.lastActivity = new Date();
        this.lastActivity.setSeconds(this.lastActivity.getSeconds() - data);
        this.apply();
    },

    // Apply warning or expiry, setup next ping
    apply: function() {
        // Cancel timeout if any, since we're going to make our own
        clearTimeout(this.timeout);

        var idleFor = Math.floor((new Date() - this.lastActivity) / 1000);

        if (idleFor >= this.expireAfter) {
            this.lastChance = !this.lastChance;
            return this.lastChance ? this.ping() : this.expire();
        } else if (idleFor >= this.warnAfter) {
            this.showWarning();
            nextPing = this.expireAfter - idleFor;
        } else {
            this.hideWarning();
            nextPing = this.warnAfter - idleFor;
        }

        this.timeout = setTimeout($.proxy(this.ping, this), nextPing * 1000);
    }
}
