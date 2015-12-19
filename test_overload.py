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

from overload import overload

if __name__ == '__main__':
    import abc

    @overload('b')
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
        @overload('obj')
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

    print(test.visit.__doc__)
