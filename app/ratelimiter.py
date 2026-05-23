from fastapi import HTTPException, Request
from upstash_ratelimit import Ratelimit, FixedWindow
from .cache import redis_client

# ip based limiter
ip_limiter = Ratelimit( redis = redis_client,
                        limiter = FixedWindow (max_requests = 10, window = 60)
                        ) # 60 secs

# user based limiter
user_limiter = Ratelimit( redis = redis_client,
                        limiter = FixedWindow (max_requests = 20, window = 60)
                        ) # 60 secs


def check_ip_rate_limit( request: Request):
    identifier = request.client.host

    response = ip_limiter.limit(identifier)

    if not response.allowed:
        raise HTTPException ( status_code = 429, detail = " Too many requests from this IP, Try again later.")
    

def check_user_rate_limit( user_id : int):
    identifier = f"user_{user_id}"

    response = user_limiter.limit(identifier)

    if not response.allowed:
        raise HTTPException ( status_code = 429, detail = " Rate limit exceeded for this user, Try again later.")
    