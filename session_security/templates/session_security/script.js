{% if request.user.is_authenticated %}
    var session_expiry_seconds = {{ request.session.session_expiry_seconds }};
    setTimeout(function() {
        alert('You session is about to expire !');
    }, session_expiry_seconds*1000-10*1000);
    setTimeout(function() {
        alert('Session expired');
    }, session_expiry_seconds*1000);
{% endif %}

