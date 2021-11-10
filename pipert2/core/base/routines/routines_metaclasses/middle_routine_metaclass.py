class MiddleRoutineMetaclass(type):
    def __new__(cls, clsname, bases, attrs, check_main_logics_structure=True):
        if check_main_logics_structure:
            pass

        return super(MiddleRoutineMetaclass, cls).__new__(cls, clsname, bases, attrs)
