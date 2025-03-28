from rest_framework.throttling import SimpleRateThrottle

class TenantRateThrottle(SimpleRateThrottle):
    scope = 'tenant'

    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return None 
        return f"throttle_{self.scope}_{request.user.tenant_id}"



