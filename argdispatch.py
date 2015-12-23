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

"""
Improved single dispatch decorator with custom dispatch argument.
"""

import functools
import inspect


__author__ = 'Federico Ficarelli'
__copyright__ = 'Copyright (c) 2015 Federico Ficarelli'
__license__ = 'Apache License Version 2.0'
__version__ = '0.1.0'


def overload(argument=None):
    """

    :param argument:
    :return:
    """
    # Define dispatch argument:
    dispatch_arg_name = argument

    def dispatch_decorator(func):
        """Dispatch closure decorator."""
        # Apply std decorator:
        dispatcher = functools.singledispatch(func)
        # Cache wrapped signature:
        wrapped_signature = inspect.signature(func)
        # Check argument correctness
        if dispatch_arg_name is not None and dispatch_arg_name not in wrapped_signature.parameters:
            raise ValueError('unknown dispatch argument specified')

        def wrapper(*args, **kwargs):
            """Dispatch function wrapper."""
            if dispatch_arg_name is None:
                discriminator = args[0].__class__  # mimic functools.singledispatch behaviour
            else:
                bound_args = wrapped_signature.bind(*args, **kwargs).arguments
                if dispatch_arg_name not in bound_args:
                    # ...with the new register this should be dead code.
                    raise TypeError('registered method mismatch')
                discriminator = bound_args[dispatch_arg_name].__class__
            return dispatcher.dispatch(discriminator)(*args, **kwargs)

        def register(cls, reg_func=None):
            """ Registration method replacement.

            Ensures that situations like the following never happen:

                >>> @overload('c')
                >>> def test(a, obj, b=None, c=None):
                >>>    pass
                >>>
                >>> @test.register(int)
                >>> def _(a, obj):
                >>>    pass
                >>>
                >>> test(1, 2) # ----> TypeError

            """
            if reg_func is not None:
                # Check signature match:
                reg_sig = inspect.signature(reg_func)
                if reg_sig != wrapped_signature:
                    raise TypeError('registered method signature mismatch')
            return dispatcher.register(cls, reg_func)

        wrapper.register = register
        functools.update_wrapper(wrapper, func)
        return wrapper

    return dispatch_decorator
