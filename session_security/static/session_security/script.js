// Use 'yourlabs' as namespace.
if (window.yourlabs == undefined) window.yourlabs = {};

// Session security class.
yourlabs.SessionSecurity = function(pingUrl) {
    // Url to PingView.
    this.pingUrl = pingUrl;

    // **HTML element** that should show to warn the user that his session will
    // expire.
    this.$warning = $('#session_security_warning');

    // **HTML element** that should replace <body> contents when the session
    // has expired, hiding potentially sensible data from HTML source code.
    this.$expired = $('#session_security_expired');

    // A hack to anticipate clock skews. If the next event (warn or expire) is
    // in 13 seconds and that timeRatio is 1.3, then it will hit PingView after
    // 10 seconds (10/1.3). Adjust to your needs when you are asked to fine-tune.
    this.timeRatio = 1.3;

    // Last recorded activity datetime.
    this.lastActivity = new Date();

    // Bind common activity events to update this.lastActivity.
    $(document)
        .scroll($.proxy(this.activity, this))
        .keyup($.proxy(this.activity, this))
        .mousemove($.proxy(this.activity, this))
        .click($.proxy(this.activity, this))

    // Ping to get the next event type and in how many seconds.
    this.ping();
}

yourlabs.SessionSecurity.prototype = {
    // Called when PingView responds with ['expire', <something lower than 0>].
    expire: function() {
        $('body').html(this.$expired);
        this.expired = true;
    },
    
    // Called when PingView responds with 
    // ['expire', <something higher than 0>].
    showWarning: function() {
        this.$warning.fadeIn('slow');
    },
    
    // Called when PingView responds with ['warn', ...]
    hideWarning: function() {
        this.$warning.hide();
    },

    // Called by click, scroll, mousemove, keyup.
    activity: function() {
        this.hideWarning();
        this.lastActivity = new Date();
    },

    // Hit the PingView with the number of seconds since last activity.
    ping: function() {
        var inactiveSince = Math.floor((new Date() - this.lastActivity)
            / 1000);

        $.post(this.pingUrl, {inactiveSince: inactiveSince},
           $.proxy(this.pong, this), 'json');
    },

    // Callback to process PingView response.
    pong: function(data) {
        if (this.expired) return;

        this.action = data[0];
        this.time = data[1];        

        if (this.action == 'expire') {
            this.time <= 0 ? this.expire() : this.showWarning();
        } else {
            this.hideWarning();
        }
        this.timeout = setTimeout($.proxy(this.ping, this), 
            (this.time / this.timeRatio) * 1000);
    },
}
