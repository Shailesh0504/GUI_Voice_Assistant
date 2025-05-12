# core/registry.py

# Dictionary that holds command_key -> function mappings
command_registry = {}

def register_command(command_key):
    """
    Decorator to register a function as a command handler.

    Usage:
        @register_command("set alarm")
        def alarm_handler(params):
            ...
    """
    def decorator(func):
        command_registry[command_key] = func
        return func
    return decorator

def get_command_registry():
    return command_registry

