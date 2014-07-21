#
# HamperSingleton is a metaclass to add the Singleton paradigm to a Python class.
#

class HamperSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        
        if cls not in cls._instances:
            cls._instances[cls] = super(HamperSingleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
