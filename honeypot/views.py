from django.http import HttpResponse
from django.shortcuts import render
from smartshuk.settings import DEBUG
import logging
from django.http import JsonResponse

logger = logging.getLogger('honeypot')

def honeypot_view(request):
    # If in DEBUG mode, log additional information for debugging purposes
    if DEBUG:
        logger.debug("Debug mode - Honeypot accessed")
    
    # AJAX requests
    if request.method == "GET" and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        logger.warning(f"HONEYPOT-ACCESS: IP: {request.META.get('REMOTE_ADDR')}, User Agent: {request.META.get('HTTP_USER_AGENT')}")
        logger.info(f"    User: {request.user if request.user.is_authenticated else 'AnonymousUser'}")
        logger.info(f"    AJAX honeypot triggered")
        return JsonResponse({"status": "success", "message": "Thank you for your feedback!"})
    
    # fors with GET method
    elif request.method == "GET":
        logger.warning(f"HONEYPOT-ACCESS: IP: {request.META.get('REMOTE_ADDR')}, User Agent: {request.META.get('HTTP_USER_AGENT')}")
        logger.info(f"    User: {request.user if request.user.is_authenticated else 'AnonymousUser'}")
        logger.info(f"    GET honeypot triggered")
    
    # POST requests
    elif request.method == "POST":
        logger.warning(f"HONEYPOT-ACCESS: IP: {request.META.get('REMOTE_ADDR')}, User Agent: {request.META.get('HTTP_USER_AGENT')}")
        logger.info(f"    User: {request.user if request.user.is_authenticated else 'AnonymousUser'}")
        logger.info(f"    POST honeypot triggered")
    
    # Other requests
    else:
        logger.warning(f"HONEYPOT-ACCESS: IP: {request.META.get('REMOTE_ADDR')}, User Agent: {request.META.get('HTTP_USER_AGENT')}")
        logger.info(f"    User: {request.user if request.user.is_authenticated else 'AnonymousUser'}")
        logger.info(f"    honeypot triggered")
    
    return HttpResponse("Not Found", status=404)

#Fail2Ban Configuration:


'''

Filter Configuration:
Create a filter for Fail2Ban that will match the log entry created by the honeypot access.
Save it - /etc/fail2ban/filter.d/honeypot-smartshuk.conf:

[Definition]
failregex = ^<HOST>.*HONEYPOT-ACCESS: IP:.*$
ignoreregex =



Jail Configuration:
In your /etc/fail2ban/jail.local or /etc/fail2ban/jail.d/custom.conf, add:

[honeypot-jail]
enabled  = true
port     = http,https
filter   = honeypot-smartshuk
#logpath  = /var/log/nginx/access.log
logpath  = /path/to/your/django/project/honeypot/honeypot.log
maxretry = 1
findtime = 3600
bantime  = 86400
action   = iptables-multiport[name=NoNginx, port="http,https", protocol=tcp]



Restart Fail2Ban:

sudo service fail2ban restart
'''