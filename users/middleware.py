# from django.utils.timezone import now
from datetime import datetime, timezone
from users import models as uMod

class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            today = datetime.now(timezone.utc)
            if request.user.last_active is None:
                #workaround for profiles not having last_active set
                try:
                    request.user.last_active = today
                    request.user.save()
                except:
                    pass

            elif request.user.last_active < today:
                # update last_active
                request.user.last_active = today
                request.user.save()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

