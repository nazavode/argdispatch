# -*- coding: utf-8 -*-
#
# Copyright 2015 Federico Ficarelli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import inspect

import pytest

from argdispatch import argdispatch

###############################################################################
# Test functions

DISPATCHED = 'DISPATCHED'


def fun_1(a=0, b=1, c=2, d=3, e=4, f=5, g=6):
    return {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g}


def fun_2(a=0, b=1, c=2, d=3, e=4, f=5, g=6):
    return {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g}


def fun_3(a=0, b=1, c=2, d=3, e=4, f=5, g=6):
    return {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g}

###############################################################################
# Fixtures

functions = (
    fun_1,
    fun_2,
    fun_3,
)


@pytest.fixture(
    params=[
        (fun, arg) for fun in functions for arg in inspect.signature(fun).parameters.keys()
    ]
)
def funarg(request):
    return request.param


###############################################################################
# Tests


def test_trivial(funarg):
    function = funarg[0]
    argument = funarg[1]
    dsp_function = argdispatch(argument)(function)
    reg_function = dsp_function.register(DISPATCHED.__class__)(function)
    kwargs = {argument: DISPATCHED}
    res = reg_function(**kwargs)
    for arg, value in res.items():
        if arg == argument:
            assert value == DISPATCHED
        else:
            assert value != DISPATCHED


def test_boundmethod():
    pass


def test_abc():
    pass


def test_argdispatch():

    @argdispatch('b')
    def foo(a, b, c):
        pass

    @foo.register(int)
    def foo_int(a, b, c):
        pass

    class BaseVisitor(metaclass=abc.ABCMeta):
        @abc.abstractmethod
        def visit(self, obj):
            pass

    class TestVisitor(BaseVisitor):
        @argdispatch('obj')
        def visit(self, obj):
            """VISIT DOC"""
            print('METH object')

        @visit.register(str)
        def _(self, obj):
            print('METH str')

        @visit.register(float)
        def _(self, obj):
            print('METH float')

        @visit.register(int)
        def _(self, obj):
            print('METH int')


    test = TestVisitor()

    test.visit(1)
    test.visit(1.0)
    test.visit("CIAO")

