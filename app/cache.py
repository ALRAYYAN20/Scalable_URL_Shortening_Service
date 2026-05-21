# import redis 

# redis_client = redis.Redis( host = 'localhost',
#                             port = 6379,
#                             db = 0,
#                             decode_responses = True
#                          )

# refactoring to upstash redis 

from upstash_redis import Redis
from dotenv import load_dotenv 
import os

redis_client = Redis(
    url = os.getenv("UPSTASH_REDIS_REST_URL"),
    token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    )