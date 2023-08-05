import sklearn


def _is_version(version_check):
    if sklearn.__version__.startswith(version_check):
        return True
    return False


def sklearn_is_0_19():
    return _is_version("0.19.")


def sklearn_is_0_20():
    return _is_version("0.20.")


def sklearn_is_0_21():
    return _is_version("0.21.")


def get_refactored_tests_to_skip():
    """These tests have been edited in order to work with spark.
    They have been moved into this repo e.g. in resource_warning_tests.py"""
    if sklearn_is_0_19():
        return [
            "test_return_train_score_warn",  # moved to resource_warning_tests.py
        ]
    elif sklearn_is_0_20():
        return [
            "test_return_train_score_warn",  # moved to resource_warning_tests.py
            "test_deprecated_grid_search_iid",  # moved to resource_warning_tests.py
            "test_validate_parameter_grid_input"  # a function, not a test
        ]
    elif sklearn_is_0_21():
        return [
            "test_refit_callable_out_bound",  # parameterized test, moved to test_parameterised_tests
            "test_deprecated_grid_search_iid",  # moved to resource_warning_tests.py
            "test_validate_parameter_grid_input",  # parameterized test, moved to test_parameterised_tests
        ]
    else:
        raise NotImplementedError(
            "Unsupported sklearn version {}".format(sklearn.__version__))
