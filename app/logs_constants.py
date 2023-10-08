from enum import Enum


class LogoutsTags(Enum):
    INFO :str = '[i]'
    NOTIFICATIONS :str = '[n]'
    LOG :str = '[L]'
    WARNING :str = '[W]'
    ERROR :str = '[error]'