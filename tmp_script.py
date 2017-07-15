#! /usr/bin/python

#============================================================================#
# test setting class attributes after inheritance
#============================================================================#
# class A(object): pass
# class B(A): pass

# A.FOO = 'BAR'
# print B.FOO

#============================================================================#
# test property vs attribute access speed
#============================================================================#
# import timeit
# result = timeit.timeit("""
# for n in xrange(1000):
#     foo.myattr
# """,
# setup="""
# class Foo(object):
#     @property
#     def myattr(self):
#         return 1
# foo = Foo()
# """,
# number=10000)
# print 'property result:', result


# result = timeit.timeit("""
# for n in xrange(1000):
#     foo.myattr()
# """,
# setup="""
# class Foo(object):
#     def myattr(self):
#         return 1
# foo = Foo()
# """,
# number=10000)
# print 'function result:', result


# result = timeit.timeit("""
# for n in xrange(1000):
#     foo.myattr
# """,
# setup="""
# class Foo(object):
#     def __init__(self):
#         self.myattr = 1
# foo = Foo()
# """,
# number=10000)
# print 'attribute result:', result


# result = timeit.timeit("""
# for n in xrange(1000):
#     foo.myattr
# """,
# setup="""
# class Foo(object):
#     myattr = 1
# foo = Foo()
# """,
# number=10000)
# print 'class attribute result:', result

#============================================================================#
# test class boolean checking
#============================================================================#
# class Foo(object):
#     def __nonzero__(self):
#         print '__nonzero__'
#         return False

# foo = Foo()
# if foo:
#     print 'Passed if statement'
# else:
#     print 'Failed if statement'

# print 'bool:', bool(foo)

#============================================================================#
# test multiple inheritance
#============================================================================#
# class BaseA(object):
#     def foo(self):
#         print 'BaseA'

# class BaseB(BaseA):
#     def foo(self):
#         print 'BaseB'
#         super(BaseB, self).foo()

# class ChildA(BaseA):
#     def foo(self):
#         print 'ChildA'
#         super(ChildA, self).foo()

# class ChildB(ChildA, BaseB):
#     def foo(self):
#         print 'ChildB'
#         super(ChildB, self).foo()


# a=ChildB()
# a.foo()

# # ChildB
# # BaseB
# # ChildA
# # BaseA


