ENVIRONMENT_PRODUCTION = 'production'
ENVIRONMENT_SANDBOX = 'sandbox'
ENVIRONMENT_STAGE = 'stage'
ENVIRONMENT_DEVELOPMENT = 'development'


class InvalidEnvironmentError(Exception):
    """Raised when the given environment name is wrong or the environment is not supported"""
    pass


def validate_environment(environment):
    if environment not in [
        ENVIRONMENT_PRODUCTION,
        ENVIRONMENT_SANDBOX,
        ENVIRONMENT_STAGE,
        ENVIRONMENT_DEVELOPMENT
    ]:
        raise InvalidEnvironmentError()
