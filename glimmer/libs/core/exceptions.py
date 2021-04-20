

class ModuleLoadExceptions:
    class Base(Exception):
        pass

    class FileNotFound(Base):
        pass

    class ModuleCompileError(Base):
        pass

    class VerifyError(Base):
        pass


class ParserExceptions:
    class Base(Exception):
        pass

    class CyberSpace(Base):
        class Base(Exception):
            pass

        class APIKeyError(Base):
            pass

        class APIError(Base):
            pass

        class HTTPError(Base):
            pass

        class ArgumentError(Base):
            pass


class LoggerExceptions:
    class Base(Exception):
        pass

    class NotInitError(Base):
        pass
