from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BurstRateThrottle(AnonRateThrottle):
    scope = 'burst'
    
class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'