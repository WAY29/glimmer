

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


class LoggerExceptions:
    class Base(Exception):
        pass

    class NotInitError(Base):
        pass
