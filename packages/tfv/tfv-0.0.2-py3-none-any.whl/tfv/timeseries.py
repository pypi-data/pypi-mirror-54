"""A module defining all point time series extractor classes"""

import numpy as np
from netCDF4 import Dataset
from abc import ABC, abstractmethod
import datetime as dt
from tfv.misc import Expression
from tfv.geometry import Mesh


__version__ = "0.0.2"
__author__ = "toby.devlin@bmtglobal.com, jonah.chorley@bmtglobal.com"
__aus_date__ = "%d/%m/%Y %H:%M:%S"


class TimeSeries(ABC):
    """A base class which defines the API for all point time series based model result data extraction"""

    def __init__(self, file):
        """Initializes TimeSeries extractor object with model result file"""

        # Store file path string as attribute
        self.file = file
        self.sites = None

        # Prepare static TimeSeries attributes
        self.__prepare_file_handle__()
        self.__prepare_time_vector__()
        self.__prepare_locations__()

    @abstractmethod
    def get_raw_data(self, variable, site):
        """
        Query to extract raw time series data at a given location.

        Arguments
        ---------
        :param variable -- string | Name of time series data set to be extracted.
        :param site -- string | Location at which to extract the time series data.

        Returns
        -------
        :return data -- array | The raw time series data as 1D or 2D numpy array

        Examples
        --------
        data = extractor.get_raw_data('H', 'SITE_1')
        """

    @abstractmethod
    def get_stat_vector(self, site):
        """
        Query to extract an array that defines invalid time series data at a given location.

        Arguments
        ---------
        :param site -- string | Location at which to extract the time series data.

        Returns
        -------
        :return stat -- logical array | True if time series data is invalid (i.e cell is dry).

        Examples
        --------
        stat = extractor.get_stat_vector('SITE_1')
        """

    @abstractmethod
    def get_z_layer_faces(self, site):
        """
        Query to extract an array that defines the vertical layer faces of a 3D model at a given location.

        Arguments
        ---------
        :param site -- string | Location at which to extract the time series data.

        Returns
        -------
        :return lfz -- array | Vertical layer faces. If model is 2D returns None.

        Examples
        --------
        lfz = extractor.get_z_layer_faces('SITE_1')
        """

    @abstractmethod
    def get_integral_data(self, site, datum, limits):
        """
        Query to extract data for vertical integration at a given location. Principle data is the
        integral limit (z2 - z1) and dz for each 3D model cell at the location.

        Arguments
        ---------
        :param site -- string | Location at which to extract the time series data.
        :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.

        Returns
        -------
        :return (z2_z1, dz) -- tuple | The elevation limits (z2 - z1) & dz for each 3D cell/node at a given location
        """

    @abstractmethod
    def get_data(self, variable, site, datum='sigma', limits=(0, 1)):
        """
        Query to extract time series data at a given location. If model data is 3D then it is
        depth-averaged according to the depth-averaging vertical datum and vertical limits.

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param site -- string | Location at which to extract the time series data.

        Keyword Arguments
        -----------------
        :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.

        Returns
        -------
        :return data -- array | Time series data at a given location.
        """

    @abstractmethod
    def __prepare_file_handle__(self):
        """Command which prepares the file handle for the extractor class"""

    @abstractmethod
    def __prepare_time_vector__(self):
        """Command which prepares the result time stamp vector relative to python epoch"""

    @abstractmethod
    def __prepare_locations__(self):
        """Command which prepares locations found in result time series file"""


class FvTimeSeries(TimeSeries):

    def __init__(self, file):
        super(FvTimeSeries, self).__init__(file)

    @Expression.decorator
    def get_raw_data(self, variable, site):
        return self.nc[site][variable][:].data.transpose()

    def get_stat_vector(self, site):
        return self.get_raw_data('stat', site) == 0

    def get_z_layer_faces(self, site):
        return self.get_raw_data('layerface_Z', site)

    def get_integral_data(self, site, datum, limits):
        # Get z layer faces
        lfz = self.get_z_layer_faces(site)

        # Get water level (wl) and bed level (bl) for each time step
        wli, bli = 0, lfz.shape[0]-1
        wl, bl = lfz[wli, :], lfz[bli, :]

        # Determine integral limits z1 and z2 for each time step using wl, bl and the limits
        if datum == 'sigma':
            z1 = limits[0] * (wl - bl) + bl
            z2 = limits[1] * (wl - bl) + bl
        elif datum == 'height':
            z1 = limits[0] + bl
            z2 = limits[1] + bl
        elif datum == 'depth':
            z1 = wl - limits[1]
            z2 = wl - limits[0]
        elif datum == 'elevation':
            z1 = limits[0]
            z2 = limits[1]
        else:
            return None

        # Create integral limits, filtering z2 and z1 above and below water level or bed level
        z1 = np.minimum(np.maximum(z1, bl), wl)
        z2 = np.minimum(np.maximum(z2, bl), wl)

        # Squeeze out middle value of each vertical layer face
        lfz = np.maximum(lfz, np.tile(z1, (lfz.shape[0], 1)))
        lfz = np.minimum(lfz, np.tile(z2, (lfz.shape[0], 1)))

        # Get upper z layer face and lower z layer face for each 3D cell
        ul = np.delete(lfz, bli, axis=0)
        ll = np.delete(lfz, wli, axis=0)
        dz = ul - ll

        # Clean up integral limit to avoid division by zero
        z2_z1 = z2 - z1
        mask = z2_z1 == 0

        # Return integral limit of each 2D cell and dz of each 3D cell contained within integral limit
        return np.ma.masked_array(data=z2_z1, mask=mask, fill_value=np.nan), dz

    @Expression.decorator
    def get_data(self, variable, site, datum='sigma', limits=(0, 1)):
        # Get the raw data
        data = self.get_raw_data(variable, site)
        stat = self.get_stat_vector(site)

        # If data is 2D depth average
        if data.ndim == 2:
            # Get the integral limits
            z2_z1, dz = self.get_integral_data(site, datum, limits)

            # Update stat vector with invalid limits
            stat = (stat | z2_z1.mask)

            # Integrate the data w.r.t z
            data = np.nansum(data*dz, axis=0) * (1 / z2_z1)

        # Return the data
        return np.ma.masked_array(data=data, mask=stat, fill_value=np.nan)

    def __prepare_file_handle__(self):
        self.nc = Dataset(self.file, 'r')

    def __prepare_time_vector__(self):
        # Prepare time vector relative to python epoch
        fv_time_vector = self.nc['ResTime'][:].data
        fv_epoch = dt.datetime(1990, 1, 1, 10).timestamp()
        fv_time_delta = fv_time_vector*3600

        self.time_vector = fv_time_delta + fv_epoch
        self.nt = self.time_vector.size

    def __prepare_locations__(self):
        self.locations = {}
        for group in self.nc.groups.keys():
            xp = self.nc[group]['x'][:].data[0]
            yp = self.nc[group]['y'][:].data[0]
            self.locations[group] = [xp, yp]

    def get_geometry(self, site):
        z = self.get_z_layer_faces(site)
        t = np.tile(self.time_vector, (z.shape[0], 1))

        tc = np.hstack((t[:, [0]], 0.5 * (t[:, :-1] + t[:, 1:]), t[:, [-1]]))
        zc = np.hstack((z[:, [0]], 0.5 * (z[:, :-1] + z[:, 1:]), z[:, [-1]]))

        node_x, node_y = tc.ravel('F'), zc.ravel('F')

        nz, nt = tc.shape
        ii = np.arange(nz - 1)
        jj = np.arange(nt - 1)

        jj, ii = np.meshgrid(jj, ii)
        tl = np.ravel(ii + nz * jj, 'F')
        tr = np.ravel(ii + nz * (jj + 1), 'F')

        cell_node = np.vstack((tl, tl + 1, tr + 1, tr))
        cell_node = cell_node.transpose()

        return Mesh(node_x, node_y, cell_node)

    # Inherit doc strings (needs to be done a better way)
    get_raw_data.__doc__ = TimeSeries.get_raw_data.__doc__
    get_stat_vector.__doc__ = TimeSeries.get_stat_vector.__doc__
    get_z_layer_faces.__doc__ = TimeSeries.get_z_layer_faces.__doc__
    get_integral_data.__doc__ = TimeSeries.get_integral_data.__doc__

    get_data.__doc__ = TimeSeries.get_data.__doc__

    __prepare_file_handle__.__doc__ = TimeSeries.__prepare_file_handle__.__doc__
    __prepare_time_vector__.__doc__ = TimeSeries.__prepare_time_vector__.__doc__
    __prepare_locations__.__doc__ = TimeSeries.__prepare_locations__.__doc__
