import time


def rate_limit(max_calls: int, period: int):
    def decorator(func):
        func_calls = []

        def wrapper(*args, **kwargs):
            now = time.time()

            if args and hasattr(args[0], "__dict__"):
                instance = args[0]
                
                if not hasattr(instance, "_rate_limit_store"):
                    instance._rate_limit_store = {}
                
                history = instance._rate_limit_store.setdefault(func.__name__, [])
                history = [t for t in history if now - t < period]
                
                if len(history) >= max_calls:
                    raise Exception(f"Rate limit exceeded for method '{func.__name__}'")
                
                history.append(now)
                instance._rate_limit_store[func.__name__] = history

            else:
                nonlocal func_calls
                func_calls = [t for t in func_calls if now - t < period]

                if len(func_calls) >= max_calls:
                    raise Exception(f"Rate limit exceeded for function '{func.__name__}'")

                func_calls.append(now)

            return func(*args, **kwargs)

        return wrapper
    return decorator


class EventDispatcher:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type: str, callback: callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: callable):
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def dispatch(self, event_type: str, *args, **kwargs):
        if event_type in self._listeners:
            for callback in list(self._listeners[event_type]):
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Error in callback '{callback.__name__}' during event '{event_type}': {e}")


class Typed:
    def __init__(self, expected_type: type):
        self.expected_type = expected_type
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type.__name__}, got {type(value).__name__}")
        
        setattr(instance, self.storage_name, value)


def product_of_multiples(factor: int, limit: int) -> int:
    product = 1
    found_multiple = False

    for multiple in range(factor, limit, factor):
        product *= multiple
        found_multiple = True

    return product if found_multiple else 0


"""
==============================================================================
QUESTION 1 EXPLANATION ANSWERS
==============================================================================

IDENTIFY BUG 1: UnboundLocalError Explanation
----------------------------------------------
Python uses static scoping rules for local variables inside functions. When Python 
compiles the 'wrapper' function, it sees the assignment statement:
    `calls = [t for t in calls if now - t < period]`

Because 'calls' appears on the left side of an assignment inside 'wrapper', Python 
flags 'calls' as a LOCAL variable for that entire scope. 

During runtime, when Python evaluates the right-hand side (`[t for t in calls ...]`), 
it looks for the local variable 'calls'. However, because it has not been assigned 
a local value yet at that line, Python raises an `UnboundLocalError`.

IDENTIFY BUG 2: State Tracking Across Class Method Instances
------------------------------------------------------------
In the original implementation, the `calls` list lives in the closure of the 
decorator function. When decorating a class method, EVERY instance of that class 
shares the SAME single `calls` list in memory. 

If Instance A makes 3 calls and hits the rate limit, Instance B will also be blocked 
from making calls—even if Instance B has made zero calls itself.

State tracking must be tied to the instance (`self`, which is `args[0]`). 
By storing a dictionary of histories on `self` (e.g., `self._rate_limit_store`), 
each object maintains its own independent rate limit window.
"""


if __name__ == "__main__":
    @rate_limit(max_calls=2, period=2)
    def standalone_demo(user_id):
        return f"Data retrieved for {user_id}"

    class UserAPI:
        @rate_limit(max_calls=2, period=2)
        def fetch(self, user_id):
            return f"User API Data for {user_id}"

    class Person:
        name = Typed(str)
        age = Typed(int)

        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    print(standalone_demo("User_101"))
    print(standalone_demo("User_102"))

    user_a = UserAPI()
    user_b = UserAPI()
    print(user_a.fetch("A"))
    print(user_a.fetch("A"))
    print(user_b.fetch("B"))

    dispatcher = EventDispatcher()

    def listener_one(msg):
        print(f"Listener 1: {msg}")

    def listener_failing(msg):
        raise ValueError("Error triggered")

    def listener_two(msg):
        print(f"Listener 2: {msg}")

    dispatcher.subscribe("test_event", listener_one)
    dispatcher.subscribe("test_event", listener_failing)
    dispatcher.subscribe("test_event", listener_two)
    dispatcher.dispatch("test_event", msg="Execution Test")

    p = Person("Alice", 25)
    print(f"Person: {p.name}, {p.age}")

    print(f"Product of multiples: {product_of_multiples(3, 10)}")battery_info())
