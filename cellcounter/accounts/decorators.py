from functools import wraps

from ratelimit.exceptions import Ratelimited
from ratelimit.helpers import is_ratelimited


def registration_ratelimit(ip=True, block=False, method=['POST'], field=None, rate='1/h',
                           skip_if=None, keys=None):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kw):
            request.limited = getattr(request, 'limited', False)
            if skip_if is None or not skip_if(request):
                ratelimited = is_ratelimited(request=request, increment=False,
                                             ip=ip, method=method, field=field,
                                             rate=rate, keys=keys)
                if ratelimited and block:
                    raise Ratelimited()
            return_val, success = fn(request, *args, **kw)
            if success:
                is_ratelimited(request=request, increment=True, ip=ip,
                               method=method, field=field, rate=rate, keys=keys)
            return return_val
        return _wrapped
    return decorator