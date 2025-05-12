import time

from fastapi import Depends, HTTPException, Request

from pixelgram.auth import current_active_user
from pixelgram.schemas import schemas

# Memory to store users temporarily to control rate limiting

rate_limit_memory = {}

RATE_LIMIT = 1  # requests per second
RATE_LIMIT_WINDOW = 60  # seconds


async def rate_limiter(
    request: Request, user: schemas.UserRead = Depends(current_active_user)
):
    """
    Rate limiting dependency to limit the number of requests per user
    """

    user_id = str(user.id)
    current_time = time.time()

    # Check if the user is in the rate limit memory
    if user_id in rate_limit_memory:
        last_request_time = rate_limit_memory[user_id]
        time_since_last_request = current_time - last_request_time

        # If the time since the last request is less than the rate limit window,
        # check if the user has exceeded the rate limit
        if time_since_last_request < RATE_LIMIT_WINDOW:
            if rate_limit_memory[user_id]["request_count"] >= RATE_LIMIT:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later.",
                )
            else:
                rate_limit_memory[user_id]["request_count"] += 1
        else:
            # Reset the request count and update the last request time
            rate_limit_memory[user_id] = {
                "last_request_time": current_time,
                "request_count": 1,
            }
    else:
        # Add the user to the rate limit memory
        rate_limit_memory[user_id] = {
            "last_request_time": current_time,
            "request_count": 1,
        }
