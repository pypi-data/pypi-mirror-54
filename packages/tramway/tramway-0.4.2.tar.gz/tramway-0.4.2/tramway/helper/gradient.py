# -*- coding: utf-8 -*-

# Copyright © 2019, Institut Pasteur
#   Contributor: François Laurent

# This file is part of the TRamWAy software available at
# "https://github.com/DecBayComp/TRamWAy" and is distributed under
# the terms of the CeCILL license as circulated at the following URL
# "http://www.cecill.info/licenses.en.html".

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.


from tramway.core.lazy import Lazy
from tramway.inference.base import FiniteElements
from importlib import import_module


class SpatialOperator(Lazy):
    '''
    Switch for spatial gradients and differential operators.

    The arguments and command-line options employed before the introduction of this class were
    (and still are):

    * `grad` for spatial gradients
    * `rgrad` for spatial variations used for regularization

    Suitable for serialization if freshly initialized (as long as properties and methods not called).

    '''
    __slots__ = 'metname', 'funcname', 'modname', '_func', '_mod', '_func_is_met', 'manifold'
    __lazy__ = 'func', 'mod', 'func_is_met'
    def __init__(self, metname, keywords=['*', 'default_*'], modules=['tramway.inference.gradient'],
            kwargs={}, **expanded_kwargs):
        Lazy.__init__(self)
        if expanded_kwargs:
            kwargs = dict(kwargs) # copy
            kwargs.update(expanded_kwargs)
        self.metname = metname
        keywords = [ k.replace('*', metname) for k in keywords ]
        modules = [ m.replace('*', metname) for m in modules ]
        self.funcname = None
        for kw in keywords:
            self.funcname = kwargs.get(kw, None)
            if self.funcname is not None:
                break
        self._func = self._func_is_met = self._mod = self.modname = None
        if self.funcname is not None:
            for modname in modules:
                mod = import_module(modname)
                try:
                    self._func = getattr(mod, self.funcname)
                except AttributeError:
                    pass
                else:
                    self._mod = mod
                    self.modname = modname
                    self._func_is_met = False
                    break
        self.manifold = None
    @property
    def func(self):
        if self._func is None and self.funcname is not None:
            self._func = getattr(self.mod, self.funcname)
            self._func_is_met = False
        return self._func
    @property
    def mod(self):
        if self._mod is None:
            self._mod = import_module(self.modname)
        return self._mod
    @property
    def func_is_met(self):
        return self._func_is_met
    def callable(self, *args, **kwargs):
        if self.manifold is None:
            raise AttributeError('`manifold` has not been set')
        if self.func is None:
            self._func = getattr(self.manifold, self.metname)
            self._func_is_met = True
        if self.func_is_met:
            return self.func(*args, **kwargs)
        else:
            return self.func(self.manifold, *args, **kwargs)
    def __getattr__(self, attr):
        if attr == self.metname:
            return self.func
        else:
            return __getattr__(Lazy, self, attr)


def overload_finite_elements_cls(setup, grad=None, rgrad=None, finite_elements_cls=None, cls_grad=None, cls_rgrad=None):
    '''
    Determines the implementation for :met:`~tramway.inference.base.FiniteElements.grad` and
    :met:`~tramway.inference.base.FiniteElements.local_variation`/:met:`~tramway.inference.base.FiniteElements.rgrad`.

    Arguments:

        setup (dict): inference mode setup.

        grad (str): implementation for :met:`~tramway.inference.base.FiniteElements.grad`;
            any of: 'grad1', 'gradn', 'delta0', 'delta1' or any other symbol from module
            :mod:`~tramway.inference.gradient`.

        rgrad (str): implementation for :met:`~tramway.inference.base.FiniteElements.local_variation`/:met:`~tramway.inference.base.FiniteElements.rgrad`;
            same values as for argument `grad`.

        finite_elements_cls (type): class for distributed domains; should be subclass of
            :class:`~tramway.inference.base.FiniteElements`.

        cls_grad (callable): actual :met:`~tramway.inference.base.FiniteElements.grad` implementation
            in the `manifold_cls` class if this implementation is straighforwardly delegated to
            any implementation exported by module :mod:`~tramway.inference.gradient`.

        cls_rgrad (callable): actual :met:`~tramway.inference.base.FiniteElements.rgrad` implementation;
            see also `cls_grad`.

    Returns:

        type: overloaded finite elements class; subclass of `finite_elements_cls`.

    '''
    grad = SpatialOperator('grad', grad=grad, kwargs=setup)
    rgrad = SpatialOperator('rgrad', rgrad=rgrad, kwargs=setup)
    if finite_elements_cls in (None, FiniteElements):
        import tramway.inference.gradient.grad as gradient
        if cls_grad is None:
            cls_grad = gradient.grad1
        if cls_rgrad is None:
            cls_rgrad = gradient.grad1
    grad = None if grad.func is cls_grad else grad.func
    rgrad = None if rgrad.func is cls_rgrad else rgrad.func
    #ops = {}
    #if grad.func is not cls_grad:
    #    ops[grad.metname] = grad.func
    #if rgrad.func is not cls_rgrad:
    #    ops[rgrad.metname] = rgrad.func
    #return ops
    if grad is None and rgrad is None:
        return finite_elements_cls
    else:
        if finite_elements_cls is None:
            finite_elements_cls = FiniteElements
        if grad is None:
            class FiniteElementsCls(finite_elements_cls):
                #def local_variation(self, *args, **kwargs):
                def rgrad(self, *args, **kwargs):
                    return rgrad(self, *args, **kwargs)
        elif rgrad is None:
            class FiniteElementsCls(finite_elements_cls):
                def grad(self, *args, **kwargs):
                    return grad(self, *args, **kwargs)
        else:
            class FiniteElementsCls(finite_elements_cls):
                def grad(self, *args, **kwargs):
                    return grad(self, *args, **kwargs)
                #def local_variation(self, *args, **kwargs):
                def rgrad(self, *args, **kwargs):
                    return rgrad(self, *args, **kwargs)
        return FiniteElementsCls

