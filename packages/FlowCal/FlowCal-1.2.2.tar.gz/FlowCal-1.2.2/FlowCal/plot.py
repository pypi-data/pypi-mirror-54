"""
Functions for visualizing flow cytometry data.

Functions in this module are divided in two categories:

- Simple Plot Functions, with a signature similar to the following::

      plot_fxn(data_list, channels, parameters, savefig)

  where `data_list` is a NxD FCSData object or numpy array, or a list of
  such, `channels` spcecifies the channel or channels to use for the plot,
  `parameters` are function-specific parameters, and `savefig` indicates
  whether to save the figure to an image file. Note that `hist1d` uses
  `channel` instead of `channels`, since it uses a single channel, and
  `density2d` only accepts one FCSData object or numpy array as its first
  argument.

  Simple Plot Functions do not create a new figure or axis, so they can be
  called directly to plot in a previously created axis if desired. If
  `savefig` is not specified, the plot is maintained in the current axis
  when the function returns. This allows for further modifications to the
  axis by direct calls to, for example, ``plt.xlabel``, ``plt.title``, etc.
  However, if `savefig` is specified, the figure is closed after being
  saved. In this case, the function may include keyword parameters
  `xlabel`, `ylabel`, `xlim`, `ylim`, `title`, and others related to
  legend or color, which allow the user to modify the axis prior to saving.

  The following functions in this module are Simple Plot Functions:

    - ``hist1d``
    - ``density2d``
    - ``scatter2d``
    - ``scatter3d``

- Complex Plot Functions, which create a figure with several axes, and use
  one or more Simple Plot functions to populate the axes. They always
  include a `savefig` argument, which indicates whether to save the figure
  to a file. If `savefig` is not specified, the plot is maintained in the
  newly created figure when the function returns. However, if `savefig` is
  specified, the figure is closed after being saved.

  The following functions in this module are Complex Plot Functions:

    - ``density_and_hist``
    - ``scatter3d_and_projections``

"""

import packaging
import numpy as np
import scipy.ndimage.filters
import matplotlib
import matplotlib.scale
import matplotlib.transforms
import matplotlib.ticker
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties
import warnings

# Use default colors from palettable if available
try:
    import palettable
except ImportError as e:
    cmap_default = plt.get_cmap(matplotlib.rcParams['image.cmap'])
else:
    cmap_default = palettable.colorbrewer.diverging.Spectral_8_r.mpl_colormap

savefig_dpi = 250

###
# HELPER FUNCTIONS FOR SCALE CLASSES
###

def _base_down(x, base=10):
    """
    Floor `x` to the nearest lower ``base^n``, where ``n`` is an integer.

    Parameters
    ----------
    x : float
        Number to calculate the floor from.
    base : float, optional
        Base used to calculate the floor.

    Return
    ------
    float
        The nearest lower ``base^n`` from `x`, where ``n`` is an integer.

    """
    if x == 0.0:
        return -base
    lx = np.floor(np.log(x) / np.log(base))
    return base ** lx


def _base_up(x, base=10):
    """
    Ceil `x` to the nearest higher ``base^n``, where ``n`` is an integer.

    Parameters
    ----------
    x : float
        Number to calculate the ceiling from.
    base : float, optional
        Base used to calculate the ceiling.

    Return
    ------
    float
        The nearest higher ``base^n`` from `x`, where ``n`` is an integer.

    """
    if x == 0.0:
        return base
    lx = np.ceil(np.log(x) / np.log(base))
    return base ** lx

###
# CUSTOM SCALES
###

class _InterpolatedInverseTransform(matplotlib.transforms.Transform):
    """
    Class that inverts a given transform class using interpolation.

    Parameters
    ----------
    transform : matplotlib.transforms.Transform
        Transform class to invert. It should be a monotonic transformation.
    smin : float
        Minimum value to transform.
    smax : float
        Maximum value to transform.
    resolution : int, optional
        Number of points to use to evaulate `transform`. Default is 1000.

    Methods
    -------
    transform_non_affine(x)
        Apply inverse transformation to a Nx1 numpy array.

    Notes
    -----
    Upon construction, this class generates an array of `resolution` points
    between `smin` and `smax`. Next, it evaluates the specified
    transformation on this array, and both the original and transformed
    arrays are stored. When calling ``transform_non_affine(x)``, these two
    arrays are used along with ``np.interp()`` to inverse-transform ``x``.

    Note that `smin` and `smax` are also transformed and stored. When using
    ``transform_non_affine(x)``, any values in ``x`` outside the range
    specified by `smin` and `smax` transformed are masked.

    """
    # ``input_dims``, ``output_dims``, and ``is_separable`` are required by
    # matplotlib.
    input_dims = 1
    output_dims = 1
    is_separable = True

    def __init__(self, transform, smin, smax, resolution=1000):
        # Call parent's constructor
        matplotlib.transforms.Transform.__init__(self)
        # Store transform object
        self._transform = transform

        # Generate input array
        self._s_range = np.linspace(smin, smax, resolution)
        # Evaluate provided transformation and store result
        self._x_range = transform.transform_non_affine(self._s_range)
        # Transform bounds and store
        self._xmin = transform.transform_non_affine(smin)
        self._xmax = transform.transform_non_affine(smax)
        if self._xmin > self._xmax:
            self._xmax, self._xmin = self._xmin, self._xmax

    def transform_non_affine(self, x, mask_out_of_range=True):
        """
        Transform a Nx1 numpy array.

        Parameters
        ----------
        x : array
            Data to be transformed.
        mask_out_of_range : bool, optional
            Whether to mask input values out of range.

        Return
        ------
        array or masked array
            Transformed data.

        """
        # Mask out-of-range values
        if mask_out_of_range:
            x_masked = np.ma.masked_where((x < self._xmin) | (x > self._xmax),
                                          x)
        else:
            x_masked = x
        # Calculate s and return
        return np.interp(x_masked, self._x_range, self._s_range)

    def inverted(self):
        """
        Get an object representing an inverse transformation to this class.

        Since this class implements the inverse of a given transformation,
        this function just returns the original transformation.

        Return
        ------
        matplotlib.transforms.Transform
            Object implementing the reverse transformation.

        """
        return self._transform

class _LogicleTransform(matplotlib.transforms.Transform):
    """
    Class implementing the Logicle transform, from scale to data values.

    Relevant parameters can be specified manually, or calculated from
    a given FCSData object.

    Parameters
    ----------
    T : float
        Maximum range of data values. If `data` is None, `T` defaults to
        262144. If `data` is not None, specifying `T` overrides the
        default value that would be calculated from `data`.
    M : float
        (Asymptotic) number of decades in display scale units. If `data` is
        None, `M` defaults to 4.5. If `data` is not None, specifying `M`
        overrides the default value that would be calculated from `data`.
    W : float
        Width of linear range in display scale units. If `data` is None,
        `W` defaults to 0.5. If `data` is not None, specifying `W`
        overrides the default value that would be calculated from `data`.
    data : FCSData or numpy array or list of FCSData or numpy array
        Flow cytometry data from which a set of T, M, and W parameters will
        be generated.
    channel : str or int
        Channel of `data` from which a set of T, M, and W parameters will
        be generated. `channel` should be specified if `data` is not None.

    Methods
    -------
    transform_non_affine(s)
        Apply transformation to a Nx1 numpy array.

    Notes
    -----
    Logicle scaling combines the advantages of logarithmic and linear
    scaling. It is useful when data spans several orders of magnitude
    (when logarithmic scaling would be appropriate) and a significant
    number of datapoints are negative.

    Logicle scaling is implemented using the following equation::

        x = T * 10**(-(M-W)) * (10**(s-W) \
                - (p**2)*10**(-(s-W)/p) + p**2 - 1)

    This equation transforms data ``s`` expressed in "display scale" units
    into ``x`` in "data value" units. Parameters in this equation
    correspond to the class properties. ``p`` and ``W`` are related as
    follows::

        W = 2*p * log10(p) / (p + 1)

    If a FCSData object or list of FCSData objects is specified along with
    a channel, the following default logicle parameters are used: T is
    taken from the largest ``data[i].range(channel)[1]`` or the largest
    element in ``data[i]`` if ``data[i].range()`` is not available, M is
    set to the largest of 4.5 and ``4.5 / np.log10(262144) * np.log10(T)``,
    and W is taken from ``(M - log10(T / abs(r))) / 2``, where ``r`` is the
    minimum negative event. If no negative events are present, W is set to
    zero.

    References
    ----------
    .. [1] D.R. Parks, M. Roederer, W.A. Moore, "A New Logicle Display
    Method Avoids Deceptive Effects of Logarithmic Scaling for Low Signals
    and Compensated Data," Cytometry Part A 69A:541-551, 2006, PMID
    16604519.

    """
    # ``input_dims``, ``output_dims``, and ``is_separable`` are required by
    # matplotlib.
    input_dims = 1
    output_dims = 1
    is_separable = True
    # Locator objects need this object to store the logarithm base used as an
    # attribute.
    base = 10

    def __init__(self, T=None, M=None, W=None, data=None, channel=None):
        matplotlib.transforms.Transform.__init__(self)
        # If data is included, try to obtain T, M and W from it
        if data is not None:
            if channel is None:
                raise ValueError("if data is provided, a channel should be"
                    + " specified")
            # Convert to list if necessary
            if not isinstance(data, list):
                data = [data]
            # Obtain T, M, and W if not specified
            # If elements of data have ``.range()``, use it to determine the
            # max data value. Else, use the maximum value in the array.
            if T is None:
                T = 0
                for d in data:
                    # Extract channel
                    y = d[:, channel] if d.ndim > 1 else d
                    if hasattr(y, 'range') and hasattr(y.range, '__call__'):
                        Ti = y.range(0)[1]
                    else:
                        Ti = np.max(y)
                    T = Ti if Ti > T else T
            if M is None:
                M = max(4.5, 4.5 / np.log10(262144) * np.log10(T))
            if W is None:
                W = 0
                for d in data:
                    # Extract channel
                    y = d[:, channel] if d.ndim > 1 else d
                    # If negative events are present, use minimum.
                    if np.any(y < 0):
                        r = np.min(y)
                        Wi = (M - np.log10(T / abs(r))) / 2
                        W = Wi if Wi > W else W
        else:
            # Default parameter values
            if T is None:
                T = 262144
            if M is None:
                M = 4.5
            if W is None:
                W = 0.5
        # Check that property values are valid
        if T <= 0:
            raise ValueError("T should be positive")
        if M <= 0:
            raise ValueError("M should be positive")
        if W < 0:
            raise ValueError("W should not be negative")

        # Store parameters
        self._T = T
        self._M = M
        self._W = W

        # Calculate dependent parameter p
        # It is not possible to analytically obtain ``p`` as a function of W
        # only, so ``p`` is calculated numerically using a root finding
        # algorithm. The initial estimate provided to the algorithm is taken
        # from the asymptotic behavior of the equation as ``p -> inf``. This
        # results in ``W = 2*log10(p)``.
        p0 = 10**(W / 2.)
        # Functions to provide to the root finding algorithm
        def W_f(p):
            return 2*p / (p + 1) * np.log10(p)
        def W_root(p, W_target):
            return W_f(p) - W_target
        # Find solution
        sol = scipy.optimize.root(W_root, x0=p0, args=(W))
        # Solution should be unique
        assert sol.success
        assert len(sol.x) == 1
        # Store solution
        self._p = sol.x[0]

    @property
    def T(self):
        """
        Maximum range of data.

        """
        return self._T

    @property
    def M(self):
        """
        (Asymptotic) number of decades in display scale units.

        """
        return self._M

    @property
    def W(self):
        """
        Width of linear range in display scale units.

        """
        return self._W

    def transform_non_affine(self, s):
        """
        Apply transformation to a Nx1 numpy array.

        Parameters
        ----------
        s : array
            Data to be transformed in display scale units.

        Return
        ------
        array or masked array
            Transformed data, in data value units.

        """
        T = self._T
        M = self._M
        W = self._W
        p = self._p
        # Calculate x
        return T * 10**(-(M-W)) * (10**(s-W) - (p**2)*10**(-(s-W)/p) + p**2 - 1)

    def inverted(self):
        """
        Get an object implementing the inverse transformation.

        Return
        ------
        _InterpolatedInverseTransform
            Object implementing the reverse transformation.

        """
        return _InterpolatedInverseTransform(transform=self,
                                             smin=0,
                                             smax=self._M)

class _LogicleLocator(matplotlib.ticker.Locator):
    """
    Determine the tick locations for logicle axes.

    Parameters
    ----------
    transform : _LogicleTransform
        transform object
    subs : array, optional
        Subtick values, as multiples of the main ticks. If None, do not use
        subticks.

    """

    def __init__(self, transform, subs=None):
        self._transform = transform
        if subs is None:
            self._subs = [1.0]
        else:
            self._subs = subs
        self.numticks = 15

    def set_params(self, subs=None, numticks=None):
        """
        Set parameters within this locator.

        Parameters
        ----------
        subs : array, optional
            Subtick values, as multiples of the main ticks.
        numticks : array, optional
            Number of ticks.

        """
        if numticks is not None:
            self.numticks = numticks
        if subs is not None:
            self._subs = subs

    def __call__(self):
        """
        Return the locations of the ticks.

        """
        # Note, these are untransformed coordinates
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        """
        Get a set of tick values properly spaced for logicle axis.

        """
        # Extract base from transform object
        b = self._transform.base
        # The logicle domain is divided into two regions: A "linear" region,
        # which may include negative numbers, and a "logarithmic" region, which
        # only includes positive numbers. These two regions are separated by a
        # value t, given by the logicle equations. An illustration is given
        # below.
        #
        # -t ==0== t ========>
        #     lin       log
        #
        # vmin and vmax can be anywhere in this domain, meaning that both should
        # be greater than -t.
        #
        # The logarithmic region will only have major ticks at integral log
        # positions. The linear region will have a major tick at zero, and one
        # major tick at the largest absolute  integral log value in screen
        # inside this region. Subticks will be added at multiples of the
        # integral log positions.

        # If the linear range is too small, create new transformation object
        # with slightly wider linear range. Otherwise, the number of decades
        # below will be infinite
        if self._transform.W == 0 or \
                self._transform.M / self._transform.W > self.numticks:
            self._transform = _LogicleTransform(
                T=self._transform.T,
                M=self._transform.M,
                W=self._transform.M / self.numticks)
        # Calculate t
        t = - self._transform.transform_non_affine(0)

        # Swap vmin and vmax if necessary
        if vmax < vmin:
            vmin, vmax = vmax, vmin
        # Calculate minimum and maximum limits in scale units
        vmins = self._transform.inverted().transform_non_affine(vmin)
        vmaxs = self._transform.inverted().transform_non_affine(vmax)

        # Check whether linear or log regions are present
        has_linear = has_log = False
        if vmin <= t:
            has_linear = True
            if vmax > t:
                has_log = True
        else:
            has_log = True

        # Calculate number of ticks in linear and log regions
        # The number of ticks is distributed by the fraction that each region
        # occupies in scale units
        if has_linear:
            fraction_linear = (min(vmaxs, 2*self._transform.W) - vmins) / \
                (vmaxs - vmins)
            numticks_linear = np.round(self.numticks*fraction_linear)
        else:
            numticks_linear = 0
        if has_log:
            fraction_log = (vmaxs - max(vmins, 2*self._transform.W)) / \
                (vmaxs - vmins)
            numticks_log = np.round(self.numticks*fraction_log)
        else:
            numticks_log = 0

        # Calculate extended ranges and step size for tick location
        # Extended ranges take into account discretization.
        if has_log:
            # The logarithmic region's range will include from the decade
            # immediately below the lower end of the region to the decade
            # immediately above the upper end.
            # Note that this may extend the logarithmic region to the left.
            log_ext_range = [np.floor(np.log(max(vmin, t)) / np.log(b)),
                             np.ceil(np.log(vmax) / np.log(b))]
            # Since a major tick will be located at the lower end of the
            # extended range, make sure that it is not too close to zero.
            if vmin <= 0:
                zero_s = self._transform.inverted().\
                    transform_non_affine(0)
                min_tick_space = 1./self.numticks
                while True:
                    min_tick_s = self._transform.inverted().\
                        transform_non_affine(b**log_ext_range[0])
                    if (min_tick_s - zero_s)/(vmaxs - vmins) < min_tick_space \
                            and ((log_ext_range[0] + 1) < log_ext_range[1]):
                        log_ext_range[0] += 1
                    else:
                        break
            # Number of decades in the extended region
            log_decades = log_ext_range[1] - log_ext_range[0]
            # The step is at least one decade.
            if numticks_log > 1:
                log_step = max(np.floor(float(log_decades)/(numticks_log-1)), 1)
            else:
                log_step = 1
        else:
            # Linear region only
            linear_range = [vmin, vmax]
            # Initial step size will be one decade below the maximum whole
            # decade in the range
            linear_step = _base_down(
                linear_range[1] - linear_range[0], b) / b
            # Reduce the step size according to specified number of ticks
            while (linear_range[1] - linear_range[0])/linear_step > \
                    numticks_linear:
                linear_step *= b
            # Get extended range by discretizing the region limits
            vmin_ext = np.floor(linear_range[0]/linear_step)*linear_step
            vmax_ext = np.ceil(linear_range[1]/linear_step)*linear_step
            linear_range_ext = [vmin_ext, vmax_ext]

        # Calculate major tick positions
        major_ticklocs = []
        if has_log:
            # Logarithmic region present
            # If a linear region is present, add the negative of the lower limit
            # of the extended log region and zero. Then, add ticks for each
            # logarithmic step as calculated above.
            if has_linear:
                major_ticklocs.append(- b**log_ext_range[0])
                major_ticklocs.append(0)
            # Use nextafter to pick the next floating point number, and try to
            # include the upper limit in the generated range.
            major_ticklocs.extend(b ** (np.arange(
                log_ext_range[0],
                np.nextafter(log_ext_range[1], np.inf),
                log_step)))
        else:
            # Only linear region present
            # Draw ticks according to linear step calculated above.
            # Use nextafter to pick the next floating point number, and try to
            # include the upper limit in the generated range.
            major_ticklocs.extend(np.arange(
                linear_range_ext[0],
                np.nextafter(linear_range_ext[1], np.inf),
                linear_step))
        major_ticklocs = np.array(major_ticklocs)

        # Add subticks if requested
        subs = self._subs
        if (subs is not None) and (len(subs) > 1 or subs[0] != 1.0):
            ticklocs = []
            if has_log:
                # Subticks for each major tickloc present
                for major_tickloc in major_ticklocs:
                    ticklocs.extend(subs * major_tickloc)
                # Subticks from one decade below the lowest
                major_ticklocs_pos = major_ticklocs[major_ticklocs > 0]
                if len(major_ticklocs_pos):
                    tickloc_next_low = np.min(major_ticklocs_pos)/b
                    ticklocs.append(tickloc_next_low)
                    ticklocs.extend(subs * tickloc_next_low)
                # Subticks for the negative linear range
                if vmin < 0:
                    ticklocs.extend([(-ti) for ti in ticklocs if ti < -vmin ])
            else:
                ticklocs = list(major_ticklocs)
                # If zero is present, add ticks from a decade below the lowest
                if (vmin < 0) and (vmax > 0):
                    major_ticklocs_nonzero = major_ticklocs[
                        np.nonzero(major_ticklocs)]
                    tickloc_next_low = np.min(np.abs(major_ticklocs_nonzero))/b
                    ticklocs.append(tickloc_next_low)
                    ticklocs.extend(subs * tickloc_next_low)
                    ticklocs.append(-tickloc_next_low)
                    ticklocs.extend(subs * - tickloc_next_low)

        else:
            # Subticks not requested
            ticklocs = major_ticklocs

        # Remove ticks outside requested range
        ticklocs = [t for t in ticklocs if (t >= vmin) and (t <= vmax)]

        return self.raise_if_exceeds(np.array(ticklocs))


    def view_limits(self, vmin, vmax):
        """
        Try to choose the view limits intelligently.

        """
        b = self._transform.base
        if vmax < vmin:
            vmin, vmax = vmax, vmin

        if not matplotlib.ticker.is_decade(abs(vmin), b):
            if vmin < 0:
                vmin = -_base_up(-vmin, b)
            else:
                vmin = _base_down(vmin, b)
        if not matplotlib.ticker.is_decade(abs(vmax), b):
            if vmax < 0:
                vmax = -_base_down(-vmax, b)
            else:
                vmax = _base_up(vmax, b)

        if vmin == vmax:
            if vmin < 0:
                vmin = -_base_up(-vmin, b)
                vmax = -_base_down(-vmax, b)
            else:
                vmin = _base_down(vmin, b)
                vmax = _base_up(vmax, b)
        result = matplotlib.transforms.nonsingular(vmin, vmax)
        return result

class _LogicleScale(matplotlib.scale.ScaleBase):
    """
    Class that implements the logicle axis scaling.

    To select this scale, an instruction similar to
    ``gca().set_yscale("logicle")`` should be used. Note that any keyword
    arguments passed to ``set_xscale`` and ``set_yscale`` are passed along
    to the scale's constructor.

    Parameters
    ----------
    T : float
        Maximum range of data values. If `data` is None, `T` defaults to
        262144. If `data` is not None, specifying `T` overrides the
        default value that would be calculated from `data`.
    M : float
        (Asymptotic) number of decades in display scale units. If `data` is
        None, `M` defaults to 4.5. If `data` is not None, specifying `M`
        overrides the default value that would be calculated from `data`.
    W : float
        Width of linear range in display scale units. If `data` is None,
        `W` defaults to 0.5. If `data` is not None, specifying `W`
        overrides the default value that would be calculated from `data`.
    data : FCSData or numpy array or list of FCSData or numpy array
        Flow cytometry data from which a set of T, M, and W parameters will
        be generated.
    channel : str or int
        Channel of `data` from which a set of T, M, and W parameters will
        be generated. `channel` should be specified if `data` is not None.

    """
    # String name of the scaling
    name = 'logicle'

    def __init__(self, axis, **kwargs):
        # Run parent's constructor
        if packaging.version.parse(matplotlib.__version__) \
                >= packaging.version.parse('3.1.0'):
            matplotlib.scale.ScaleBase.__init__(self, axis)
        else:
            matplotlib.scale.ScaleBase.__init__(self)

        # Initialize and store logicle transform object
        self._transform = _LogicleTransform(**kwargs)

    def get_transform(self):
        """
        Get a new object to perform the scaling transformation.

        """
        return _InterpolatedInverseTransform(transform=self._transform,
                                             smin=0,
                                             smax=self._transform._M)

    def set_default_locators_and_formatters(self, axis):
        """
        Set up the locators and formatters for the scale.

        Parameters
        ----------
        axis: matplotlib.axis
            Axis for which to set locators and formatters.

        """
        axis.set_major_locator(_LogicleLocator(self._transform))
        axis.set_minor_locator(_LogicleLocator(self._transform,
                                               subs=np.arange(2.0, 10.)))
        axis.set_major_formatter(matplotlib.ticker.LogFormatterSciNotation(
            labelOnlyBase=True))

    def limit_range_for_scale(self, vmin, vmax, minpos):
        """
        Return minimum and maximum bounds for the logicle axis.

        Parameters
        ----------
        vmin : float
            Minimum data value.
        vmax : float
            Maximum data value.
        minpos : float
            Minimum positive value in the data. Ignored by this function.

        Return
        ------
        float
            Minimum axis bound.
        float
            Maximum axis bound.

        """
        vmin_bound = self._transform.transform_non_affine(0)
        vmax_bound = self._transform.transform_non_affine(self._transform.M)
        vmin = max(vmin, vmin_bound)
        vmax = min(vmax, vmax_bound)
        return vmin, vmax

# Register custom scales
matplotlib.scale.register_scale(_LogicleScale)


###
# SIMPLE PLOT FUNCTIONS
###

def hist1d(data_list,
           channel=0,
           xscale='logicle',
           bins=256,
           histtype='stepfilled',
           normed_area=False,
           normed_height=False,
           xlabel=None,
           ylabel=None,
           xlim=None,
           ylim=None,
           title=None,
           legend=False,
           legend_loc='best',
           legend_fontsize='medium',
           legend_labels=None,
           facecolor=None,
           edgecolor=None,
           savefig=None,
           **kwargs):
    """
    Plot one 1D histogram from one or more flow cytometry data sets.

    Parameters
    ----------
    data_list : FCSData or numpy array or list of FCSData or numpy array
        Flow cytometry data to plot.
    channel : int or str, optional
        Channel from where to take the events to plot. If ndim == 1,
        channel is ignored. String channel specifications are only
        supported for data types which support string-based indexing
        (e.g. FCSData).
    xscale : str, optional
        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.
    bins : int or array_like, optional
        If `bins` is an integer, it specifies the number of bins to use.
        If `bins` is an array, it specifies the bin edges to use. If `bins`
        is None or an integer, `hist1d` will attempt to use
        ``data.hist_bins`` to generate the bins automatically.
    histtype : {'bar', 'barstacked', 'step', 'stepfilled'}, str, optional
        Histogram type. Directly passed to ``plt.hist``.
    normed_area : bool, optional
        Flag indicating whether to normalize the histogram such that the
        area under the curve is equal to one. The resulting plot is
        equivalent to a probability density function.
    normed_height : bool, optional
        Flag indicating whether to normalize the histogram such that the
        sum of all bins' heights is equal to one. The resulting plot is
        equivalent to a probability mass function. `normed_height` is
        ignored if `normed_area` is True.
    savefig : str, optional
        The name of the file to save the figure to. If None, do not save.

    Other parameters
    ----------------
    xlabel : str, optional
        Label to use on the x axis. If None, attempts to extract channel
        name from last data object.
    ylabel : str, optional
        Label to use on the y axis. If None and ``normed_area==True``, use
        'Probability'. If None, ``normed_area==False``, and
        ``normed_height==True``, use 'Counts (normalized)'. If None,
        ``normed_area==False``, and ``normed_height==False``, use 'Counts'.
    xlim : tuple, optional
        Limits for the x axis. If not specified and `bins` exists, use
        the lowest and highest values of `bins`.
    ylim : tuple, optional
        Limits for the y axis.
    title : str, optional
        Plot title.
    legend : bool, optional
        Flag specifying whether to include a legend. If `legend` is True,
        the legend labels will be taken from `legend_labels` if present,
        else they will be taken from ``str(data_list[i])``.
    legend_loc : str, optional
        Location of the legend.
    legend_fontsize : int or str, optional
        Font size for the legend.
    legend_labels : list, optional
        Labels to use for the legend.
    facecolor : matplotlib color or list of matplotlib colors, optional
        The histogram's facecolor. It can be a list with the same length as
        `data_list`. If `edgecolor` and `facecolor` are not specified, and
        ``histtype == 'stepfilled'``, the facecolor will be taken from the
        module-level variable `cmap_default`.
    edgecolor : matplotlib color or list of matplotlib colors, optional
        The histogram's edgecolor. It can be a list with the same length as
        `data_list`. If `edgecolor` and `facecolor` are not specified, and
        ``histtype == 'step'``, the edgecolor will be taken from the
        module-level variable `cmap_default`.
    kwargs : dict, optional
        Additional parameters passed directly to matploblib's ``hist``.

    Notes
    -----
    `hist1d` calls matplotlib's ``hist`` function for each object in
    `data_list`. `hist_type`, the type of histogram to draw, is directly
    passed to ``plt.hist``. Additional keyword arguments provided to
    `hist1d` are passed directly to ``plt.hist``.

    If `normed_area` is set to True, `hist1d` calls ``plt.hist`` with
    ``density`` (or ``normed``, if matplotlib's version is older than
    2.2.0) set to True. There is a bug in matplotlib 2.1.0 that
    produces an incorrect plot in these conditions. We do not recommend
    using matplotlib 2.1.0 if `normed_area` is expected to be used.

    """
    # Using `normed_area` with matplotlib 2.1.0 causes an incorrect plot to be
    # produced. Raise warning in these conditions.
    if normed_area and packaging.version.parse(matplotlib.__version__) \
            == packaging.version.parse('2.1.0'):
        warnings.warn("bug in matplotlib 2.1.0 will result in an incorrect plot"
            " when normed_area is set to True")

    # Convert to list if necessary
    if not isinstance(data_list, list):
        data_list = [data_list]

    # Default colors
    if histtype == 'stepfilled':
        if facecolor is None:
            facecolor = [cmap_default(i)
                         for i in np.linspace(0, 1, len(data_list))]
        if edgecolor is None:
            edgecolor = ['black']*len(data_list)
    elif histtype == 'step':
        if edgecolor is None:
            edgecolor = [cmap_default(i)
                         for i in np.linspace(0, 1, len(data_list))]

    # Convert colors to lists if necessary
    if not isinstance(edgecolor, list):
        edgecolor = [edgecolor]*len(data_list)
    if not isinstance(facecolor, list):
        facecolor = [facecolor]*len(data_list)

    # Collect scale parameters that depend on all elements in data_list
    xscale_kwargs = {}
    if xscale=='logicle':
        t = _LogicleTransform(data=data_list, channel=channel)
        xscale_kwargs['T'] = t.T
        xscale_kwargs['M'] = t.M
        xscale_kwargs['W'] = t.W

    # Iterate through data_list
    for i, data in enumerate(data_list):
        # Extract channel
        if data.ndim > 1:
            y = data[:, channel]
        else:
            y = data

        # If ``data_plot.hist_bins()`` exists, obtain bin edges from it if
        # necessary. If it does not exist, do not modify ``bins``.
        if hasattr(y, 'hist_bins') and hasattr(y.hist_bins, '__call__'):
            # If bins is None or an integer, get bin edges from
            # ``data_plot.hist_bins()``.
            if bins is None or isinstance(bins, int):
                bins = y.hist_bins(channels=0,
                                   nbins=bins,
                                   scale=xscale,
                                   **xscale_kwargs)

        # Decide whether to normalize
        if normed_height and not normed_area:
            weights = np.ones_like(y)/float(len(y))
        else:
            weights = None

        # Actually plot
        if packaging.version.parse(matplotlib.__version__) \
                >= packaging.version.parse('2.2'):
            if bins is not None:
                n, edges, patches = plt.hist(y,
                                             bins,
                                             weights=weights,
                                             density=normed_area,
                                             histtype=histtype,
                                             edgecolor=edgecolor[i],
                                             facecolor=facecolor[i],
                                             **kwargs)
            else:
                n, edges, patches = plt.hist(y,
                                             weights=weights,
                                             density=normed_area,
                                             histtype=histtype,
                                             edgecolor=edgecolor[i],
                                             facecolor=facecolor[i],
                                             **kwargs)
        else:
            if bins is not None:
                n, edges, patches = plt.hist(y,
                                             bins,
                                             weights=weights,
                                             normed=normed_area,
                                             histtype=histtype,
                                             edgecolor=edgecolor[i],
                                             facecolor=facecolor[i],
                                             **kwargs)
            else:
                n, edges, patches = plt.hist(y,
                                             weights=weights,
                                             normed=normed_area,
                                             histtype=histtype,
                                             edgecolor=edgecolor[i],
                                             facecolor=facecolor[i],
                                             **kwargs)

    # Set scale of x axis
    if xscale=='logicle':
        plt.gca().set_xscale(xscale, data=data_list, channel=channel)
    else:
        plt.gca().set_xscale(xscale)

    ###
    # Final configuration
    ###

    # x and y labels
    if xlabel is not None:
        # Highest priority is user-provided label
        plt.xlabel(xlabel)
    elif hasattr(y, 'channels'):
        # Attempt to use channel name
        plt.xlabel(y.channels[0])

    if ylabel is not None:
        # Highest priority is user-provided label
        plt.ylabel(ylabel)
    elif normed_area:
        plt.ylabel('Probability')
    elif normed_height:
        plt.ylabel('Counts (normalized)')
    else:
        # Default is "Counts"
        plt.ylabel('Counts')

    # x and y limits
    if xlim is not None:
        # Highest priority is user-provided limits
        plt.xlim(xlim)
    elif bins is not None:
        # Use bins if specified
        plt.xlim((edges[0], edges[-1]))

    if ylim is not None:
        plt.ylim(ylim)

    # Title
    if title is not None:
        plt.title(title)

    # Legend
    if legend:
        if legend_labels is None:
            legend_labels = [str(data) for data in data_list]
        plt.legend(legend_labels,
                   loc=legend_loc,
                   prop={'size': legend_fontsize})

    # Save if necessary
    if savefig is not None:
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()

def density2d(data, 
              channels=[0,1],
              bins=1024,
              mode='mesh',
              normed=False,
              smooth=True,
              sigma=10.0,
              colorbar=False,
              xscale='logicle',
              yscale='logicle',
              xlabel=None,
              ylabel=None,
              xlim=None,
              ylim=None,
              title=None,
              savefig=None,
              **kwargs):
    """
    Plot a 2D density plot from two channels of a flow cytometry data set.

    `density2d` has two plotting modes which are selected using the `mode`
    argument. With ``mode=='mesh'``, this function plots the data as a true
    2D histogram, in which a plane is divided into bins and the color of
    each bin is directly related to the number of elements therein. With
    ``mode=='scatter'``, this function also calculates a 2D histogram,
    but it plots a 2D scatter plot in which each dot corresponds to a bin,
    colored according to the number elements therein. The most important
    difference is that the ``scatter`` mode does not color regions
    corresponding to empty bins. This allows for easy identification of
    regions with low number of events. For both modes, the calculated
    histogram can be smoothed using a Gaussian kernel by specifying
    ``smooth=True``. The width of the kernel is, in this case, given by
    `sigma`.

    Parameters
    ----------
    data : FCSData or numpy array
        Flow cytometry data to plot.
    channels : list of int, list of str, optional
        Two channels to use for the plot.
    bins : int or array_like or [int, int] or [array, array], optional
        Bins used for plotting:

          - If None, use ``data.hist_bins`` to obtain bin edges for both
            axes. None is not allowed if ``data.hist_bins`` is not
            available.
          - If int, `bins` specifies the number of bins to use for both
            axes. If ``data.hist_bins`` exists, it will be used to generate
            a number `bins` of bins.
          - If array_like, `bins` directly specifies the bin edges to use
            for both axes.
          - If [int, int], each element of `bins` specifies the number of
            bins for each axis. If ``data.hist_bins`` exists, use it to
            generate ``bins[0]`` and ``bins[1]`` bin edges, respectively.
          - If [array, array], each element of `bins` directly specifies
            the bin edges to use for each axis.
          - Any combination of the above, such as [int, array], [None,
            int], or [array, int]. In this case, None indicates to generate
            bin edges using ``data.hist_bins`` as above, int indicates the
            number of bins to generate, and an array directly indicates the
            bin edges. Note that None is not allowed if ``data.hist_bins``
            does not exist.
    mode : {'mesh', 'scatter'}, str, optional
        Plotting mode. 'mesh' produces a 2D-histogram whereas 'scatter'
        produces a scatterplot colored by histogram bin value.
    normed : bool, optional
        Flag indicating whether to plot a normed histogram (probability
        mass function instead of a counts-based histogram).
    smooth : bool, optional
        Flag indicating whether to apply Gaussian smoothing to the
        histogram.
    colorbar : bool, optional
        Flag indicating whether to add a colorbar to the plot.
    savefig : str, optional
        The name of the file to save the figure to. If None, do not save.

    Other parameters
    ----------------
    sigma : float, optional
        The sigma parameter for the Gaussian kernel to use when smoothing.
    xscale : str, optional
        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.
    yscale : str, optional
        Scale of the y axis, either ``linear``, ``log``, or ``logicle``
    xlabel : str, optional
        Label to use on the x axis. If None, attempts to extract channel
        name from `data`.
    ylabel : str, optional
        Label to use on the y axis. If None, attempts to extract channel
        name from `data`.
    xlim : tuple, optional
        Limits for the x axis. If not specified and `bins` exists, use
        the lowest and highest values of `bins`.
    ylim : tuple, optional
        Limits for the y axis. If not specified and `bins` exists, use
        the lowest and highest values of `bins`.
    title : str, optional
        Plot title.
    kwargs : dict, optional
        Additional parameters passed directly to the underlying matplotlib
        functions: ``plt.scatter`` if ``mode==scatter``, and
        ``plt.pcolormesh`` if ``mode==mesh``.

    """
    # Extract channels to plot
    if len(channels) != 2:
        raise ValueError('two channels need to be specified')
    data_plot = data[:, channels]

    # If ``data_plot.hist_bins()`` exists, obtain bin edges from it if
    # necessary.
    if hasattr(data_plot, 'hist_bins') and \
            hasattr(data_plot.hist_bins, '__call__'):
        # Check whether `bins` contains information for one or two axes
        if hasattr(bins, '__iter__') and len(bins)==2:
            # `bins` contains separate information for both axes
            # If bins for the X axis is not an iterable, get bin edges from
            # ``data_plot.hist_bins()``.
            if not hasattr(bins[0], '__iter__'):
                bins[0] = data_plot.hist_bins(channels=0,
                                              nbins=bins[0],
                                              scale=xscale)
            # If bins for the Y axis is not an iterable, get bin edges from
            # ``data_plot.hist_bins()``.
            if not hasattr(bins[1], '__iter__'):
                bins[1] = data_plot.hist_bins(channels=1,
                                              nbins=bins[1],
                                              scale=yscale)
        else:
            # `bins` contains information for one axis, which will be used
            # twice.
            # If bins is not an iterable, get bin edges from
            # ``data_plot.hist_bins()``.
            if not hasattr(bins, '__iter__'):
                bins = [data_plot.hist_bins(channels=0,
                                            nbins=bins,
                                            scale=xscale),
                        data_plot.hist_bins(channels=1,
                                            nbins=bins,
                                            scale=yscale)]

    else:
        # Check if ``bins`` is None and raise error
        if bins is None:
            raise ValueError("bins should be specified")

    # If colormap is not specified, use the default of this module
    if 'cmap' not in kwargs:
        kwargs['cmap'] = cmap_default

    # Calculate histogram
    H,xe,ye = np.histogram2d(data_plot[:,0], data_plot[:,1], bins=bins)

    # Smooth    
    if smooth:
        sH = scipy.ndimage.filters.gaussian_filter(
            H,
            sigma=sigma,
            order=0,
            mode='constant',
            cval=0.0)
    else:
        sH = None

    # Normalize
    if normed:
        H = H / np.sum(H)
        sH = sH / np.sum(sH) if sH is not None else None

    ###
    # Plot
    ###

    # numpy histograms are organized such that the 1st dimension (eg. FSC) =
    # rows (1st index) and the 2nd dimension (eg. SSC) = columns (2nd index).
    # Visualized as is, this results in x-axis = SSC and y-axis = FSC, which
    # is not what we're used to. Transpose the histogram array to fix the
    # axes.
    H = H.T
    sH = sH.T if sH is not None else None

    if mode == 'scatter':
        Hind = np.ravel(H)
        xc = (xe[:-1] + xe[1:]) / 2.0   # x-axis bin centers
        yc = (ye[:-1] + ye[1:]) / 2.0   # y-axis bin centers
        xv, yv = np.meshgrid(xc, yc)
        x = np.ravel(xv)[Hind != 0]
        y = np.ravel(yv)[Hind != 0]
        z = np.ravel(H if sH is None else sH)[Hind != 0]
        plt.scatter(x, y, s=1.5, edgecolor='none', c=z, **kwargs)
    elif mode == 'mesh':
        plt.pcolormesh(xe, ye, H if sH is None else sH, **kwargs)
    else:
        raise ValueError("mode {} not recognized".format(mode))

    if colorbar:
        cbar = plt.colorbar()
        if normed:
            cbar.ax.set_ylabel('Probability')
        else:
            cbar.ax.set_ylabel('Counts')

    # Set scale of axes
    if xscale=='logicle':
        plt.gca().set_xscale(xscale, data=data_plot, channel=0)
    else:
        plt.gca().set_xscale(xscale)
    if yscale=='logicle':
        plt.gca().set_yscale(yscale, data=data_plot, channel=1)
    else:
        plt.gca().set_yscale(yscale)

    # x and y limits
    if xlim is not None:
        # Highest priority is user-provided limits
        plt.xlim(xlim)
    else:
        # Use histogram edges
        plt.xlim((xe[0], xe[-1]))

    if ylim is not None:
        # Highest priority is user-provided limits
        plt.ylim(ylim)
    else:
        # Use histogram edges
        plt.ylim((ye[0], ye[-1]))

    # x and y labels
    if xlabel is not None:
        # Highest priority is user-provided label
        plt.xlabel(xlabel)
    elif hasattr(data_plot, 'channels'):
        # Attempt to use channel name
        plt.xlabel(data_plot.channels[0])

    if ylabel is not None:
        # Highest priority is user-provided label
        plt.ylabel(ylabel)
    elif hasattr(data_plot, 'channels'):
        # Attempt to use channel name
        plt.ylabel(data_plot.channels[1])

    # title
    if title is not None:
        plt.title(title)

    # Save if necessary
    if savefig is not None:
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()

def scatter2d(data_list, 
              channels=[0,1],
              xscale='logicle',
              yscale='logicle',
              xlabel=None,
              ylabel=None,
              xlim=None,
              ylim=None,
              title=None,
              color=None,
              savefig=None,
              **kwargs):
    """
    Plot 2D scatter plot from one or more FCSData objects or numpy arrays.

    Parameters
    ----------
    data_list : array or FCSData or list of array or list of FCSData
        Flow cytometry data to plot.
    channels : list of int, list of str
        Two channels to use for the plot.
    savefig : str, optional
        The name of the file to save the figure to. If None, do not save.

    Other parameters
    ----------------
    xscale : str, optional
        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.
    yscale : str, optional
        Scale of the y axis, either ``linear``, ``log``, or ``logicle``.
    xlabel : str, optional
        Label to use on the x axis. If None, attempts to extract channel
        name from last data object.
    ylabel : str, optional
        Label to use on the y axis. If None, attempts to extract channel
        name from last data object.
    xlim : tuple, optional
        Limits for the x axis. If None, attempts to extract limits from the
        range of the last data object.
    ylim : tuple, optional
        Limits for the y axis. If None, attempts to extract limits from the
        range of the last data object.
    title : str, optional
        Plot title.
    color : matplotlib color or list of matplotlib colors, optional
        Color for the scatter plot. It can be a list with the same length
        as `data_list`. If `color` is not specified, elements from
        `data_list` are plotted with colors taken from the module-level
        variable `cmap_default`.
    kwargs : dict, optional
        Additional parameters passed directly to matploblib's ``scatter``.

    Notes
    -----
    `scatter2d` calls matplotlib's ``scatter`` function for each object in
    data_list. Additional keyword arguments provided to `scatter2d` are
    passed directly to ``plt.scatter``.

    """
    # Check appropriate number of channels
    if len(channels) != 2:
        raise ValueError('two channels need to be specified')

    # Convert to list if necessary
    if not isinstance(data_list, list):
        data_list = [data_list]

    # Default colors
    if color is None:
        color = [cmap_default(i) for i in np.linspace(0, 1, len(data_list))]

    # Convert color to list, if necessary
    if not isinstance(color, list):
       color = [color]*len(data_list)

    # Iterate through data_list
    for i, data in enumerate(data_list):
        # Get channels to plot
        data_plot = data[:, channels]
        # Make scatter plot
        plt.scatter(data_plot[:,0],
                    data_plot[:,1],
                    s=5,
                    alpha=0.25,
                    color=color[i],
                    **kwargs)

    # Set labels if specified, else try to extract channel names
    if xlabel is not None:
        plt.xlabel(xlabel)
    elif hasattr(data_plot, 'channels'):
        plt.xlabel(data_plot.channels[0])
    if ylabel is not None:
        plt.ylabel(ylabel)
    elif hasattr(data_plot, 'channels'):
        plt.ylabel(data_plot.channels[1])

    # Set scale of axes
    if xscale=='logicle':
        plt.gca().set_xscale(xscale, data=data_list, channel=channels[0])
    else:
        plt.gca().set_xscale(xscale)
    if yscale=='logicle':
        plt.gca().set_yscale(yscale, data=data_list, channel=channels[1])
    else:
        plt.gca().set_yscale(yscale)

    # Set plot limits if specified, else extract range from data_list.
    # ``.hist_bins`` with one bin works better for visualization that
    # ``.range``, because it deals with two issues. First, it automatically
    # deals with range values that are outside the domain of the current scaling
    # (e.g. when the lower range value is zero and the scaling is logarithmic).
    # Second, it takes into account events that are outside the limits specified
    # by .range (e.g. negative events will be shown with logicle scaling, even
    # when the lower range is zero).
    if xlim is None:
        xlim = [np.inf, -np.inf]
        for data in data_list:
            if hasattr(data, 'hist_bins') and \
                    hasattr(data.hist_bins, '__call__'):
                xlim_data = data.hist_bins(channels=channels[0],
                                           nbins=1,
                                           scale=xscale)
                xlim[0] = xlim_data[0] if xlim_data[0] < xlim[0] else xlim[0]
                xlim[1] = xlim_data[1] if xlim_data[1] > xlim[1] else xlim[1]
    plt.xlim(xlim)
    if ylim is None:
        ylim = [np.inf, -np.inf]
        for data in data_list:
            if hasattr(data, 'hist_bins') and \
                    hasattr(data.hist_bins, '__call__'):
                ylim_data = data.hist_bins(channels=channels[1],
                                           nbins=1,
                                           scale=yscale)
                ylim[0] = ylim_data[0] if ylim_data[0] < ylim[0] else ylim[0]
                ylim[1] = ylim_data[1] if ylim_data[1] > ylim[1] else ylim[1]
    plt.ylim(ylim)

    # Title
    if title is not None:
        plt.title(title)

    # Save if necessary
    if savefig is not None:
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()

def scatter3d(data_list, 
              channels=[0,1,2],
              xscale='logicle',
              yscale='logicle',
              zscale='logicle',
              xlabel=None,
              ylabel=None,
              zlabel=None,
              xlim=None,
              ylim=None,
              zlim=None,
              title=None,
              color=None,
              savefig=None,
              **kwargs):
    """
    Plot 3D scatter plot from one or more FCSData objects or numpy arrays.

    Parameters
    ----------
    data_list : array or FCSData or list of array or list of FCSData
        Flow cytometry data to plot.
    channels : list of int, list of str
        Three channels to use for the plot.
    savefig : str, optional
        The name of the file to save the figure to. If None, do not save.

    Other parameters
    ----------------
    xscale : str, optional
        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.
    yscale : str, optional
        Scale of the y axis, either ``linear``, ``log``, or ``logicle``.
    zscale : str, optional
        Scale of the z axis, either ``linear``, ``log``, or ``logicle``.
    xlabel : str, optional
        Label to use on the x axis. If None, attempts to extract channel
        name from last data object.
    ylabel : str, optional
        Label to use on the y axis. If None, attempts to extract channel
        name from last data object.
    zlabel : str, optional
        Label to use on the z axis. If None, attempts to extract channel
        name from last data object.
    xlim : tuple, optional
        Limits for the x axis. If None, attempts to extract limits from the
        range of the last data object.
    ylim : tuple, optional
        Limits for the y axis. If None, attempts to extract limits from the
        range of the last data object.
    zlim : tuple, optional
        Limits for the z axis. If None, attempts to extract limits from the
        range of the last data object.
    title : str, optional
        Plot title.
    color : matplotlib color or list of matplotlib colors, optional
        Color for the scatter plot. It can be a list with the same length
        as `data_list`. If `color` is not specified, elements from
        `data_list` are plotted with colors taken from the module-level
        variable `cmap_default`.
    kwargs : dict, optional
        Additional parameters passed directly to matploblib's ``scatter``.

    Notes
    -----
    `scatter3d` uses matplotlib's ``scatter`` with a 3D projection.
    Additional keyword arguments provided to `scatter3d` are passed
    directly to ``scatter``.

    """
    # Check appropriate number of channels
    if len(channels) != 3:
        raise ValueError('three channels need to be specified')

    # Convert to list if necessary
    if not isinstance(data_list, list):
        data_list = [data_list]

    # Default colors
    if color is None:
        color = [cmap_default(i) for i in np.linspace(0, 1, len(data_list))]

    # Convert color to list, if necessary
    if not isinstance(color, list):
       color = [color]*len(data_list)

    # Get transformation functions for each axis
    # Explicit rescaling is required for non-linear scales because mplot3d does
    # not natively support anything but linear scale.
    if xscale == 'linear':
        xscale_transform = lambda x: x
    elif xscale == 'log':
        xscale_transform = np.log10
    elif xscale == 'logicle':
        t = _LogicleTransform(data=data_list, channel=channels[0])
        it = _InterpolatedInverseTransform(t, 0, t.M)
        xscale_transform = it.transform_non_affine
    else:
        raise ValueError('scale {} not supported'.format(xscale))

    if yscale == 'linear':
        yscale_transform = lambda x: x
    elif yscale == 'log':
        yscale_transform = np.log10
    elif yscale == 'logicle':
        t = _LogicleTransform(data=data_list, channel=channels[1])
        it = _InterpolatedInverseTransform(t, 0, t.M)
        yscale_transform = it.transform_non_affine
    else:
        raise ValueError('scale {} not supported'.format(yscale))

    if zscale == 'linear':
        zscale_transform = lambda x: x
    elif zscale == 'log':
        zscale_transform = np.log10
    elif zscale == 'logicle':
        t = _LogicleTransform(data=data_list, channel=channels[2])
        it = _InterpolatedInverseTransform(t, 0, t.M)
        zscale_transform = it.transform_non_affine
    else:
        raise ValueError('scale {} not supported'.format(zscale))

    # Make 3d axis if necessary
    ax_3d = plt.gca(projection='3d')

    # Iterate through data_list
    for i, data in enumerate(data_list):
        # Get channels to plot
        data_plot = data[:, channels]
        # Make scatter plot
        ax_3d.scatter(xscale_transform(data_plot[:, 0]),
                      yscale_transform(data_plot[:, 1]),
                      zscale_transform(data_plot[:, 2]),
                      marker='o',
                      alpha=0.1,
                      color=color[i],
                      **kwargs)

    # Remove tick labels
    ax_3d.xaxis.set_ticklabels([])
    ax_3d.yaxis.set_ticklabels([])
    ax_3d.zaxis.set_ticklabels([])

    # Set labels if specified, else try to extract channel names
    if xlabel is not None:
        ax_3d.set_xlabel(xlabel)
    elif hasattr(data_plot, 'channels'):
        ax_3d.set_xlabel(data_plot.channels[0])
    if ylabel is not None:
        ax_3d.set_ylabel(ylabel)
    elif hasattr(data_plot, 'channels'):
        ax_3d.set_ylabel(data_plot.channels[1])
    if zlabel is not None:
        ax_3d.set_zlabel(zlabel)
    elif hasattr(data_plot, 'channels'):
        ax_3d.set_zlabel(data_plot.channels[2])

    # Set plot limits if specified, else extract range from data_plot
    # ``.hist_bins`` with one bin works better for visualization that
    # ``.range``, because it deals with two issues. First, it automatically
    # deals with range values that are outside the domain of the current scaling
    # (e.g. when the lower range value is zero and the scaling is logarithmic).
    # Second, it takes into account events that are outside the limits specified
    # by .range (e.g. negative events will be shown with logicle scaling, even
    # when the lower range is zero).
    if xlim is None:
        xlim = np.array([np.inf, -np.inf])
        for data in data_list:
            if hasattr(data, 'hist_bins') and \
                    hasattr(data.hist_bins, '__call__'):
                xlim_data = data.hist_bins(channels=channels[0],
                                           nbins=1,
                                           scale=xscale)
                xlim[0] = xlim_data[0] if xlim_data[0] < xlim[0] else xlim[0]
                xlim[1] = xlim_data[1] if xlim_data[1] > xlim[1] else xlim[1]
        xlim = xscale_transform(xlim)
    ax_3d.set_xlim(xlim)

    if ylim is None:
        ylim = np.array([np.inf, -np.inf])
        for data in data_list:
            if hasattr(data, 'hist_bins') and \
                    hasattr(data.hist_bins, '__call__'):
                ylim_data = data.hist_bins(channels=channels[1],
                                           nbins=1,
                                           scale=yscale)
                ylim[0] = ylim_data[0] if ylim_data[0] < ylim[0] else ylim[0]
                ylim[1] = ylim_data[1] if ylim_data[1] > ylim[1] else ylim[1]
        ylim = yscale_transform(ylim)
    ax_3d.set_ylim(ylim)

    if zlim is None:
        zlim = np.array([np.inf, -np.inf])
        for data in data_list:
            if hasattr(data, 'hist_bins') and \
                    hasattr(data.hist_bins, '__call__'):
                zlim_data = data.hist_bins(channels=channels[2],
                                           nbins=1,
                                           scale=zscale)
                zlim[0] = zlim_data[0] if zlim_data[0] < zlim[0] else zlim[0]
                zlim[1] = zlim_data[1] if zlim_data[1] > zlim[1] else zlim[1]
        zlim = zscale_transform(zlim)
    ax_3d.set_zlim(zlim)

    # Title
    if title is not None:
        plt.title(title)

    # Save if necessary
    if savefig is not None:
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()

###
# COMPLEX PLOT FUNCTIONS
###

def density_and_hist(data,
                     gated_data=None,
                     gate_contour=None,
                     density_channels=None,
                     density_params={},
                     hist_channels=None,
                     hist_params={},
                     figsize=None,
                     savefig=None):
    """
    Make a combined density/histogram plot of a FCSData object.

    This function calls `hist1d` and `density2d` to plot a density diagram
    and a number of histograms in different subplots of the same plot using
    one single function call. Setting `density_channels` to None will not
    produce a density diagram, and setting `hist_channels` to None will not
    produce any histograms. Setting both to None will raise an error.
    Additional parameters can be provided to `density2d` and `hist1d` by
    using `density_params` and `hist_params`.

    If `gated_data` is provided, this function will plot the histograms
    corresponding to `gated_data` on top of `data`'s histograms, with some
    transparency on `data`. In addition, a legend will be added with the
    labels 'Ungated' and 'Gated'. If `gate_contour` is provided and it
    contains a valid list of 2D curves, these will be plotted on top of the
    density plot.

    Parameters
    ----------
    data : FCSData object
        Flow cytometry data object to plot.
    gated_data : FCSData object, optional
        Flow cytometry data object. If `gated_data` is specified, the
        histograms of `data` are plotted with an alpha value of 0.5, and
        the histograms of `gated_data` are plotted on top of those with
        an alpha value of 1.0.
    gate_contour : list, optional
        List of Nx2 curves, representing a gate contour to be plotted in
        the density diagram.
    density_channels : list
        Two channels to use for the density plot. If `density_channels` is
        None, do not plot a density plot.
    density_params : dict, optional
        Parameters to pass to `density2d`.
    hist_channels : list
        Channels to use for each histogram. If `hist_channels` is None,
        do not plot histograms.
    hist_params : list, optional
        List of dictionaries with the parameters to pass to each call of
        `hist1d`.
    savefig : str, optional
        The name of the file to save the figure to. If None, do not save.

    Other parameters
    ----------------
    figsize : tuple, optional
        Figure size. If None, calculate a default based on the number of
        subplots.

    Raises
    ------
    ValueError
        If both `density_channels` and `hist_channels` are None.

    """
    # Check number of plots
    if density_channels is None and hist_channels is None:
        raise ValueError("density_channels and hist_channels cannot be both "
            "None")

    # Change hist_channels to iterable if necessary
    if not hasattr(hist_channels, "__iter__"):
        hist_channels = [hist_channels]
    if isinstance(hist_params, dict):
        hist_params = [hist_params]*len(hist_channels)

    plot_density = not(density_channels is None)
    n_plots = plot_density + len(hist_channels)

    # Calculate plot size if necessary
    if figsize is None:
        height = 0.315 + 2.935*n_plots
        figsize = (6, height)

    # Create plot
    plt.figure(figsize=figsize)

    # Density plot
    if plot_density:
        plt.subplot(n_plots, 1, 1)
        # Plot density diagram
        density2d(data, channels=density_channels, **density_params)
        # Plot gate contour
        if gate_contour is not None:
            for g in gate_contour:
                plt.plot(g[:,0], g[:,1], color='k', linewidth=1.25)
        # Add title
        if 'title' not in density_params:
            if gated_data is not None:
                ret = gated_data.shape[0] * 100. / data.shape[0]
                title = "{} ({:.1f}% retained)".format(str(data), ret)
            else:
                title = str(data)
            plt.title(title)

    # Colors
    n_colors = n_plots - 1
    colors = [cmap_default(i) for i in np.linspace(0, 1, n_colors)]
    # Histogram
    for i, hist_channel in enumerate(hist_channels):
        # Define subplot
        plt.subplot(n_plots, 1, plot_density + i + 1)
        # Default colors
        hist_params_i = hist_params[i].copy()
        if 'facecolor' not in hist_params_i:
            hist_params_i['facecolor'] = colors[i]
        # Plots
        if gated_data is not None:
            hist1d(data,
                   channel=hist_channel,
                   alpha=0.5,
                   **hist_params_i)
            hist1d(gated_data,
                   channel=hist_channel,
                   alpha=1.0,
                   **hist_params_i)
            plt.legend(['Ungated', 'Gated'], loc='best', fontsize='medium')
        else:
            hist1d(data, channel=hist_channel, **hist_params_i)
    
    # Save if necessary
    if savefig is not None:
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()

def scatter3d_and_projections(data_list,
                              channels=[0,1,2],
                              xscale='logicle',
                              yscale='logicle',
                              zscale='logicle',
                              xlabel=None,
                              ylabel=None,
                              zlabel=None,
                              xlim=None,
                              ylim=None,
                              zlim=None,
                              color=None,
                              figsize=None,
                              savefig=None,
                              **kwargs):
    """
    Plot a 3D scatter plot and 2D projections from FCSData objects.

    `scatter3d_and_projections` creates a 3D scatter plot and three 2D
    projected scatter plots in four different axes for each FCSData object
    in `data_list`, in the same figure.

    Parameters
    ----------
    data_list : FCSData object, or list of FCSData objects
        Flow cytometry data to plot.
    channels : list of int, list of str
        Three channels to use for the plot.
    savefig : str, optional
        The name of the file to save the figure to. If None, do not save.

    Other parameters
    ----------------
    xscale : str, optional
        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.
    yscale : str, optional
        Scale of the y axis, either ``linear``, ``log``, or ``logicle``.
    zscale : str, optional
        Scale of the z axis, either ``linear``, ``log``, or ``logicle``.
    xlabel : str, optional
        Label to use on the x axis. If None, attempts to extract channel
        name from last data object.
    ylabel : str, optional
        Label to use on the y axis. If None, attempts to extract channel
        name from last data object.
    zlabel : str, optional
        Label to use on the z axis. If None, attempts to extract channel
        name from last data object.
    xlim : tuple, optional
        Limits for the x axis. If None, attempts to extract limits from the
        range of the last data object.
    ylim : tuple, optional
        Limits for the y axis. If None, attempts to extract limits from the
        range of the last data object.
    zlim : tuple, optional
        Limits for the z axis. If None, attempts to extract limits from the
        range of the last data object.
    color : matplotlib color or list of matplotlib colors, optional
        Color for the scatter plot. It can be a list with the same length
        as `data_list`. If `color` is not specified, elements from
        `data_list` are plotted with colors taken from the module-level
        variable `cmap_default`.
    figsize : tuple, optional
        Figure size. If None, use matplotlib's default.
    kwargs : dict, optional
        Additional parameters passed directly to matploblib's ``scatter``.

    Notes
    -----
    `scatter3d_and_projections` uses matplotlib's ``scatter``, with the 3D
    scatter plot using a 3D projection. Additional keyword arguments
    provided to `scatter3d_and_projections` are passed directly to
    ``scatter``.

    """
    # Check appropriate number of channels
    if len(channels) != 3:
        raise ValueError('three channels need to be specified')

    # Create figure
    plt.figure(figsize=figsize)

    # Axis 1: channel 0 vs channel 2
    plt.subplot(221)
    scatter2d(data_list,
              channels=[channels[0], channels[2]],
              xscale=xscale,
              yscale=zscale,
              xlabel=xlabel,
              ylabel=zlabel,
              xlim=xlim,
              ylim=zlim,
              color=color,
              **kwargs)

    # Axis 2: 3d plot
    ax_3d = plt.gcf().add_subplot(222, projection='3d')
    scatter3d(data_list,
              channels=channels,
              xscale=xscale,
              yscale=yscale,
              zscale=zscale,
              xlabel=xlabel,
              ylabel=ylabel,
              zlabel=zlabel,
              xlim=xlim,
              ylim=ylim,
              zlim=zlim,
              color=color,
              **kwargs)

    # Axis 3: channel 0 vs channel 1
    plt.subplot(223)
    scatter2d(data_list,
              channels=[channels[0], channels[1]],
              xscale=xscale,
              yscale=yscale,
              xlabel=xlabel,
              ylabel=ylabel,
              xlim=xlim,
              ylim=ylim,
              color=color,
              **kwargs)

    # Axis 4: channel 2 vs channel 1
    plt.subplot(224)
    scatter2d(data_list,
              channels=[channels[2], channels[1]],
              xscale=zscale,
              yscale=yscale,
              xlabel=zlabel,
              ylabel=ylabel,
              xlim=zlim,
              ylim=ylim,
              color=color,
              **kwargs)

    # Save if necessary
    if savefig is not None:
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()
