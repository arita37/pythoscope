from pythoscope.side_effect import ListAppend, ListExtend, ListInsert

from assertions import *
from inspector_assertions import *
from inspector_helper import *


def function_doing_to_list(action, *args):
    def fun():
        def foo(x):
            getattr(x, action)(*args)
        foo([])
    return fun

def assert_builtin_method_side_effects(se, klass, obj, *args):
    assert isinstance(se, klass)
    assert_serialized(obj, se.obj)
    assert_collection_of_serialized(list(args), list(se.args))

class TestMutation:
    def test_handles_list_append(self):
        fun = function_doing_to_list('append', 1)
        call = inspect_returning_single_call(fun)
        se = assert_one_element_and_return(call.side_effects)
        assert_builtin_method_side_effects(se, ListAppend, [], 1)

    def test_handles_list_extend(self):
        fun = function_doing_to_list('extend', [2])
        call = inspect_returning_single_call(fun)
        se = assert_one_element_and_return(call.side_effects)
        assert_builtin_method_side_effects(se, ListExtend, [], [2])

    def test_handles_list_insert(self):
        fun = function_doing_to_list('insert', 0, 3)
        call = inspect_returning_single_call(fun)
        se = assert_one_element_and_return(call.side_effects)
        assert_builtin_method_side_effects(se, ListInsert, [], 0, 3)
