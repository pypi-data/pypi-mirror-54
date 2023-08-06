"""A module defining functions & objects that handle common computational geometry algorithms"""

import numpy as np

__version__ = "0.0.2"
__author__ = "toby.devlin@bmtglobal.com, jonah.chorley@bmtglobal.com"
__aus_date__ = "%d/%m/%Y %H:%M:%S"


def is_ccw(a, b, c):
    """
    Determines if elbow formed by points ABC is counter clockwise (ccw).

    Arguments
    ---------
    :param a -- tuple | Point A as tuple (x, y)
    :param b -- tuple | Point B as tuple (x, y)
    :param c -- tuple | Point C as tuple (x, y)

    Returns
    -------
    :return lgi -- logical array | True if elbow ABC is counter clockwise

    Examples
    --------
    >> a, b, c = (0, 0), (1, 1), (0, 1)
    >> is_ccw(a, b, c)
    """

    # Is angle AC > angle AB
    # is slope AC > slope AB
    lhs = (c[1] - a[1]) * (b[0] - a[0])
    rhs = (b[1] - a[1]) * (c[0] - a[0])
    return lhs > rhs


def is_intersection(a, b, c, d):
    """
    Determines if polyline AB crosses polyline CD.
    :param a: Point A as tuple (x, y)
    :param b: Point B as tuple (x, y)
    :param c: Point C as tuple (x, y)
    :param d: Point D as tuple (x, y)
    :return: True/False
    """

    abc = is_ccw(a, b, c)
    abd = is_ccw(a, b, d)

    cda = is_ccw(c, d, a)
    cdb = is_ccw(c, d, b)

    return np.logical_and(abc != abd, cda != cdb)


def get_intersection(a, b, c, d):
    """
    Gets parameters for intersections of line\s AB and line\s CD.

    Arguments
    ---------
    :param a -- tuple | Point A as tuple (x, y) of line\s AB
    :param b -- tuple | Point B as tuple (x, y) of line\s AB
    :param c -- tuple | Point C as tuple (x, y) of line\s CD
    :param d -- tuple | Point D as tuple (x, y) of line\s CD

    Returns
    -------
    :return (t, u, lc, rc, lgi) -- tuple | Line intersection parameters
    """

    # Basic preparation
    x2_x1 = b[0] - a[0]
    y2_y1 = b[1] - a[1]
    x4_x3 = d[0] - c[0]
    y4_y3 = d[1] - c[1]
    x1_x3 = a[0] - c[0]
    y1_y3 = a[1] - c[1]

    # Determine numerator a, numerator b & denominator
    num_a = x4_x3 * y1_y3 - y4_y3 * x1_x3
    num_b = x2_x1 * y1_y3 - y2_y1 * x1_x3
    denom = (y4_y3 * x2_x1 - x4_x3 * y2_y1)

    # Check for parallel lines
    is_parallel = denom == 0
    denom[is_parallel] = -999

    # Get polyline intersection parameters
    t = np.round(num_a * (1 / denom), 8)  # Normalized distance along polyline AB
    u = np.round(num_b * (1 / denom), 8)  # Normalized distance along polyline CD
    lc = (x2_x1 * y4_y3) < (x4_x3 * y2_y1)  # Left cross if polyline ABC is counter clockwise
    rc = (x2_x1 * y4_y3) > (x4_x3 * y2_y1)  # Right cross if polyline ABD is counter clockwise

    # Set parallel lines to inf
    t[is_parallel] = np.inf
    u[is_parallel] = np.inf

    # Determine logical index for valid polyline intersection
    lgi = (0 <= t) & (t <= 1) & (0 <= u) & (u <= 1)

    return t, u, lc, rc, lgi


def in_polygon(x, y, xp, yp):

    a, b = (x, y), (x-10**8, y-10**8)

    winding_num = np.zeros(x.size, dtype=np.int32)
    for ii in range(xp.size-1):
        c, d = (xp[ii], yp[ii]), (xp[ii+1], yp[ii+1])
        lgi = is_intersection(a, b, c, d)

        if np.any(lgi):
            a_ii = (a[0][lgi], a[1][lgi])
            b_ii = (b[0][lgi], b[1][lgi])
            rc = 1*is_ccw(a_ii, b_ii, d)
            lc = -1*is_ccw(a_ii, b_ii, c)
            winding_num[lgi] = winding_num[lgi] + lc + rc
        else:
            continue

    return winding_num != 0


def get_unit_vectors(xv, yv):
    """
    Gets unit tangent and unit normal vectors for line segments

    Arguments
    ---------
    :param xv -- 1D array | X coordinate of polyline
    :param yv -- 1D array | Y coordinate of polyline

    Returns
    -------
    :return (ut, un) -- tuple | Unit tangent and unit normal vectors
    """

    dx = np.diff(xv)
    dy = np.diff(yv)
    ds = np.hypot(dx, dy)

    ut = np.transpose(np.vstack((dx/ds, dy/ds)))
    un = np.hstack((-ut[:, [1]], ut[:, [0]]))

    return ut, un


class Mesh:
    """
    Creates object which handles common 2D polygonal mesh based geometry operations

    Arguments
    ---------
    :param node_x -- 1D array | X coordinate of mesh vertices
    :param node_y -- 1D array | Y coordinate of mesh vertices
    :param cell_node -- 2D array | A (n, 4) array defining each mesh cell/element by four node indices

    Returns
    -------
    :return mesh -- object | Mesh instance
    """

    def __init__(self, node_x, node_y, cell_node):
        """Initializes Mesh object with node_x, node_y & cell_node"""

        # Store basic data as attributes
        self.node_x = node_x
        self.node_y = node_y
        self.cell_node = cell_node

        # Prepare additional mesh attributes
        self.__prepare_basic__()
        self.__prepare_edge_node__()
        self.__prepare_node_weights__()
        self.__prepare_tri_index__()

    def __prepare_basic__(self):
        """Command to prepare basic mesh geometry"""

        # Set null value
        null = -999

        # Count number of 2D cells and nodes
        self.nc2 = self.cell_node.shape[0]
        self.nv2 = self.node_x.shape[0]

        # Set node_x & node_y to 64 bit floating point arrays
        self.node_x = np.array(self.node_x).astype(np.float64)
        self.node_y = np.array(self.node_y).astype(np.float64)

        # Convert to integer Array for indexing purposes
        self.cell_node[np.isnan(self.cell_node)] = null
        self.cell_node = self.cell_node.astype(np.int32)

        # Identify triangles and repeat last node for triangles
        self.is_tri = self.cell_node[:, -1] == null
        self.is_quad = self.cell_node[:, -1] != null
        self.cell_node[self.is_tri, 3] = self.cell_node[self.is_tri, 2]

    def __prepare_edge_node__(self):
        """Command to define edge_nodes (nodes & cell associated with each half-edge)"""

        # Declare edge_node as tuple (n1, n2, idx)
        self.edge_node = \
            (
                self.cell_node[:, [0, 1, 2, 3]].flatten(),
                self.cell_node[:, [1, 2, 3, 0]].flatten(),
                np.repeat(np.arange(self.cell_node.shape[0]), 4),
                np.zeros((self.nc2 * 4,), dtype=np.bool)
            )

        # Delete 4th edge of triangle cells (repeated 3rd node)
        invalid = np.where(self.edge_node[0] == self.edge_node[1])[0]
        self.edge_node = tuple(np.delete(arr, invalid) for arr in self.edge_node)

    def __prepare_node_weights__(self):
        """Command to prepare node recovery weights for nodes local to each cell"""

        # Index nx, ny for each for 5 edges (4 angles)
        ii = [3, 0, 1, 2, 3, 0]
        nx = self.node_x[self.cell_node[:, ii]]
        ny = self.node_y[self.cell_node[:, ii]]

        # For triangle cells, set last corner to be first corner
        nx[self.is_tri, 4:6] = nx[self.is_tri, 1:3]
        ny[self.is_tri, 4:6] = ny[self.is_tri, 1:3]

        # Calculate angles
        dx = nx[:, 1:] - nx[:, :-1]
        dy = ny[:, 1:] - ny[:, :-1]
        ds = np.sqrt(dx * dx + dy * dy)

        ang = np.arccos(-(dx[:, 1:] * dx[:, :-1] + dy[:, 1:] * dy[:, :-1]) / (ds[:, 1:] * ds[:, :-1]))

        # Set angle of repeated corner to 0
        ang[self.is_tri, 3] = 0

        # Sum angles for each node & divide by total angle
        ang_sum = np.bincount(self.cell_node.flatten(), weights=ang.flatten())
        self.weights = ang / ang_sum[self.cell_node]

    def __prepare_tri_index__(self):
        """Command to prepare cell and node indices of a triangular element mesh (splits quadrilateral elements)"""

        rep_mat = self.is_quad + 1

        tri_cell_node = self.cell_node.repeat(rep_mat, axis=0)
        tri_cell_index = np.arange(0, self.nc2).repeat(rep_mat)

        rep_index = np.where(tri_cell_index[:-1] == tri_cell_index[1:])[0]
        rep_index.shape = (rep_index.size, 1)

        tri_cell_node[rep_index + 1, [0, 1, 2]] = tri_cell_node[rep_index, [2, 3, 0]]

        self.tri_cell_node = tri_cell_node[:, 0:3]
        self.tri_cell_index = tri_cell_index

    def get_intersection_data(self, polyline):
        """
        Query to extract data for intersections(x) of a polyline and the mesh half-edges

        Arguments
        ---------
        :param polyline -- 2D array | Polyline as [x, y] which intersects mesh half-edges.

        Returns
        -------
        :return (x, y, ii) -- tuple | Intersection(x) data defined by coordinates & mesh cell index

        Examples
        --------
        >> polyline = np.array([[0, 0], [10, 10]])
        >> x, y, ii = mesh.get_intersection_data(polyline)
        """

        # Basic preparation of data (avoids precision errors)
        polyline = np.array(polyline).astype(np.float64)

        # Prepare mesh segments as (x, y)
        c = (self.node_x[self.edge_node[0]], self.node_y[self.edge_node[0]])
        d = (self.node_x[self.edge_node[1]], self.node_y[self.edge_node[1]])

        # Prepare data to be returned  as tuple (x, y, cc)
        tup = (polyline[0, 0], polyline[0, 1], np.array([], dtype=np.int32))

        # Loop through each polyline segment
        ns = polyline.shape[0] - 1
        for ii in range(ns):
            # Get polyline segment intersections for segment ii
            a_ii, b_ii = tuple(polyline[ii]), tuple(polyline[ii + 1])
            t, u, lc, rc, lgi = get_intersection(a_ii, b_ii, c, d)

            # Index cell crossing parameters based on valid intersections
            t, u, lc, rc, cc = tuple(v[lgi] for v in (t, u, lc, rc, self.edge_node[2]))

            # Find index of null intersections (hits node)
            sort = np.lexsort((lc, t, cc,))
            node = sort[(u[sort] == 0) | (u[sort] == 1)]
            is_cell = cc[node][:-1] == cc[node][1:]
            is_space = t[node][:-1] != t[node][1:]
            keep = np.where(is_cell & is_space)[0]
            node = np.delete(node, np.hstack((keep, keep + 1)))

            # Remove null intersections
            t, lc, rc, cc = tuple(np.delete(v, node) for v in (t, lc, rc, cc))

            # Check number of valid intersections
            if t.size == 0:
                continue

            # Sort based on normalized distance along polyline AB
            sort = np.lexsort((cc, lc, t,))
            t, lc, rc, cc = tuple(v[sort] for v in (t, lc, rc, cc))

            # Further check for nodal intersections
            node = np.where((lc[:-1] & lc[1:]) | (rc[:-1] & rc[1:]))
            t, lc, rc, cc = tuple(np.delete(v, node) for v in (t, lc, rc, cc))

            # Find null cells
            null = np.where(((t[:-1] != t[1:]) & lc[1:]))[0] + 1
            null = np.insert(null, range(null.size), null)

            # Get cell indices
            cc = np.insert(cc, null, -999)
            if lc[0]:
                cc = np.insert(cc, 0, [-999, -999])
            else:
                cc = np.insert(cc, 0, cc[0])
            if rc[-1]:
                cc = np.insert(cc, cc.size, [-999, -999])
            else:
                cc = np.insert(cc, cc.size, cc[-1])
            cc = cc[range(0, cc.size, 2)]

            # Get unique edges between cells
            t = np.unique(t)
            x = a_ii[0] + t * (b_ii[0] - a_ii[0])
            y = a_ii[1] + t * (b_ii[1] - a_ii[1])

            # Add the  last points of the polyline
            x = np.insert(x, x.size, b_ii[0])
            y = np.insert(y, y.size, b_ii[1])

            # Concatenate data
            tup = tuple(np.hstack((tup[ii], arr)) for ii, arr in enumerate((x, y, cc)))

        return tup

    def get_grid_index(self, grid_x, grid_y):
        """
        Query to extract the mesh cell indices of each point in a grid

        Arguments
        ---------
        :param grid_x -- 1D array | Horizontal grid point values
        :param grid_y -- 1D array | Vertical grid point values

        Returns
        -------
        :return grid_index -- 2D array | Mesh cell index for each point in grid

        Examples
        --------
        >> xlim = [mesh.node_x.min(), mesh.node_x.max()]
        >> ylim = [mesh.node_y.min(), mesh.node_y.max()]
        >> grid_x = np.linspace(xlim[0], xlim[1], 100)
        >> grid_y = np.linspace(ylim[0], ylim[1], 100)
        >> index = mesh.get_grid_index(grid_x, grid_y)
        """

        # Basic preparation of data (avoids precision errors)
        nx, ny = grid_x.size, grid_y.size
        grid_x = np.round(np.array(grid_x), 8).astype(np.float64)
        grid_y = np.round(np.array(grid_y), 8).astype(np.float64)

        # Prepare mesh segments as (x, y)
        c = (self.node_x[self.edge_node[0]], self.node_y[self.edge_node[0]])
        d = (self.node_x[self.edge_node[1]], self.node_y[self.edge_node[1]])

        # Segment dy for narrowing search
        dy = np.max(np.abs(d[1] - c[1]))

        # Declare mesh cell index array
        grid_index = np.zeros((ny, nx), dtype=np.int32) - 999

        # Loop through horizontal grid lines
        for ii in range(ny):
            a_ii, b_ii = (grid_x[0], grid_y[ii]), (grid_x[-1], grid_y[ii])

            # Get logical index of mesh segments in zone
            in_zone = (d[1] < (a_ii[1] + dy)) & (d[1] > (a_ii[1] - dy))

            # Filter mesh segments based on logical index
            c_ii = (c[0][in_zone], c[1][in_zone])
            d_ii = (d[0][in_zone], d[1][in_zone])

            # Get polyline segment intersections for horizontal ray
            t, u, lc, rc, lgi = get_intersection(a_ii, b_ii, c_ii, d_ii)

            # Index cell crossing parameters based on valid intersections
            t, u, lc, rc, cc = tuple(v[lgi] for v in (t, u, lc, rc, self.edge_node[2][in_zone]))

            # Find index of null intersections (hits node)
            sort = np.lexsort((lc, t, cc,))
            node = sort[(u[sort] == 0) | (u[sort] == 1)]
            is_cell = cc[node][:-1] == cc[node][1:]
            is_space = t[node][:-1] != t[node][1:]
            keep = np.where(is_cell & is_space)[0]
            node = np.delete(node, np.hstack((keep, keep + 1)))

            # Remove null intersections
            t, lc, rc, cc = tuple(np.delete(v, node) for v in (t, lc, rc, cc))

            # Check number of valid intersections
            if t.size == 0:
                continue

            # Sort based on normalized distance along polyline AB
            sort = np.lexsort((cc, lc, t,))
            t, lc, rc, cc = tuple(v[sort] for v in (t, lc, rc, cc))

            # Further check for nodal intersections
            node = np.where((lc[:-1] & lc[1:]) | (rc[:-1] & rc[1:]))
            t, lc, rc, cc = tuple(np.delete(v, node) for v in (t, lc, rc, cc))

            # Find null cells
            null = np.where(((t[:-1] != t[1:]) & lc[1:]))[0] + 1
            null = np.insert(null, range(null.size), null)

            # Get cell indices
            cc = np.insert(cc, null, -999)
            if lc[0]:
                cc = np.insert(cc, 0, [-999, -999])
            else:
                cc = np.insert(cc, 0, cc[0])
            if rc[-1]:
                cc = np.insert(cc, cc.size, [-999, -999])
            else:
                cc = np.insert(cc, cc.size, cc[-1])
            cc = cc[range(0, cc.size, 2)]

            # Get unique edges between cells
            xi = a_ii[0] + np.unique(t) * (b_ii[0] - a_ii[0])

            # Add the first & last points of the polyline
            xi = np.insert(xi, [0, xi.size], [a_ii[0], b_ii[0]])

            # Find cell index based on xe(ii) < xm < xe(ii+1)
            xm = np.tile(grid_x, (cc.size, 1)).transpose()
            xe = np.tile(xi, (nx, 1))

            index = np.where((xe[:, :-1] < xm) & (xm < xe[:, 1:]))

            grid_index[ii, index[0]] = cc[index[1]]

        return grid_index

    def get_cell_index(self, xp, yp):
        """
        Query to extract the mesh cell indices of scatter points

        Arguments
        ---------
        :param xp -- 1D array | X coordinate of scatter data
        :param yp -- 1D array | Y coordinate of scatter data

        Returns
        -------
        :return index -- 1D array | Mesh cell index for each scatter point

        Examples
        --------
        >> xlim = [mesh.node_x.min(), mesh.node_x.max()]
        >> ylim = [mesh.node_y.min(), mesh.node_y.max()]
        >> xp = np.random(0, 1, 100)*np.diff(xlim) - xlim[0]
        >> yp = np.random(0, 1, 100)*np.diff(ylim) - ylim[0]
        >> index = mesh.get_cell_index(xp, yp)
        """

        node_x = np.array(self.node_x).astype(np.float64)
        node_y = np.array(self.node_y).astype(np.float64)
        xp = np.array(xp, ndmin=1).astype(np.float64)
        yp = np.array(yp, ndmin=1).astype(np.float64)

        xp, yp = np.round(xp, 8), np.round(yp, 8)

        a = (node_x[self.tri_cell_node[:, 0]], node_y[self.tri_cell_node[:, 0]])
        b = (node_x[self.tri_cell_node[:, 1]], node_y[self.tri_cell_node[:, 1]])
        c = (node_x[self.tri_cell_node[:, 2]], node_y[self.tri_cell_node[:, 2]])

        index = np.zeros(xp.size, dtype=np.int32) - 999
        for aa in range(xp.size):
            p = (xp[aa], yp[aa])
            ccw = \
                (
                    is_ccw(p, a, b),
                    is_ccw(p, b, c),
                    is_ccw(p, c, a)
                )
            ii = np.where(np.all(ccw, axis=0))[0]

            if ii.size == 0:
                continue
            elif ii.size == 1:
                index[aa] = ii

        index[index != -999] = self.tri_cell_index[index[index != -999]]

        return index

    def get_barycentric_weights(self, xp, yp, cell_index=None):
        pass
