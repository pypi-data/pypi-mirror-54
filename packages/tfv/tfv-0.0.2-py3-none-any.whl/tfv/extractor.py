"""A module defining all Extractor classes. Extractors are the primary objects for model result data extraction"""

import os
import numpy as np
import datetime as dt
from abc import ABC, abstractmethod
from netCDF4 import Dataset
from tfv.geometry import Mesh
from tfv.misc import Expression, unsupported_decorator, get_date_num


__version__ = "0.0.2"
__author__ = "toby.devlin@bmtglobal.com, jonah.chorley@bmtglobal.com"
__aus_date__ = "%d/%m/%Y %H:%M:%S"


class Extractor(ABC):
    """
    A base class that defines the API for all model result subclasses. Examples of these subclasses
    might be model results such as a TUFLOW FV NetCDF file, a Hycom NetCDF file or a TUFLOW FV .dat file.
    """

    result_type = None

    def __init__(self, file, is_spherical):
        """Initializes Extractor object with a model results file i.e A TUFLOW FV netCDF4 results file."""

        # Store file path string as attribute
        self.file = file
        self.is_spherical = is_spherical

        # Prepare static Extractor attributes
        self.__prep_file_handle__()
        self.__prep_time_vector__()
        self.__prep_2d_geometry__()
        self.__prep_3d_geometry__()

    @abstractmethod
    def get_raw_data(self, variable, ii):
        """
        Query to extract raw data at a time step (if time-varying).

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param ii -- integer | The time vector index at which to extract the data.

        Returns
        -------
        :return data -- array | The raw data as 1D or 2D numpy array

        Examples
        --------
        data = extractor.get_raw_data('H', 10)
        """
        pass

    @abstractmethod
    def get_stat_vector(self, ii):
        """
        Query to extract an array that defines invalid model data.

        Arguments
        ---------
        :param ii -- integer | Time index at which to extract the stat array.

        Returns
        -------
        :return stat -- logical array | True if model cells/nodes are invalid (i.e dry cells).

        Examples
        --------
        stat = extractor.get_stat_vector(10)
        """
        pass

    @abstractmethod
    def get_z_layer_faces(self, ii):
        """
        Query to extract an array that defines the vertical layer faces of a 3D model.

        Arguments
        ---------
        :param ii -- integer | Time index at which to extract the vertical layer faces.

        Returns
        -------
        :return lfz -- array | Vertical layer faces. If model is 2D returns None.

        Examples
        --------
        lfz = extractor.get_z_layer_faces(10)
        """
        pass

    @abstractmethod
    def get_integral_data(self, ii, datum, limits):
        """
        Query to extract data for vertical integration at given time step. Principle data is the
        integral limit (z2 - z1) for each 2D model cell/node and dz for each 3D model cell/node.

        Arguments
        ---------
        :param ii -- integer | Time index at which to extract the vertical layer faces.
        :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.

        Returns
        -------
        :return (z2_z1, dz) -- tuple | The elevation limits (z2 - z1) for each 2D cell/node & dz for each 3D cell/node
        """
        pass

    @abstractmethod
    def get_sheet_cell(self, variable, ii, datum='sigma', limits=(0, 1), z_data=None):
        """
        Query to extract data in a 2D map format ('sheet') at model cell centroids for a given time step. If model
        data is 3D then it is depth-averaged according to the depth-averaging vertical datum and vertical limits.

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param ii -- integer | Time index at which to extract the data.

        Keyword Arguments
        -----------------
        :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.
        :param z_data -- tuple | Vertical integration data returned by self.get_integral_data

        Returns
        -------
        :return data -- 1D or 2D array | A 2D spatial 'sheet' of the relevant variable at time step ii.

        Examples
        --------
        >> data = extractor.get_sheet_cell('V_x', 10, 'depth', (0, 1))
        >> data = extractor.get_sheet_cell('V_x', 10, 'elevation', (-5, -4))

        >> z2_z1, dz = extractor.get_integral_data(15, 'sigma', (0, 1))
        >> data = extractor.get_sheet_cell('V_x', 15, z_data=(z2_z1, dz))
        """
        pass

    @abstractmethod
    def get_sheet_node(self, variable, ii, datum='sigma', limits=(0, 1), z_data=None):
        """
        Query to extract data in a 2D map format ('sheet') at model cell vertices for a given time step. If model
        data is 3D then it is depth-averaged according to the depth-averaging vertical datum and vertical limits.

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param ii -- integer | Time index at which to extract the data.

        Keyword Arguments
        -----------------
        :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.
        :param z_data -- tuple | Vertical integration data returned by self.get_integral_data

        Returns
        -------
        :return data -- 1D or 2D array | A 2D spatial 'sheet' of the relevant variable at time step ii.

        Examples
        --------
        >> data = extractor.get_sheet_node('V_x', 10, 'depth', (0, 1))
        >> data = extractor.get_sheet_node('V_x', 10, 'elevation', (-5, -4))

        >> z2_z1, dz = extractor.get_integral_data(15, 'sigma', (0, 1))
        >> data = extractor.get_sheet_node('V_x', 15, z_data=(z2_z1, dz))
        """
        pass

    @abstractmethod
    def get_sheet_grid(self, variable, ii, grid_x, grid_y, datum='sigma', limits=(0, 1), z_data=None, grid_index=None):
        """
        Query to extract data in a 2D map format ('sheet') at fixed grid points for a given time step. If model
        data is 3D then it is depth-averaged according to the depth-averaging vertical datum and vertical limits.

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param ii -- integer | Time index at which to extract the data.
        :param grid_x -- 1D array | Horizontal grid point values
        :param grid_y -- 1D array | Vertical grid point values

        Keyword Arguments
        -----------------
        :param datum -- string | Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        :param limits -- tuple | Vertical depth-averaging limits relative to vertical datum.
        :param z_data -- tuple | Vertical integration data returned by self.get_integral_data
        :param grid_index -- 2D array | Mesh cell index for each grid point returned by self.get_grid_index

        Returns
        -------
        :return data -- 2D array | A gridded 2D spatial 'sheet' of the relevant variable at time step ii.

        Examples
        --------
        >> xlim = [extractor.node_x.min(), extractor.node_x.max()]
        >> ylim = [extractor.node_y.min(), extractor.node_y.max()]
        >> grid_x = np.linspace(xlim[0], xlim[1], 100)
        >> grid_y = np.linspace(ylim[0], ylim[1], 100)
        >> data = extractor.get_sheet_grid('H', 10, grid_x, grid_y)

        >> index = extractor.get_grid_index(grid_x, grid_y)
        >> data = extractor.get_sheet_grid('H', 10, grid_x, grid_y, grid_index=index)
        """
        pass

    @abstractmethod
    def get_curtain_cell(self, variable, ii, polyline, x_data=None, index=None):
        """
        Query to extract data in a 2D slice format ('curtain') at the cell centroids for a given time step. It does
        this along the polyline specified.

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param ii -- integer | Time index at which to extract the data.
        :param polyline -- 2D array | Polyline as [x, y] used to slice 3D data.

        Keyword Arguments
        -----------------
        :param x_data -- tuple | Model edge intersection(x) data returned by self.get_intersections.
        :param index -- tuple | Curtain index data returned by self.get_curtain_cell_index.

        Returns
        -------
        :return data -- array | A 2D slice 'curtain' of the relevant variable at time step ii.

        Examples
        --------
        >> polyline = np.array([[0, 0], [10, 10]])
        >> data = extractor.get_curtain_cell('SAL', 10, polyline)

        >> x_data = extractor.get_intersections(polyline)
        >> index = extractor.get_curtain_cell_index(polyline, x_data=x_data)
        >> data = extractor.get_curtain_cell('V_x', 15, polyline, x_data=intersections, index=index)
        """
        pass

    @abstractmethod
    def get_curtain_edge(self, variable, ii, polyline, x_data=None, index=None):
        """
        Query to extract data in a 2D slice format ('curtain') at the cell centroids for a given time step. It does
        this along the polyline specified.

        This function is currently not supported.
        """
        pass

    @abstractmethod
    def get_curtain_grid(self, variable, ii, polyline, grid_x, grid_y, x_data=None, index=None, grid_index=None):
        """
        Query to extract data in a 2D slice format ('curtain') at fixed grid points for a given time step. It does
        this along the polyline specified.

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param ii -- integer | Time index at which to extract the data.
        :param polyline -- 2D array | Polyline as [x, y] used to slice 3D data.
        :param grid_x -- 1D array | Horizontal grid point values
        :param grid_y -- 1D array | Vertical grid point values

        Keyword Arguments
        -----------------
        :param x_data -- tuple | Model edge intersection(x) data returned by self.get_intersections.
        :param index -- tuple | Curtain index data returned by extractor.get_curtain_cell_index.
        :param grid_index -- 2D array | Curtain cell index for each grid point

        Returns
        -------
        :return data -- array | A gridded 2D slice 'curtain' of the relevant variable at time step ii.

        Examples
        --------
        >> polyline = np.array([[0, 0], [10, 10]])
        >> grid_x = np.linspace(0, 100, 50)
        >> grid_y = np.linspace(-20, 0, 50)
        >> data = extractor.get_curtain_grid('SAL', 10, polyline, grid_x, grid_y)
        """
        pass

    @abstractmethod
    def get_profile_cell(self, variable, ii, point, index=None):
        """
        Query to extract data as 1D vertical profile of cells at the given time step.
        It does this at the point specified.

        Arguments
        ---------
        :param variable -- string | Name of time varying data set to be extracted.
        :param ii -- integer | Time index at which to extract the data.
        :param point -- tuple | Point (x, y) of profile location.

        Keyword Arguments
        -----------------
        :param index -- integer | Index of cell which contains the point.

        Returns
        -------
        :return data -- array | A 1D section of the vertical values of the relevant variable.

        Examples
        --------
        data = extractor.get_profile_cell('SAL', 10, (20, 30))
        """
        pass

    @abstractmethod
    def __prep_file_handle__(self):
        """Command which prepares the file handle for the extractor class"""

    @abstractmethod
    def __prep_time_vector__(self):
        """Command which prepares the result time stamp vector relative to python epoch"""

    @abstractmethod
    def __prep_2d_geometry__(self):
        """Command which prepares the result 2D mesh geometry"""

    @abstractmethod
    def __prep_3d_geometry__(self):
        """A command which prepares the result 3D mesh geometry"""


class FvExtractor(Extractor, Mesh):
    """
    Class that extracts data from a TUFLOW FV netCDF4 result file.

    Arguments
    ----------
    :param file -- string | Model result file path.

    Keyword Arguments
    -----------------
    :param is_spherical -- bool | True if model geometry defined in spherical coordinate reference system.

    Returns
    -------
    :return extractor -- object | FvExtractor instance
    """

    result_type = 'Cell-centred TUFLOWFV output'

    def __init__(self, file, is_spherical=True):
        super(FvExtractor, self).__init__(file, is_spherical)

    def get_raw_data(self, variable, ii):
        return self.nc[variable][ii, :].data

    def get_stat_vector(self, ii):
        return self.nc['stat'][ii, :].data == 0

    def get_z_layer_faces(self, ii):
        return self.nc['layerface_Z'][ii, :].data

    def get_integral_data(self, ii, datum, limits):
        lfz = self.get_z_layer_faces(ii)

        # Get water level (wl) and bed level (bl) of each 2D cell
        wl = lfz[self.wli]
        bl = lfz[self.bli]

        # Determine integral limits z1 and z2 for each 2D cell using wl, bl and the limits
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
        lfz = np.maximum(lfz, z1[self.idx4])
        lfz = np.minimum(lfz, z2[self.idx4])

        # Get upper z layer face and lower z layer face for each 3D cell
        ul = np.delete(lfz, self.bli)
        ll = np.delete(lfz, self.wli)
        dz = ul - ll

        # Clean up integral limit (z2 - z1) to avoid division by zero
        z2_z1 = z2 - z1
        mask = z2_z1 == 0

        # Return integral limit of each 2D cell and dz of each 3D cell contained within integral limit
        return np.ma.masked_array(data=z2_z1, mask=mask, fill_value=np.nan), dz

    @Expression.decorator
    def get_sheet_cell(self, variable, ii, datum='sigma', limits=(0, 1), z_data=None):
        # Get the raw data
        data = self.get_raw_data(variable, ii)
        stat = self.get_stat_vector(ii)

        # Check if data is 3D
        if data.size == self.nc3:
            # Get integral data for depth averaging
            if z_data is None:
                z_data = self.get_integral_data(ii, datum, limits)
            z2_z1, dz = z_data

            # Update stat vector with invalid limits
            stat = (stat | z2_z1.mask)

            # Integrate the data w.r.t z
            data = np.bincount(self.idx2, data * dz) * (1 / z2_z1)

        # Reshape stat vector for 2D sheets i.e bed mass
        if data.shape != stat.shape:
            n = data.shape[1]
            stat = np.tile(stat, (n, 1))
            stat = np.transpose(stat)

        # Return the data
        return np.ma.MaskedArray(data=data, mask=stat, fill_value=np.nan)

    @Expression.decorator
    def get_sheet_node(self, variable, ii, datum='sigma', limits=(0, 1), z_data=None):
        # Get the raw data
        data = self.get_raw_data(variable, ii)
        stat = self.get_stat_vector(ii)

        # Check if data is 3D
        if data.size == self.nc3:
            # Get integral data for depth averaging
            if z_data is None:
                z_data = self.get_integral_data(ii, datum, limits)
            z2_z1, dz = z_data

            # Update stat vector for invalid limits (z2 - z1)
            stat = (stat | z2_z1.mask)

            # Integrate the data w.r.t z
            data = np.bincount(self.idx2, data * dz) * (1 / z2_z1)

        # Create copy of 2D node recovery weights
        weights = np.copy(self.weights)

        # Set weightings of invalid cells to zero
        weights[stat, :] = 0

        # Rescale weightings to account for discounted cells
        weights_sum = np.bincount(self.cell_node.flatten(), weights.flatten())
        stat = weights_sum == 0
        weights_sum[stat] = -999
        weights = weights / weights_sum[self.cell_node]

        if data.ndim == 1:
            # For each cell, calculate the weighted nodal data values
            tmp = np.tile(data, (4, 1)).transpose() * weights

            # Sum weighted data values for each node to get final vertex data
            data_node = np.bincount(self.cell_node.flatten(), tmp.flatten())
        else:
            data_node = np.empty((self.nv2, data.shape[1]), dtype=np.float64)
            for jj in range(data.shape[1]):
                # For each cell, calculate the weighted nodal data values
                tmp = np.tile(data[:, jj], (4, 1)).transpose() * weights

                # Sum weighted data values for each node to get final vertex data
                data_node[:, jj] = np.bincount(self.cell_node.flatten(), tmp.flatten())

            stat = np.tile(stat, (data.shape[1], 1))
            stat = np.transpose(stat)

        # Return the data
        return np.ma.MaskedArray(data=data_node, mask=stat, fill_value=np.nan)

    def get_sheet_grid(self, variable, ii, xg, yg, datum='sigma', limits=(0, 1), z_data=None, grid_index=None):
        # Get grid index
        if grid_index is None:
            grid_index = self.get_grid_index(xg, yg)
        mask = np.equal(grid_index, -999)
        valid = np.equal(mask, False)

        # Index mesh data using grid index
        grid_data = np.ma.MaskedArray(data=np.zeros(grid_index.shape) * np.nan, fill_value=np.nan, mask=mask)
        grid_data[valid] = self.get_sheet_cell(variable, ii, datum, limits, z_data)[grid_index[valid]]

        # Return gridded data
        return grid_data

    @Expression.decorator
    def get_curtain_cell(self, variable, ii, polyline, x_data=None, index=None):
        # Get prerequisite data
        stat = self.get_stat_vector(ii)
        data = self.get_raw_data(variable, ii)

        # Check if data is 3D
        assert data.size == self.nc3, "Data is not 3D"

        # Get edge intersection data
        if x_data is None:
            x_data = self.get_intersection_data(polyline)
        _, _, idx = x_data

        # Get curtain index data
        if index is None:
            index = self.get_curtain_cell_index(polyline, x_data)
        line_index, cell_index = index

        # Return curtain data
        return np.ma.MaskedArray(data=data[cell_index], mask=stat[idx[line_index]], fill_value=np.nan)

    @unsupported_decorator
    def get_curtain_edge(self, variable, ii, polyline, x_data=None, index=None):
        pass

    def get_curtain_grid(self, variable, ii, polyline, xg, yg, x_data=None, index=None, grid_index=None):
        # Get grid index
        if grid_index is None:
            geo = self.get_curtain_cell_geo(ii, polyline, x_data)
            grid_index = Mesh(*geo).get_grid_index(xg, yg)
        mask = np.equal(grid_index, -999)
        valid = np.equal(mask, False)

        # Index mesh data using grid index
        grid_data = np.ma.MaskedArray(data=np.zeros(grid_index.shape) * np.nan, fill_value=np.nan, mask=mask)
        grid_data[valid] = self.get_curtain_cell(variable, ii, polyline, x_data, index)[grid_index[valid]]

        # Return gridded data
        return grid_data

    @Expression.decorator
    def get_profile_cell(self, variable, time, point, index=None):
        # Get the raw data
        data = self.get_raw_data(variable, time)

        # Get 2D cell index
        if index is None:
            index = self.get_cell_index(point[0], point[1])

        # Index the data
        data = data[self.idx2 == index]

        # Repeat to get discrete elements
        insert = np.arange(0, data.size)
        data = np.insert(data, insert, data[insert])

        return data

    def __prep_file_handle__(self):
        # Store netCDF4 Dataset handle
        self.nc = Dataset(self.file, 'r')

        # Assert the file type is correct
        self.result_type = getattr(self.nc, 'Type', None)
        assert self.result_type == type(self).result_type, "Invalid file"

    def __prep_time_vector__(self):
        # Define fv epoch relative to python epoch
        fv_epoch = dt.datetime(1990, 1, 1)
        fv_epoch = get_date_num(fv_epoch)

        # Prepare time vector relative to python epoch
        fv_time_vector = self.nc['ResTime'][:].data
        py_time_vector = fv_time_vector*3600 + fv_epoch

        # Store data as attributes
        self.time_vector = py_time_vector
        self.nt = self.time_vector.size

    def __prep_2d_geometry__(self):
        # Get basic data from file
        node_x = self.nc['node_X'][:].data
        node_y = self.nc['node_Y'][:].data
        cell_node = self.nc['cell_node'][:].data - 1

        # Identify null node indices
        cell_node[cell_node == -1] = -999

        # Initialize 2d geometry as Mesh
        Mesh.__init__(self, node_x, node_y, cell_node)

    def __prep_3d_geometry__(self):
        # Get basic data from file
        self.nz = self.nc['NL'][:].data

        # Prepare variables to define 3D mesh
        index = np.arange(self.nz.size)
        self.idx2 = np.repeat(index, self.nz)
        self.idx3 = np.cumsum(self.nz) - self.nz
        self.idx4 = np.repeat(index, self.nz + 1)
        self.wli = self.idx3 + index
        self.bli = self.wli + self.nz
        self.nc3 = self.idx2.size

    def get_curtain_cell_index(self, polyline, x_data=None):
        # Get cell x_data
        if x_data is None:
            x_data = self.get_intersection_data(polyline)
        _, _, idx = x_data

        # Determine which cells in the polyline are valid
        is_valid = idx != -999

        # Prepare indexing variables for curtain
        idx = idx[is_valid]  # 2D cell index for each column in curtain
        nz = self.nz[idx]  # Number of 3D cells for each column in curtain
        n = int(np.sum(nz))  # Total number of 3D cells in curtain
        idx3 = np.cumsum(nz) - nz  # Index of top 3D cell for each column in curtain

        # Get 1D polyline index of the curtain cells (maps curtain cell to polyline segments)
        line_index = np.repeat(np.where(is_valid)[0], nz)

        # Get 3D cell index of the curtain cells (maps curtain cell to 3D model cell)
        cell_index = np.repeat(self.idx3[idx], nz) + (np.arange(n) - np.repeat(idx3, nz))

        return line_index, cell_index

    def get_curtain_cell_geo(self, ii, polyline, x_data=None, index=None):
        # Get layer face z
        lfz = self.get_z_layer_faces(ii)

        # Get edge intersection(x) data
        if x_data is None:
            x_data = self.get_intersection_data(polyline)
        x, y, idx = x_data

        # Get curtain index
        if index is None:
            index = self.get_curtain_cell_index(polyline, x_data)
        line_index, cell_index = index

        # Convert x & y into (m) if spherical
        if self.is_spherical:
            r_e = 6.371*10**6
            cf = np.pi/180
            x = (r_e*np.cos(y*cf))*(x*cf)
            y = r_e*(y*cf)

        # Prepare curtain mesh (x, y)
        dx = np.diff(x)
        dy = np.diff(y)
        ds = np.hypot(dx, dy)
        s = np.cumsum(ds)
        s = np.hstack((0, s))

        s1 = s[line_index]
        s2 = s[line_index + 1]
        z1 = np.delete(lfz, self.wli)[cell_index]
        z2 = np.delete(lfz, self.bli)[cell_index]

        # Get nodes and node indices that define each cell
        n = cell_index.size
        node_x = np.vstack((s1, s2, s2, s1)).ravel('F')
        node_y = np.vstack((z1, z1, z2, z2)).ravel('F')
        cell_node = np.arange(n * 4, dtype=np.int32).reshape(n, 4)

        # Return geometry
        return node_x, node_y, cell_node

    def get_profile_cell_geo(self, ii, point, index=None):
        # Get layer face z
        lfz = self.get_z_layer_faces(ii)

        # Get 2D cell index
        if index is None:
            index = self.get_cell_index(point[0], point[1])

        # Index faces of cell
        lfz = lfz[self.idx4 == index]

        # Repeat to represent discrete elements
        insert = np.arange(1, lfz.size-1)
        lfz = np.insert(lfz, insert, lfz[insert])

        return lfz

    def write_time_series_file(self, out_file, locations):
        """
        Query that writes 2D & 3D point time series data from a TUFLOW FV netCDF4 results file.

        Arguments
        ---------
        :param out_file -- string | File path to write time series file.
        :param locations -- dictionary | Extraction points as dict(SITE_1=(x, y), SITE_2=(x, y)).
        """

        # Check if out path exists
        if os.path.isfile(out_file):
            user_input = input(out_file + ' exists - enter Y/N to proceed:\n')
            while True:
                if user_input.upper() == 'Y':
                    os.remove(out_file)
                    break
                elif user_input.upper() == 'N':
                    break
                else:
                    user_input = input('Invalid user input please enter Y/N:\n')

        # Get list of valid variables
        variables, exclude = [], ['ResTime']
        for var in self.nc.variables.keys():
            if var not in exclude and self.nc[var].shape[0] == self.nt:
                variables.append(var)

        # Check variable dimensions, required for pre-allocation & indexing
        num_dim = {}
        for var in variables:
            if self.nc.variables[var].shape[1] == self.nc2:
                num_dim[var] = 2
            elif self.nc.variables[var].shape[1] == self.nc3:
                num_dim[var] = 3

        # Get 2D cell index (ii) of each point
        idx = {name: self.get_cell_index(point[0], point[1])[0] for name, point in locations.items()}

        # Preallocate memory for each location
        profile, size = {}, ()
        for name in locations:
            profile[name] = {}
            for var in variables:
                if var == 'layerface_Z':
                    size = (self.nt, self.nz[idx[name]]+1)
                elif num_dim[var] == 3:
                    size = (self.nt, self.nz[idx[name]])
                elif num_dim[var] == 2:
                    size = (self.nt, 1)
                data = np.empty(size, dtype=np.float32)
                mask = np.zeros(size, dtype=np.bool)
                profile[name][var] = np.ma.masked_array(data=data, mask=mask)

        # For each variable, for each time step, for each site get the data
        for var in variables:
            for ii in range(self.nt):
                data = self.get_raw_data(var, ii)
                stat = self.get_stat_vector(ii)
                for name in locations:
                    if var == 'layerface_Z':
                        profile[name][var][ii, :] = data[self.idx4 == idx[name]]
                    elif num_dim[var] == 3:
                        profile[name][var][ii, :] = data[self.idx2 == idx[name]]
                    elif num_dim[var] == 2:
                        profile[name][var][ii, :] = data[idx[name]]
                    profile[name][var].mask[ii, :] = stat[idx[name]]
                del data

        # Create netCDF4 outfile & add time dimension
        nc = Dataset(out_file, 'w', format='NETCDF4')
        nc.createDimension('time', self.nt)

        # Create time variable and write out data
        nc.createVariable('ResTime', 'f8', dimensions=('time', ), fill_value=np.nan)
        nc.variables['ResTime'][:] = self.nc.variables['ResTime'][:].data

        # For each location, for each variable, write out data
        dims = ()
        for name in locations:
            nc.createGroup(name)
            nc[name].createDimension('x', 1)
            nc[name].createDimension('y', 1)

            nc[name].createVariable('x', 'f8', dimensions=('x',))
            nc[name].createVariable('y', 'f8', dimensions=('x',))

            nc[name].variables['x'][:] = locations[name][0]
            nc[name].variables['y'][:] = locations[name][1]

            nc[name].createDimension('z', self.nz[idx[name]])
            nc[name].createDimension('lfz', self.nz[idx[name]]+1)

            for var in variables:
                if var == 'layerface_Z':
                    dims = ('time', 'lfz',)
                elif num_dim[var] == 3:
                    dims = ('time', 'z',)
                elif num_dim[var] == 2:
                    dims = ('time',)
                nc[name].createVariable(var, 'f8', dimensions=dims, fill_value=np.nan)
                nc[name].variables[var][:] = profile[name][var]

        nc.close()
        return

    def write_data_to_ascii(self, out_file, data, resolution, bbox=None, grid_index=None):
        """
        Query data at cell centroids to gridded raster ASCII file.

        Arguments
        ---------
        :param out_file -- string | File path of .asc file to write data to.
        :param data -- 1D array | Cell centred TUFLOW FV data as numpy array.
        :param resolution -- float | Grid resolution at which to output data.

        Keyword Arguments
        -----------------
        :param bbox -- list | The bounding box to trim the data with as [left, bottom, right, top].
        :param grid_index -- 2D array | Mesh cell index for each grid point returned by self.get_grid_index
        """

        # Calculate grid parameters
        if bbox is None:
            x_min, x_max = self.node_x.min(), self.node_x.max()
            y_min, y_max = self.node_y.min(), self.node_y.max()
        else:
            x_min, x_max = bbox[0], bbox[2]
            y_min, y_max = bbox[1], bbox[3]

        dx = x_max - x_min
        dy = y_max - y_min

        nc = int(np.ceil(dx / resolution))
        nr = int(np.ceil(dy / resolution))

        xg = np.linspace(x_min, x_max, nc)
        yg = np.linspace(y_min, y_max, nr)

        # Get grid index & flip (x increasing, y decreasing)
        if grid_index is None:
            grid_index = self.get_grid_index(xg, yg)
        grid_index = np.flipud(grid_index)
        valid = grid_index != -999

        # Index mesh data using grid index
        grid_data = np.ones(grid_index.shape) * np.nan
        grid_data[valid] = data[grid_index[valid]]
        grid_data[np.isnan(grid_data)] = -999

        # Specify header
        header = \
            [
                'ncols {:d}'.format(nc),
                'nrows {:d}'.format(nr),
                'xllcorner {:.7f}'.format(x_min-dx/2),
                'yllcorner {:.7f}'.format(y_min-dy/2),
                'cellsize {:.7f}'.format(resolution),
                'NODATA_value {:d}'.format(-999)
            ]

        # Prepare row format
        row_fmt = ['{' + 'a[{}]:.7f'.format(jj) + '}' for jj in range(nc)]
        row_fmt = ' '.join(row_fmt) + '\n'

        # Write ASCII file
        with open(out_file, 'w') as asc:
            asc.write('\n'.join(header)+'\n')
            for ii in range(nr):
                asc.write(row_fmt.format(a=grid_data[ii, :]))

    # Inherit doc strings (needs to be done a better way)
    get_raw_data.__doc__ = Extractor.get_raw_data.__doc__
    get_stat_vector.__doc__ = Extractor.get_stat_vector.__doc__
    get_z_layer_faces.__doc__ = Extractor.get_z_layer_faces.__doc__
    get_integral_data.__doc__ = Extractor.get_integral_data.__doc__

    get_sheet_cell.__doc__ = Extractor.get_sheet_cell.__doc__
    get_sheet_node.__doc__ = Extractor.get_sheet_node.__doc__
    get_sheet_grid.__doc__ = Extractor.get_sheet_grid.__doc__

    get_curtain_cell.__doc__ = Extractor.get_curtain_cell.__doc__
    get_curtain_edge.__doc__ = Extractor.get_curtain_edge.__doc__
    get_curtain_grid.__doc__ = Extractor.get_curtain_grid.__doc__
    get_profile_cell.__doc__ = Extractor.get_profile_cell.__doc__
