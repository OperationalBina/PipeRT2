class MainLogicValidation(type):
    routines_main_logics_registry_getter = None
    VALIDATE_MAIN_LOGIC_ATTRIBUTE_NAME = "validate_main_logic"

    def __new__(mcs, clsname, bases, attrs, routines_registry=False, validate_main_logics_function=None): # check main logics, (checking config, param type - return type)
        if routines_registry:
            MainLogicValidation.routines_main_logics_registry_getter = routines_registry.all
        if callable(validate_main_logics_function):
            attrs[mcs.VALIDATE_MAIN_LOGIC_ATTRIBUTE_NAME] = validate_main_logics_function
        if validate_main_logics_function is None:
            assert len(bases) > 0  # Should never fail
            validation_function = getattr(bases[0], mcs.VALIDATE_MAIN_LOGIC_ATTRIBUTE_NAME)

            for expected_input_type, main_logics in mcs.routines_main_logics_registry_getter(clsname).items():
                for main_logic in main_logics:
                    validation_function(main_logic, expected_input_type)

        return super(MainLogicValidation, mcs).__new__(
            mcs, clsname, bases, attrs)
