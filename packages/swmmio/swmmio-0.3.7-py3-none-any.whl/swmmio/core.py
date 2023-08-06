#!/usr/bin/env python
# coding:utf-8
import re
from time import ctime
import pandas as pd
import glob
import math
from swmmio.utils import spatial
from swmmio.utils import functions
from swmmio.utils.dataframes import create_dataframeINP, create_dataframeRPT, get_link_coords, \
    create_dataframe_multi_index
from swmmio.defs.config import *
from swmmio.tests.data import MODEL_FULL_FEATURES__NET_PATH, MODEL_FULL_FEATURES_XY
import warnings
import swmmio
from swmmio.elements import ModelSection
from swmmio.defs import HEADERS
# from swmmio.utils.functions import find_invalid_links
from swmmio.utils.functions import trim_section_to_nodes


class Model(object):

    def __init__(self, in_file_path, crs=None):
        """
        Class representing a complete SWMM model incorporating its INP and RPT
        files and data

        initialize a swmmio.Model object by pointing it to a directory containing
        a single INP (and optionally an RPT file with matching filename) or by
        pointing it directly to an .inp file.
        """
        self.crs = None
        inp_path = None
        if os.path.isdir(in_file_path):
            # a directory was passed in
            inps_in_dir = glob.glob1(in_file_path, "*.inp")
            if len(inps_in_dir) == 1:
                # there is only one INP in this directory -> good.
                inp_path = os.path.join(in_file_path, inps_in_dir[0])

        elif os.path.splitext(in_file_path)[1] == '.inp':
            # an inp was passed in
            inp_path = in_file_path

        if inp_path:
            wd = os.path.dirname(inp_path)  # working dir
            name = os.path.splitext(os.path.basename(inp_path))[0]
            self.name = name
            self.inp = inp(inp_path)  # inp object
            self.rpt = None  # until we can confirm it initializes properly
            self.bbox = None  # to remember how the model data was clipped
            self.scenario = ''  # self._get_scenario()
            self.crs = crs  # coordinate reference system

            # try to initialize a companion RPT object
            rpt_path = os.path.join(wd, name + '.rpt')
            if os.path.exists(rpt_path):
                try:
                    self.rpt = rpt(rpt_path)
                except Exception as e:
                    print('{}.rpt failed to initialize\n{}'.format(name, e))

            self._nodes_df = None
            self._conduits_df = None
            self._orifices_df = None
            self._weirs_df = None
            self._pumps_df = None
            self._links_df = None
            self._subcatchments_df = None
            self._network = None

    def rpt_is_valid(self, verbose=False):
        """
        Return true if the .rpt file exists and has a revision date more
        recent than the .inp file. If the inp has an modified date later than
        the rpt, assume that the rpt should be regenerated
        """

        if self.rpt is None:
            if verbose:
                print('{} does not have an rpt file'.format(self.name))
            return False

        # check if the rpt has ERRORS output from SWMM
        with open(self.rpt.path) as f:
            # jump to 500 bytes before the end of file
            f.seek(self.rpt.file_size - 500)
            for line in f:
                spl = line.split()
                if len(spl) > 0 and spl[0] == 'ERROR':
                    # return false at first "ERROR" occurence
                    return False

        rpt_mod_time = os.path.getmtime(self.rpt.path)
        inp_mod_time = os.path.getmtime(self.inp.path)

        if verbose:
            print("{}.rpt: modified {}".format(self.name, ctime(rpt_mod_time)))
            print("{}.inp: modified {}".format(self.name, ctime(inp_mod_time)))

        if inp_mod_time > rpt_mod_time:
            # inp datetime modified greater than rpt datetime modified
            return False
        else:
            return True

    def to_map(self, filename=None, inproj='epsg:2272'):
        '''
        To be removed in v0.4.0. Use swmmio.reporting.visualize.create_map()
        '''

        def wrn():
            w = '''to_map is no longer supported! Use
            swmmio.reporting.visualize.create_map() instead'''
            warnings.warn(w, DeprecationWarning)

        with warnings.catch_warnings():
            warnings.simplefilter("always")
            wrn()

    def conduits(self):
        """
        collect all useful and available data related model conduits and
        organize in one dataframe.
        """

        # check if this has been done already and return that data accordingly
        if self._conduits_df is not None:
            return self._conduits_df

        # parse out the main objects of this model
        inp = self.inp
        rpt = self.rpt

        # create dataframes of relevant sections from the INP
        conduits_df = create_dataframeINP(inp.path, "[CONDUITS]", comment_cols=False)
        xsections_df = create_dataframeINP(inp.path, "[XSECTIONS]", comment_cols=False)
        conduits_df = conduits_df.join(xsections_df)

        if rpt:
            # create a dictionary holding data from an rpt file, if provided
            link_flow_df = create_dataframeRPT(rpt.path, "Link Flow Summary")
            conduits_df = conduits_df.join(link_flow_df)

        # add conduit coordinates
        xys = conduits_df.apply(lambda r: get_link_coords(r, self.inp.coordinates, self.inp.vertices), axis=1)
        df = conduits_df.assign(coords=xys.map(lambda x: x[0]))

        # add conduit up/down inverts and calculate slope
        elevs = self.nodes()[['InvertElev']]
        df = pd.merge(df, elevs, left_on='InletNode', right_index=True, how='left')
        df = df.rename(index=str, columns={"InvertElev": "InletNodeInvert"})
        df = pd.merge(df, elevs, left_on='OutletNode', right_index=True, how='left')
        df = df.rename(index=str, columns={"InvertElev": "OutletNodeInvert"})
        df['UpstreamInvert'] = df.InletNodeInvert + df.InletOffset
        df['DownstreamInvert'] = df.OutletNodeInvert + df.OutletOffset
        df['SlopeFtPerFt'] = (df.UpstreamInvert - df.DownstreamInvert) / df.Length

        df.InletNode = df.InletNode.astype(str)
        df.OutletNode = df.OutletNode.astype(str)

        self._conduits_df = df

        return df

    @property
    def orifices(self):
        """
        collect all useful and available data related model orifices and
        organize in one dataframe.
        """

        df = ModelSection(self, 'orifices')
        self._orifices_df = df

        return df

    def weirs(self):
        """
        collect all useful and available data related model weirs and
        organize in one dataframe.
        """

        # check if this has been done already and return that data accordingly
        if self._weirs_df is not None:
            return self._weirs_df

        # parse out the main objects of this model
        inp = self.inp
        rpt = self.rpt

        # create dataframes of relevant sections from the INP
        weirs_df = create_dataframeINP(inp.path, "[WEIRS]")
        if weirs_df.empty:
            return pd.DataFrame()

        weirs_df = weirs_df[['InletNode', 'OutletNode', 'WeirType', 'CrestHeight']]

        # add conduit coordinates
        xys = weirs_df.apply(lambda r: get_link_coords(r, self.inp.coordinates, self.inp.vertices), axis=1)
        df = weirs_df.assign(coords=xys.map(lambda x: x[0]))
        df.InletNode = df.InletNode.astype(str)
        df.OutletNode = df.OutletNode.astype(str)

        self._weirs_df = df

        return df

    @property
    def pumps(self):

        """
        collect all useful and available data related model pumps and
        organize in one dataframe.
        >>> import swmmio
        >>> from swmmio.tests.data import MODEL_FULL_FEATURES_XY
        >>> model = swmmio.Model(MODEL_FULL_FEATURES_XY)
        >>> pumps = model.pumps()
        >>> pumps[['PumpCurve', 'InitStatus']]
             PumpCurve InitStatus
        Name
        C2    P1_Curve         ON
        >>> pumps = model.pumps.to_gdf()
        >>> pumps
        """

        pumps_df = ModelSection(self, 'pumps')
        self._pumps_df = pumps_df

        return pumps_df

    def links(self):
        """
        create a DataFrame containing all link objects in the model including
        conduits, pumps, weirs, and orifices.
        :return: dataframe containing all link objects in the model
        """
        if self._links_df is not None:
            return self._links_df

        df = pd.concat([self.conduits(), self.orifices(), self.weirs(), self.pumps()], sort=True)
        df['facilityid'] = df.index
        self._links_df = df
        return df

    def nodes(self, bbox=None, subset=None):
        """
        collect all useful and available data related model nodes and organize
        in one dataframe.
        """

        # check if this has been done already and return that data accordingly
        if self._nodes_df is not None and bbox == self.bbox:
            return self._nodes_df

        # parse out the main objects of this model
        inp = self.inp
        rpt = self.rpt

        # create dataframes of relevant sections from the INP
        juncs_df = create_dataframeINP(inp.path, "[JUNCTIONS]")
        outfalls_df = create_dataframeINP(inp.path, "[OUTFALLS]")
        storage_df = create_dataframeINP(inp.path, "[STORAGE]")

        # concatenate the DFs and keep only relevant cols
        all_nodes = pd.concat([juncs_df, outfalls_df, storage_df], sort=True)
        cols = ['InvertElev', 'MaxDepth', 'SurchargeDepth', 'PondedArea']
        all_nodes = all_nodes[cols]

        if rpt:
            # add results data if a rpt file was found
            depth_summ = create_dataframeRPT(rpt.path, "Node Depth Summary")
            flood_summ = create_dataframeRPT(rpt.path, "Node Flooding Summary")

            # join the rpt data (index on depth df, suffixes for common cols)
            rpt_df = depth_summ.join(
                flood_summ, lsuffix='_depth', rsuffix='_flood')
            all_nodes = all_nodes.join(rpt_df)  # join to the all_nodes df

        all_nodes = all_nodes.join(self.inp.coordinates[['X', 'Y']])

        def nodexy(row):
            if math.isnan(row.X) or math.isnan(row.Y):
                return None
            else:
                return [(row.X, row.Y)]

        xys = all_nodes.apply(lambda r: nodexy(r), axis=1)
        all_nodes = all_nodes.assign(coords=xys)
        all_nodes = all_nodes.rename(index=str)
        self._nodes_df = all_nodes

        return all_nodes

    def subcatchments(self):
        """
        collect all useful and available data related subcatchments and organize
        in one dataframe.
        """
        subs = create_dataframeINP(self.inp.path, "[SUBCATCHMENTS]")
        subs = subs.drop([';', 'Comment', 'Origin'], axis=1)
        polygons_df = self.inp.polygons

        if self.rpt:
            flw = create_dataframeRPT(
                self.rpt.path, 'Subcatchment Runoff Summary')
            subs = subs.join(flw)

            # more accurate runoff calculations
            subs['RunoffAcFt'] = subs.TotalRunoffIn / 12.0 * subs.Area
            subs['RunoffMGAccurate'] = subs.RunoffAcFt / 3.06888785

        self._subcatchments_df = subs

        return subs

    def node(self, node, conduit=None):
        '''
        To be removed in v0.4.0
        '''

        def wrn():
            w = "Depreciated. Use model.nodes().loc['{}'] instead".format(node)
            warnings.warn(w, DeprecationWarning)
            return self.nodes().loc[node]

        with warnings.catch_warnings():
            warnings.simplefilter("always")
            wrn()

    @property
    def network(self):
        """
        Networkx MultiDiGraph representation of the model
        :return: Networkx MultiDiGraph representation of model
        :rtype: networkx.MultiDiGraph
        """

        if self._network is None:
            G = functions.model_to_networkx(self, drop_cycles=False)
            self._network = G

        return self._network

    def to_crs(self, *args, **kwargs):
        """
        Convert coordinate reference system of the model coordinates
        :param target_crs:
        :return: True
        Example:
        >>> import swmmio
        >>> m = swmmio.Model(MODEL_FULL_FEATURES_XY, crs="+init=EPSG:2272")
        >>> m.to_crs("+init=EPSG:4326") # convert to WGS84 web mercator
        >>> m.inp.coordinates
                      X          Y
        Name
        J3   -74.866424  42.365958
        1    -74.870614  42.368292
        2    -74.867615  42.367916
        3    -74.869387  42.368527
        4    -74.869024  42.368089
        5    -74.868888  42.367709
        J2   -74.868458  42.366748
        J4   -74.864787  42.365966
        J1   -74.868861  42.366968
        >>> m.inp.vertices
                       X          Y
        Name
        C1:C2 -74.868703  42.366833
        C2.1  -74.868034  42.366271
        C2.1  -74.867305  42.365974
        """
        try:
            import pyproj
        except ImportError:
            raise ImportError('pyproj module needed. get this package here: ',
                              'https://pypi.python.org/pypi/pyproj')

        if self.crs is None:
            raise AttributeError('CRS of model object not set')

        if not self.inp.coordinates.empty:
            self.inp.coordinates = spatial.change_crs(self.inp.coordinates, self.crs, *args, **kwargs)

        if not self.inp.vertices.empty:
            self.inp.vertices = spatial.change_crs(self.inp.vertices, self.crs, *args, **kwargs)

        if not self.inp.polygons.empty:
            self.inp.polygons = spatial.change_crs(self.inp.polygons, self.crs, *args, **kwargs)

        self.crs = args[0]

    def to_geojson(self, target_path=None):
        """
        Return a GeoJSON representation of the entire model
        :param target_path: target path of geojson (optional)
        :return: GeoJSON representation of model
        """
        raise NotImplementedError

    def export_to_shapefile(self, shpdir, prj=None):
        """
        export the model data into a shapefile. element_type dictates which type
        of data will be included.

        default projection is PA State Plane - untested on other cases
        """

        # CREATE THE CONDUIT shp
        conds = self.conduits()
        conds_path = os.path.join(shpdir, self.inp.name + '_conduits.shp')
        spatial.write_shapefile(conds, conds_path, prj=prj)

        # CREATE THE NODE shp
        nodes = self.nodes()
        nodes_path = os.path.join(shpdir, self.inp.name + '_nodes.shp')
        spatial.write_shapefile(nodes, nodes_path, geomtype='point', prj=prj)


class SWMMIOFile(object):
    defaultSection = "Link Flow Summary"

    def __init__(self, file_path):

        # file name and path variables
        self.path = file_path
        self.name = os.path.splitext(os.path.basename(file_path))[0]
        self.dir = os.path.dirname(file_path)
        self.file_size = os.path.getsize(file_path)

    def findByteRangeOfSection(self, startStr):
        '''
        returns the start and end "byte" location of substrings in a text file
        '''

        with open(self.path) as f:
            start = None
            end = None
            l = 0  # line bytes index
            for line in f:

                if start and line.strip() == "" and (l - start) > 100:
                    # LOGIC: if start exists (was found) and the current line
                    # length is 3 or less (length of /n ) and we're more than
                    # 100 bytes from the start location then we are at the first
                    # "blank" line after our start section (aka the end of the
                    # section)
                    end = l
                    break

                if (startStr in line) and (not start):
                    start = l

                # increment length (bytes?) of current position
                l += len(line) + len("\n")

        return [start, end]


class rpt(SWMMIOFile):
    '''
    An accessible SWMM .rpt object
    '''

    def __init__(self, filePath):

        SWMMIOFile.__init__(self, filePath)

        with open(filePath) as f:
            for line in f:
                if "Starting Date" in line:
                    simulationStart = line.split(".. ")[1].replace("\n", "")
                if "Ending Date" in line:
                    simulationEnd = line.split(".. ")[1].replace("\n", "")
                if "Report Time Step ........." in line:
                    timeStepMin = int(line.split(":")[1].replace("\n", ""))
                    break

        self.simulationStart = simulationStart
        self.simulationEnd = simulationEnd
        self.timeStepMin = timeStepMin

        # grab the date of analysis
        with open(filePath) as f:
            f.seek(self.file_size - 500)  # jump to 500 bytes before the end of file
            for line in f:
                if "Analysis begun on" in line:
                    date = line.split("Analysis begun on:  ")[1].replace("\n", "")

        self.dateOfAnalysis = date
        self.elementByteLocations = {"Link Results": {}, "Node Results": {}}

    def returnDataAtDTime(self, id, dtime, sectionTitle="Link Results", startByte=0):
        '''
        return data from time series in RPT file
        '''

        byteLocDict = self.elementByteLocations[sectionTitle]
        if byteLocDict:
            startByte = byteLocDict[id]

        elif startByte == 0:
            startByte = self.findByteRangeOfSection(sectionTitle)[0]
            print('startByte ' + str(startByte))

        with open(self.path) as f:

            f.seek(startByte)  # jump to general area of file if we know it
            subsectionFound = False

            for line in f:
                if id in line: subsectionFound = True

                if subsectionFound and dtime in line:
                    line = ' '.join(re.findall('\"[^\"]*\"|\S+', line))
                    rowdata = line.replace("\n", "").split(" ")
                    return rowdata


class inp(SWMMIOFile):

    # creates an accessible SWMM .inp object
    # make sure INP has been saved in the GUI before using this

    def __init__(self, file_path):
        self._options_df = None
        self._files_df = None
        self._conduits_df = None
        self._xsections_df = None
        self._pumps_df = None
        self._orifices_df = None
        self._weirs_df = None
        self._junctions_df = None
        self._outfalls_df = None
        self._storage_df = None
        self._coordinates_df = None
        self._vertices_df = None
        self._polygons_df = None
        self._subcatchments_df = None
        self._subareas_df = None
        self._infiltration_df = None
        self._headers = None
        self._curves_df = None

        SWMMIOFile.__init__(self, file_path)  # run the superclass init

        self._sections = [
                '[OPTIONS]',
                '[FILES]',
                '[CONDUITS]',
                '[XSECTIONS]',
                '[PUMPS]',
                '[ORIFICES]',
                '[WEIRS]',
                '[JUNCTIONS]',
                '[STORAGE]',
                '[OUTFALLS]',
                '[VERTICES]',
                '[SUBCATCHMENTS]',
                '[SUBAREAS]',
                '[INFILTRATION]',
                '[COORDINATES]'
                '[CURVES]'
            ]

    def save(self, target_path=None):
        '''
        Save the inp file to disk. File will be overwritten unless a target_path
        is provided
        '''
        from swmmio.utils.modify_model import replace_inp_section
        import shutil
        target_path = target_path if target_path is not None else self.path

        shutil.copyfile(self.path, target_path)
        for section in self._sections:
            # reformate the [SECTION] to section (and _section_df)
            sect_id = section.translate({ord(i): None for i in '[]'}).lower()
            sect_id_private = '_{}_df'.format(sect_id)
            data = getattr(self, sect_id_private)
            if data is not None:
                replace_inp_section(target_path, section, data)

    def validate(self):
        """
        Detect and remove invalid model elements
        :return: None
        """
        drop_invalid_model_elements(self)

    def trim_to_nodes(self, node_ids):

        for section in ['junctions', 'storage', 'outfalls', 'coordinates']:
            trim_section_to_nodes(self, node_ids, node_type=section)

    @property
    def headers(self):
        """
        Get the proper section headers for the INP file.
        """
        if self._headers is None:

            infil_type = self.options.loc['INFILTRATION', 'Value']
            infil_cols = HEADERS['infiltration_cols'][infil_type]

            # overwrite the dynamic sections with proper header cols
            h = dict(HEADERS['inp_sections'])
            h['[INFILTRATION]'] = list(infil_cols)
            self._headers = h

        else:
            return self._headers

    @property
    def options(self):
        """
        Get/set options section of the INP file.

        :return: options section of the INP file
        :rtype: pandas.DataFrame

        Examples:
        """
        if self._options_df is None:
            self._options_df = create_dataframeINP(self.path, "[OPTIONS]", comment_cols=False,
                                                   headers=self._headers)
        return self._options_df

    @options.setter
    def options(self, df):
        """Set inp.options DataFrame."""
        self._options_df = df

        # update the headers
        infil_type = df.loc['INFILTRATION', 'Value']
        infil_cols = HEADERS['infiltration_cols'][infil_type]

        # overwrite the dynamic sections with proper header cols
        h = dict(HEADERS['inp_sections'])
        h['[INFILTRATION]'] = list(infil_cols)
        self._headers = h
        self._infiltration_df = None

    @property
    def files(self):
        """
        Get/set files section of the INP file.

        :return: files section of the INP file
        :rtype: pandas.DataFrame

        Examples:
        """
        if self._files_df is None:
            self._files_df = create_dataframeINP(self.path, "[FILES]", comment_cols=False)
        return self._files_df.reset_index()

    @files.setter
    def files(self, df):
        """Set inp.files DataFrame."""
        first_col = df.columns[0]
        self._files_df = df.set_index(first_col)

    @property
    def conduits(self):
        """
        Get/set conduits section of the INP file.

        :return: Conduits section of the INP file
        :rtype: pandas.DataFrame

        Examples:

        >>> import swmmio
        >>> from swmmio.tests.data import MODEL_FULL_FEATURES__NET_PATH
        >>> model = swmmio.Model(MODEL_FULL_FEATURES__NET_PATH)
        >>> model.inp.conduits[['InletNode', 'OutletNode', 'Length', 'ManningN']]
              InletNode OutletNode  Length  ManningN
        Name
        C1:C2        J1         J2  244.63      0.01
        C2.1         J2         J3  666.00      0.01
        1             1          4  400.00      0.01
        2             4          5  400.00      0.01
        3             5         J1  400.00      0.01
        4             3          4  400.00      0.01
        5             2          5  400.00      0.01
        """
        if self._conduits_df is None:
            self._conduits_df = create_dataframeINP(self.path, "[CONDUITS]", comment_cols=False)
        return self._conduits_df

    @conduits.setter
    def conduits(self, df):
        """Set inp.conduits DataFrame."""
        self._conduits_df = df

    @property
    def xsections(self):
        """
        Get/set pumps section of the INP file.
        """
        if self._xsections_df is None:
            self._xsections_df = create_dataframeINP(self.path, "[XSECTIONS]", comment_cols=False)
        return self._xsections_df

    @xsections.setter
    def xsections(self, df):
        """Set inp.xsections DataFrame."""
        self._xsections_df = df

    @property
    def pumps(self):
        """
        Get/set pumps section of the INP file.
        """
        if self._pumps_df is None:
            self._pumps_df = create_dataframeINP(self.path, "[PUMPS]", comment_cols=False)
        return self._pumps_df

    @pumps.setter
    def pumps(self, df):
        """Set inp.pumps DataFrame."""
        self._pumps_df = df

    @property
    def orifices(self):
        """
        Get/set orifices section of the INP file.
        """
        if self._orifices_df is None:
            self._orifices_df = create_dataframeINP(self.path, "[ORIFICES]", comment_cols=False)
        return self._orifices_df

    @orifices.setter
    def orifices(self, df):
        """Set inp.orifices DataFrame."""
        self._orifices_df = df

    @property
    def weirs(self):
        """
        Get/set weirs section of the INP file.
        """
        if self._weirs_df is None:
            self._weirs_df = create_dataframeINP(self.path, "[WEIRS]", comment_cols=False)
        return self._weirs_df

    @weirs.setter
    def weirs(self, df):
        """Set inp.weirs DataFrame."""
        self._weirs_df = df

    @property
    def junctions(self):
        """
        Get/set junctions section of the INP file.

        :return: junctions section of the INP file
        :rtype: pandas.DataFrame

        Examples:

        >>> import swmmio
        >>> from swmmio.tests.data import MODEL_FULL_FEATURES__NET_PATH
        >>> model = swmmio.Model(MODEL_FULL_FEATURES__NET_PATH)
        >>> model.inp.junctions
              InvertElev  MaxDepth  InitDepth  SurchargeDepth  PondedArea
        Name
        J3         6.547        15          0               0           0
        1         17.000         0          0               0           0
        2         17.000         0          0               0           0
        3         16.500         0          0               0           0
        4         16.000         0          0               0           0
        5         15.000         0          0               0           0
        J2        13.000        15          0               0           0
        """
        if self._junctions_df is None:
            self._junctions_df = create_dataframeINP(self.path, "[JUNCTIONS]", comment_cols=False)
        return self._junctions_df

    @junctions.setter
    def junctions(self, df):
        """Set inp.junctions DataFrame."""
        self._junctions_df = df

    @property
    def outfalls(self):
        """
        Get/set outfalls section of the INP file.

        :return: outfalls section of the INP file
        :rtype: pandas.DataFrame

        Examples:

        >>> import swmmio
        >>> from swmmio.tests.data import MODEL_FULL_FEATURES__NET_PATH
        >>> model = swmmio.Model(MODEL_FULL_FEATURES__NET_PATH)
        >>> model.inp.outfalls
              InvertElev OutfallType StageOrTimeseries  TideGate
        Name
        J4             0        FREE                NO       NaN
        """
        if self._outfalls_df is None:
            self._outfalls_df = create_dataframeINP(self.path, "[OUTFALLS]", comment_cols=False)
        return self._outfalls_df

    @outfalls.setter
    def outfalls(self, df):
        """Set inp.outfalls DataFrame."""
        self._outfalls_df = df

    @property
    def storage(self):
        """
        Get/set storage section of the INP file.

        :return: storage section of the INP file
        :rtype: pandas.DataFrame

        Examples:
        """
        if self._storage_df is None:
            self._storage_df = create_dataframeINP(self.path, "[STORAGE]", comment_cols=False)
        return self._storage_df

    @storage.setter
    def storage(self, df):
        """Set inp.storage DataFrame."""
        self._storage_df = df

    @property
    def subcatchments(self):
        """
        Get/set subcatchments section of the INP file.

        :return: subcatchments section of the INP file
        :rtype: pandas.DataFrame

        Examples:
        """
        if self._subcatchments_df is None:
            self._subcatchments_df = create_dataframeINP(self.path, "[SUBCATCHMENTS]", comment_cols=False,
                                                         headers=self._headers)
        return self._subcatchments_df

    @subcatchments.setter
    def subcatchments(self, df):
        """Set inp.subcatchments DataFrame."""
        self._subcatchments_df = df

    @property
    def subareas(self):
        """
        Get/set subareas section of the INP file.
        """
        if self._subareas_df is None:
            self._subareas_df = create_dataframeINP(self.path, "[SUBAREAS]", comment_cols=False,
                                                    headers=self._headers)
        return self._subareas_df

    @subareas.setter
    def subareas(self, df):
        """Set inp.subareas DataFrame."""
        self._subareas_df = df

    @property
    def infiltration(self):
        """
        Get/set infiltration section of the INP file.
        """
        if self._infiltration_df is None:
            self._infiltration_df = create_dataframeINP(self.path, "[INFILTRATION]", comment_cols=False,
                                                        headers=self._headers)
        return self._infiltration_df

    @infiltration.setter
    def infiltration(self, df):
        """Set inp.infiltration DataFrame."""
        self._infiltration_df = df

    @property
    def coordinates(self):
        """
        Get/set coordinates section of model
        :return: dataframe of model coordinates
        """
        if self._coordinates_df is not None:
            return self._coordinates_df
        self._coordinates_df = create_dataframeINP(self.path, "[COORDINATES]", comment_cols=False,
                                                        headers=self._headers)
        return self._coordinates_df

    @coordinates.setter
    def coordinates(self, df):
        """Set inp.coordinates DataFrame."""
        self._coordinates_df = df

    @property
    def vertices(self):
        """
        get/set vertices section of model
        :return: dataframe of model coordinates
        """
        if self._vertices_df is not None:
            return self._vertices_df
        self._vertices_df = create_dataframeINP(self.path, '[VERTICES]', comment_cols=False)
        return self._vertices_df

    @vertices.setter
    def vertices(self, df):
        """Set inp.vertices DataFrame."""
        self._vertices_df = df

    @property
    def polygons(self):
        """
        get/set polygons section of model
        :return: dataframe of model coordinates
        """
        if self._polygons_df is not None:
            return self._polygons_df
        self._polygons_df = create_dataframeINP(self.path, '[Polygons]', comment_cols=False)
        return self._polygons_df

    @polygons.setter
    def polygons(self, df):
        """Set inp.polygons DataFrame."""
        self._curves_df = df

    @property
    def curves(self):
        """
        get/set curves section of model
        :return: multi-index dataframe of model curves
        """
        if self._curves_df is not None:
            return self._curves_df
        self._curves_df = create_dataframe_multi_index(self.path, '[CURVES]', comment_cols=False)
        return self._curves_df

    @curves.setter
    def curves(self, df):
        """Set inp.polygons DataFrame."""
        self._curves_df = df


def drop_invalid_model_elements(inp):
    """
    Identify references to elements in the model that are undefined and remove them from the
    model. These should coincide with warnings/errors produced by SWMM5 when undefined elements
    are referenced in links, subcatchments, and controls.
    :param model: swmmio.Model
    :return:
    >>> import swmmio
    >>> from swmmio.tests.data import MODEL_FULL_FEATURES_INVALID
    >>> m = swmmio.Model(MODEL_FULL_FEATURES_INVALID)
    >>> drop_invalid_model_elements(m.inp)
    ['InvalidLink2', 'InvalidLink1']
    >>> m.inp.conduits.index
    Index(['C1:C2', 'C2.1', '1', '2', '4', '5'], dtype='object', name='Name')
    """
    from swmmio.utils.dataframes import create_dataframeINP
    juncs = create_dataframeINP(inp.path, "[JUNCTIONS]").index.tolist()
    outfs = create_dataframeINP(inp.path, "[OUTFALLS]").index.tolist()
    stors = create_dataframeINP(inp.path, "[STORAGE]").index.tolist()
    nids = juncs + outfs + stors

    # drop links with bad refs to inlet/outlet nodes
    from swmmio.utils.functions import find_invalid_links
    inv_conds = find_invalid_links(inp, nids, 'conduits', drop=True)
    inv_pumps = find_invalid_links(inp, nids, 'pumps', drop=True)
    inv_orifs = find_invalid_links(inp, nids, 'orifices', drop=True)
    inv_weirs = find_invalid_links(inp, nids, 'weirs', drop=True)

    # drop other parts of bad links
    invalid_links = inv_conds + inv_pumps + inv_orifs + inv_weirs
    inp.xsections = inp.xsections.loc[~inp.xsections.index.isin(invalid_links)]

    # drop invalid subcats and their related components
    invalid_subcats = inp.subcatchments.index[~inp.subcatchments['Outlet'].isin(nids)]
    inp.subcatchments = inp.subcatchments.loc[~inp.subcatchments.index.isin(invalid_subcats)]
    inp.subareas = inp.subareas.loc[~inp.subareas.index.isin(invalid_subcats)]
    inp.infiltration = inp.infiltration.loc[~inp.infiltration.index.isin(invalid_subcats)]

    return invalid_links + invalid_subcats