from time import sleep
from typing import Callable


def retry(
    f: Callable,
    retry_time: int = 3,
    errors: tuple = (Exception,),
    sleep_second: int = 1,
):
    '''Retries a function a specified number of times if it fails.

    Args:
        f (Callable): The function to be retried.
        retry_times (int, optional): The number of times to retry the function. Defaults to 3.
    '''

    while retry_time:
        try:
            return f()
        except errors as e:
            retry_time -= 1
            print(f'>>>>>>>> {retry_time=}')
            if not retry_time and e:
                raise

        sleep(sleep_second)
