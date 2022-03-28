# -*- coding: utf-8 -*-
"""
Various minimization/optimization algorithms.
"""
import ananimlib as al

import numpy     as np
from scipy.stats import norm


class Search(object):
        """Base class for Search objects.

        Search objects must implement an iterate method that uses
        the error class to update the current parameter estimate.

        Attributes
        ----------
        parameter : float
        Current parameter estimate.

        perror : float
        Error on the current parameter.

        error : Error
        An instance of a  class derived from Error.
        """

        def __init__(self,error):
            self.error = error

        def iterate(self):
            '''Run one iteration of the search algorithm.

            To be implemented in the sub class.
            Should update self.parameter and self.perror
            '''
            pass


        def iterate_until(self, threshold):
            """Iterate until error < threshold

            Parameters
            ----------
            threshold : float
                The desired maximum error threshold

            Returns
            -------
            parameter : float
                The value of the parameter when the error is less than the
                threshold

            perror : float
                The associated error
            """

            # Iterate until the error is small
            while abs(self.perror) > threshold:
                self.iterate()

            return self.parameter, self.perror

class NelderMead2d(Search):
    """Find a minima on a two dimensional surface using Nelder-Mead Simplex

    Attributes
    ---------
    x1,x2,x3 : Vector
        Two dimensional parameter vectors describing the three vertices
        of the Nelder-Mead simplex

    e1,e2,e3 : float
        The "error" or objective function value at each vertex
    """

    def __init__(self,error,x1,dx):
        """Initial setup

        Parmeters
        ---------
        x1 : Vector
            Parameter vector

        dx : Vector
            Initial guess at vertex spacing
        """
        super().__init__(error)

        # Calculate the other two points of the simplex
        x2 = al.Vector(x1.x + dx.x, x1.y)
        x3 = al.Vector(x1.x, x1.y + dx.y)

        self.x = np.array([x1,x2,x3])

        e = self.error(x3.x,x3.y)

        # Calculate the errors at all three vertices
        self.e = np.array([self.error(x1.x,x1.y),
                           self.error(x2.x,x2.y),
                           self.error(x3.x,x3.y)])

        # Sort the points
        self._sort_points()

    def iterate(self):

        # Reflect w to r and calculate er
        c = (self.x[0]+self.x[1])*0.5       # Midpoint of GB
        r = c + (c-self.x[2])

        er = self.error(r.x,r.y)

        if er < self.e[2]:         # Better than worst point?

            if er < self.e[0]:     # Better than the best point?
                # grow and take the best of r and g
                g = c + (c-self.x[2])*2
                eg = self.error(g.x,g.y)

                if eg < er:
                    self.x[2] = g
                    self.e[2] = eg
                else:
                    self.x[2] = r
                    self.e[2] = er

            elif er < self.e[1]:  # Better than the second best point?
                self._shrink()
            else:
                # Outside contraction
                s = c + (r-c)*0.5
                es = self.error(s.x,s.y)

                if es < er:
                    self.x[2] = s
                    self.e[2] = es
                else:
                    self._shrink()

        else :                      # Worse than the worse point.

            # Inside Contraction
            s = c + (self.x[2]-c)*0.5
            es = self.error(s.x,s.y)

            if es < self.e[2]:
                self.x[2] = s
                self.e[2] = es
            else:
                self._shrink()

        self._sort_points()

    @property
    def perror(self):
        return self.e[0]

    @property
    def parameter(self):
        return self.x[0]

    def _shrink(self):
        """Shrink worst and second best points towards best point
        """
        print("Shrinking!")
        self.x[2] = self.x[0] + (self.x[2]-self.x[0])*.5
        self.x[1] = self.x[0] + (self.x[1]-self.x[0])*.5
        self.e[2] = self.error(self.x[2].x,self.x[2].y)
        self.e[1] = self.error(self.x[1].x,self.x[1].y)


    def _sort_points(self):
        """Sort the vertices in order of error, best to worst
        """

        si = self.e.argsort()   # Get the sort indices
        self.e = self.e[si]     # Reorder both arrays
        self.x = self.x[si]

class MCMC(Search):
    """Markov Chain Monte-Carlo multi-dimensional search

    """

    def __init__(self,error,start,width=0.5):
        super().__init__(error)

        self.current = start
        self.e_current = self.error(self.current)

        self.posterior = [start]
        self.norm = norm(loc=0,scale=width)
        self.reject = 0
        self.n_iterations = 0

    def iterate(self):

        # Generate a proposal and calculate its likelihood
        proposal = self.propose()
        e_proposal = self.error(proposal)

        r = e_proposal/self.e_current

        if r > np.random.rand():
            self.current = proposal
            self.e_current = e_proposal
        else:
            self.reject += 1

        self.n_iterations += 1

        self.posterior.append(self.current)

    def propose(self):

#        t = -1
#
#        while t + self.current < 0 or t + self.current > np.pi/2:
        t = self.norm.rvs()

        return t + self.current

    def bake(self,iterations):

        for i in range(iterations):
            self.iterate()

        self.posterior = [self.current]
        self.n_iterations = 0
        self.reject = 0


class GoldenSection(Search):
    """Search 1D parameter space for a minima using Golden Section

    Attributes
    ----------
    left_bracket, right_bracket : float
        Initial parameter values that bracket the minimum.

    """

    def __init__(self,func,left_bracket,right_bracket,skip_check=False):
        super().__init__(func)

        # Save the brackets
        self.a = left_bracket
        self.c = right_bracket

        self.func = func

        # Caculate midpoints (b1 is always closer to a than to c)
        self.gold = 0.5*(3-np.sqrt(5))  # Golden Section (small side)
        self.b1 = (self.a + self.gold*(self.c - self.a))
        self.b2 = self.a + (1-self.gold)*(self.c - self.a)

        # Calculate the errors at the midpoint
        self.fofa  = self.func(self.a)
        self.fofb1 = self.func(self.b1)
        self.fofb2 = self.func(self.b2)
        self.fofc  = self.func(self.c)

        self.n_iterations = 0

        # Make sure the bracketing is sound
        if (self.fofb1 > self.fofa or self.fofb1 > self.fofc or
            self.fofb2 > self.fofa or self.fofb2 > self.fofc):
            raise ValueError("Error at the midpoints must be smaller " +
                             "than the error at either bracket.")


    def iterate(self):

        # Which midpoint is larger?
        if self.fofb1 > self.fofb2:        # Minima in the right segment

            # shift points
            self.a = self.b1
            self.b1 = self.b2
            self.fofb1 = self.fofb2

            # Calculate new b2 and its error
            self.b2 = (self.a + (1-self.gold)*(self.c - self.a))
            self.fofb2 = self.func(self.b2)

        else :                     # Minima in the left segment

            # shift points
            self.c = self.b2
            self.b2 = self.b1
            self.fofb2 = self.fofb1

            # Calculate new b1 and its error
            self.b1 = (self.a + self.gold*(self.c - self.a))
            self.fofb1 = self.func(self.b1)

        self.n_iterations += 1

        return self.parameter, self.error

    @property
    def parameter(self):
        if self.fofb1 < self.fofb2:
            return self.b1
        else:
            return self.b2

    @property
    def error(self):

        # Return the distance between the brackets
        if self.fofb1 < self.fofb2:
            return self.b1-self.a
        else :
            return self.c-self.b2

class Newton(Search):
    """Search parameter space for a zero via Newton's Method.

    Attributes
    ----------
    See Search for inherited parameters

    n_interations : int
        Current number of iterations
    """

    def __init__(self,error,initial_guess,dx):
        '''Initialize

        Parameters
        ----------
        error : Error
            An instance of a  class derived from Error.

        initial_guess : float
            The starting value of the parameter

        dx : float
            The step size for estimating E prime


        '''
        super().__init__(error)
        self.parameter = initial_guess
        self.dx = dx
        self.perror = self.error(initial_guess)
        self.n_iterations = 0

    def iterate(self):
        '''Run the bisection algorithm for a single iteration.

        Returns
        -------
        value : float
            The value of the parameter that is the closest to zero

        error : float
            The associated error as returned by:
            sfunction(value)

        '''

        # Get the error at the advanced position
        dx_error = self.error(self.parameter + self.dx)

        # Calculate the new position
        self.parameter = (self.parameter -
                          self.perror/(dx_error-self.perror)*self.dx)
        self.perror = self.error(self.parameter)

        self.n_iterations += 1



class Bisect(Search):
    """Search parameter space for a zero via the bisection technique.

    Bisection iteratively splits the search space in half by moving either
    the current left or right brackets to the midpoint depending on which
    side of the midpoint the zero lies.

    Attributes
    ----------
    See ZeroSearch for inherited parameters

    n_interations : int
        Current number of iterations
    """

    def __init__(self,error,left_bracket,right_bracket):
        '''Initialize

        Parameters
        ----------
        error : Callable
            The function whose zero crossing we should find.

        left_bracket : float
            Initial left bracket value

        right_bracket : float
            Initial right bracket value

        Raises
        ------
        ValueError :
            When initial brackets don't meet the condition:
            sfunction(left_bracket)*sfunction(right_bracket) < 0
        '''
        super().__init__(error)

        self.n_iterations = 0

        # Set up initial bracket values
        self._left_bracket = left_bracket
        self._right_bracket = right_bracket

        # Calculate initial errors
        self._left_error = error(left_bracket)
        self._right_error = error(right_bracket)

        # Make sure that there is a zero between the brackets.
        if self._left_error*self._right_error > 0:
            raise ValueError("Brackets must bracket a zero.")

    def iterate(self):
        '''Run the bisection algorithm for a single iteration.

        Returns
        -------
        value : float
            The value of the parameter that is the closest to zero

        error : float
            The associated error as returned by:
            sfunction(value)

        '''

        # Calculate the midpoint
        midpoint = (self._left_bracket+self._right_bracket)/2.0

        # Get the new error from sfunction
        mid_error = self.error(midpoint)

        # Which side gets rejected?
        if (self._left_error*mid_error) > 0:       # Move the left bracket
            self._left_error = mid_error
            self._left_bracket = midpoint
        elif (self._right_error*mid_error) > 0:    # Move the right bracket
            self._right_error = mid_error
            self._right_bracket = midpoint
        else:                                     # Lost the zero...
            raise ValueError("Brackets must bracket a zero")

        self.n_iterations += 1

        # Return the bracket with the lowest error
        if (abs(self._left_error) < abs(self._right_error)):
            return self._left_bracket, self._left_error
        else:
            return self._right_bracket, self._right_error


    @property

    def parameter(self):
        '''Return the bracket with the smallest perror'''

        # Which bracket currently has the smallest error?
        if (abs(self._left_error) < abs(self._right_error)):
            return self._left_bracket
        else:
            return self._right_bracket

    @property
    def perror(self):
        '''Return bracket size'''

        return self._right_bracket - self._left_bracket
