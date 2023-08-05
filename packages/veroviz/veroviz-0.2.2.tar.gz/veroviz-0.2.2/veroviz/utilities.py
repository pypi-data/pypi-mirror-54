from veroviz._common import *
from veroviz._validation import *
from veroviz._geometry import *
from veroviz._internal import *

def convertSpeed(speed, fromUnitsDist, fromUnitsTime, toUnitsDist, toUnitsTime):
	"""
	Convert a speed to different units.

	Parameters
	----------
	speed: float
		The numeric value describing a speed to be converted.
	fromUnitsDist: string
		Distance units for the given speed, before conversion. See :ref:`Units` for options.
	fromUnitsTime: string
		Time units for the given speed, before conversion. See :ref:`Units` for options.
	toUnitsDist: string
		Distance units for the speed after conversion. See :ref:`Units` for options.
	toUnitTime: string
		Time units for the speed after conversion. See :ref:`Units` for options.
	
	Returns
	-------
	float
		Speed after conversion

	Example
	-------
		>>> import veroviz as vrv
		>>> speedFPS = 10
		>>> speedMPH = vrv.convertSpeed(speedFPS, 'ft', 's', 'mi', 'h')
		>>> speedMPH
		6.818198764711	
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valConvertSpeed(speed, fromUnitsDist, fromUnitsTime, toUnitsDist, toUnitsTime)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)
	
	try:
		fromUnitsDist = fromUnitsDist.lower()
	except:
		pass
	
	fromUnitsDist = distanceUnitsDictionary[fromUnitsDist]
	if (fromUnitsDist == 'm'):
		tmpSpeed = speed * 1.0
	elif (fromUnitsDist == 'km'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_KILOMETER
	elif (fromUnitsDist == 'mi'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_MILE
	elif (fromUnitsDist == 'ft'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_FEET
	elif (fromUnitsDist == 'yard'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_YARD
	elif (fromUnitsDist == 'nmi'):
		tmpSpeed = speed * VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		fromUnitsTime = fromUnitsTime.lower()
	except:
		pass

	fromUnitsTime = timeUnitsDictionary[fromUnitsTime]
	if (fromUnitsTime == 's'):
		tmpSpeed = tmpSpeed / 1.0
	elif (fromUnitsTime == 'min'):
		tmpSpeed = tmpSpeed / VRV_CONST_SECONDS_PER_MINUTE
	elif (fromUnitsTime == 'h'):
		tmpSpeed = tmpSpeed / VRV_CONST_SECONDS_PER_HOUR

	try:
		toUnitsDist = toUnitsDist.lower()
	except:
		pass

	toUnitsDist = distanceUnitsDictionary[toUnitsDist]
	if (toUnitsDist == 'm'):
		tmpSpeed = tmpSpeed / 1.0
	elif (toUnitsDist == 'km'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_KILOMETER
	elif (toUnitsDist == 'mi'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_MILE
	elif (toUnitsDist == 'ft'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_FEET
	elif (toUnitsDist == 'yard'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_YARD
	elif (toUnitsDist == 'nmi'):
		tmpSpeed = tmpSpeed / VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		toUnitsTime = toUnitsTime.lower()
	except:
		pass

	toUnitsTime = timeUnitsDictionary[toUnitsTime]
	if (toUnitsTime == 's'):
		convSpeed = tmpSpeed * 1.0
	elif (toUnitsTime == 'min'):
		convSpeed = tmpSpeed * VRV_CONST_SECONDS_PER_MINUTE
	elif (toUnitsTime == 'h'):
		convSpeed = tmpSpeed * VRV_CONST_SECONDS_PER_HOUR

	return convSpeed

def convertDistance(distance, fromUnits, toUnits):
	"""
	Convert a distance to different units.

	Parameters
	----------
	distance: float
		The numeric value describing a distance to be converted.
	fromUnits: string
		Distance units before conversion. See :ref:`Units` for options.
	toUnits: string
		Distance units after conversion. See :ref:`Units` for options.

	Returns
	-------
	float
		Distance after conversion

	Example
	-------
	    >>> import veroviz as vrv
	    >>> distanceMiles = 1.0
	    >>> distanceKilometers = vrv.convertDistance(distanceMiles, 'miles', 'km')
	    >>> distanceKilometers
	    1.60934

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valConvertDistance(distance, fromUnits, toUnits)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		fromUnits = fromUnits.lower()
	except:
		pass

	fromUnits = distanceUnitsDictionary[fromUnits]
	if (fromUnits == 'm'):
		tmpDist = distance * 1.0
	elif (fromUnits == 'km'):
		tmpDist = distance * VRV_CONST_METERS_PER_KILOMETER
	elif (fromUnits == 'mi'):
		tmpDist = distance * VRV_CONST_METERS_PER_MILE
	elif (fromUnits == 'ft'):
		tmpDist = distance * VRV_CONST_METERS_PER_FEET
	elif (fromUnits == 'yard'):
		tmpDist = distance * VRV_CONST_METERS_PER_YARD
	elif (fromUnits == 'nmi'):
		tmpDist = distance * VRV_CONST_METERS_PER_NAUTICAL_MILE

	try:
		toUnits = toUnits.lower()
	except:
		pass
		
	toUnits = distanceUnitsDictionary[toUnits]
	if (toUnits == 'm'):
		convDist = tmpDist / 1.0
	elif (toUnits == 'km'):
		convDist = tmpDist / VRV_CONST_METERS_PER_KILOMETER
	elif (toUnits == 'mi'):
		convDist = tmpDist / VRV_CONST_METERS_PER_MILE
	elif (toUnits == 'ft'):
		convDist = tmpDist / VRV_CONST_METERS_PER_FEET
	elif (toUnits == 'yard'):
		convDist = tmpDist / VRV_CONST_METERS_PER_YARD
	elif (toUnits == 'nmi'):
		convDist = tmpDist / VRV_CONST_METERS_PER_NAUTICAL_MILE

	return convDist

def convertTime(time, fromUnits, toUnits):
	"""
	Convert a time to different units.

	Parameters
	----------
	time: float
		The numeric value describing a time to be converted.
	fromUnits: string
		Time units before conversion. See :ref:`Units` for options.
	toUnits: string
		Time units after conversion. See :ref:`Units` for options.

	Returns
	-------
	float
		Time after conversion

	Example
	-------
	    >>> import veroviz as vrv
	    >>> timeHours = 1.5
	    >>> timeMinutes = vrv.convertTime(timeHours, 'h', 'min')
	    >>> timeMinutes
	    90.0

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valConvertTime(time, fromUnits, toUnits)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		fromUnits = fromUnits.lower()
	except:
		pass
		
	fromUnits = timeUnitsDictionary[fromUnits]
	if (fromUnits == 's'):
		tmpTime = time * 1.0
	elif (fromUnits == 'min'):
		tmpTime = time * VRV_CONST_SECONDS_PER_MINUTE
	elif (fromUnits == 'h'):
		tmpTime = time * VRV_CONST_SECONDS_PER_HOUR

	try:
		toUnits = toUnits.lower()
	except:
		pass
		
	toUnits = timeUnitsDictionary[toUnits]
	if (toUnits == 's'):
		convTime = tmpTime / 1.0
	elif (toUnits == 'min'):
		convTime = tmpTime / VRV_CONST_SECONDS_PER_MINUTE
	elif (toUnits == 'h'):
		convTime = tmpTime / VRV_CONST_SECONDS_PER_HOUR

	return convTime

def convertArea(area, fromUnits, toUnits):
	"""
	Convert an area from `fromUnits` to `toUnits`.
	
	Parameters
	----------
	area: float
		The numeric value describing an area to be converted.
	fromUnits: string
		Area units, before conversion. See :ref:`Units` for options.
	toUnits: string
		Desired units of area after conversion. See :ref:`Units` for options.

	Returns
	-------
	float
		New value of area, after conversion.
		
	Example
	-------
	    >>> import veroviz as vrv
	    >>> areaSQKM = 1.0
	    >>> areaSqMiles = vrv.convertArea(50, 'sqkm', 'sqmi')	
	    >>> areaSqMiles
	    >>> 19.305
	"""

	[valFlag, errorMsg, warningMsg] = valConvertArea(area, fromUnits, toUnits)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)
		
	try:
		fromUnits = fromUnits.lower()
	except:
		pass
				
	# Convert input to square meters:	
	fromUnits = areaUnitsDictionary[fromUnits]
	if (fromUnits == 'sqft'):
		tmpArea = area / VRV_CONST_SQFT_PER_SQMETER 
	elif (fromUnits == 'sqmi'):
		tmpArea = area / VRV_CONST_SQMILES_PER_SQMETER
	elif (fromUnits == 'sqkm'):
		tmpArea = area / VRV_CONST_SQKM_PER_SQMETER
	else:
		tmpArea = area
	
	try:
		toUnits = toUnits.lower()
	except:
		pass
		
	# Convert from square meters to desired output units:
	toUnits = areaUnitsDictionary[toUnits]
	if (toUnits == 'sqft'):
		convArea = tmpArea * VRV_CONST_SQFT_PER_SQMETER 
	elif (toUnits == 'sqmi'):
		convArea = tmpArea * VRV_CONST_SQMILES_PER_SQMETER
	elif (toUnits == 'sqkm'):
		convArea = tmpArea * VRV_CONST_SQFT_PER_SQMETER
	else:
		convArea = tmpArea
	
	return convArea

def initDataframe(dataframeType):
	"""
	Return an empty dataframe of a given type.

	Parameters
	----------
	dataframeType: string
		The options are 'Nodes', 'Arcs', and 'Assignments'.  These options are case insensitive.

	Returns
	-------
	pandas.dataframe
		A dataframe of the given type.  See :ref:`Nodes`, :ref:`Arcs`, and :ref:`Assignments` for details on each dataframe type.

	Example
	-------
	    >>> import veroviz as vrv
	    >>> newNodes = vrv.initDataframe('Nodes')
	    >>> newNodes
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valInitDataframe(dataframeType)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		dataframeType = dataframeType.lower()
	except:
		pass
	
	if (dataframeType == 'nodes'):
		dataframe = pd.DataFrame(
			columns=nodesColumnList)
	elif (dataframeType == 'assignments'):
		dataframe = pd.DataFrame(
			columns=assignmentsColumnList)
	elif (dataframeType == 'arcs'):
		dataframe = pd.DataFrame(
			columns=arcsColumnList)
	else:
		return

	return dataframe

def getMapBoundary(nodes=None, arcs=None, locs=None):
	"""
	Find the smallest rectangle that encloses a collection of nodes, arcs, assignments, and/or locations.  This function returns a list of lists, of the form [minLat, maxLon], [maxLat, minLon]].  This is equivalent to finding the southeast and northwest corners of the rectangle.
	
	Parameters
	----------
	nodes: :ref:`Nodes`, Conditional, `nodes`, `arcs`, and `locs` cannot be None at the same time
		A :ref:`Nodes` dataframe.
	arcs: :ref:`Arcs` or :ref:`Assignments`, Conditional, `nodes`, `arcs`, and `locs` cannot be None at the same time
		An :ref:`Arcs` or :ref:`Assignments` dataframe.
	locs: list of lists, Conditional, `nodes`, `arcs`, and `locs` cannot be None at the same time
		A list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  
	Returns
	-------
	list of lists
		In form of [[minLat, maxLon], [maxLat, minLon]].  These two points denote the southeast and northwest corners of the boundary rectangle.

	Example
	-------
		>>> import veroviz as vrv
		>>>
		>>> # Create 3 nodes, with blue pin markers (default):
		>>> myNodes = vrv.createNodesFromLocs(
		...     locs = [[42.1343, -78.1234], 
		...             [42.5323, -78.2534], 
		...             [42.9812, -78.1353]])
		>>> 
		>>> # Create 1 arc, with orange arrows (default):
		>>> myArc = vrv.createArcsFromLocSeq(locSeq = [[42.62, -78.20], 
		...                                            [42.92, -78.30]])
		>>> 
		>>> # Define 2 locations, with altitude.  (We'll color these purple later):
		>>> myLocs = [[42.03, -78.26, 100], [42.78, -78.25, 200]] 
		>>>
		>>> # Find the boundary of these objects:
		>>> myBoundary = vrv.getMapBoundary(nodes = myNodes,
		...                                 arcs  = myArc,
		...                                 locs  = myLocs)
		>>> myBoundary
		[[42.03, -78.1234], [42.9812, -78.3]]
		
		>>> # Initialize a map with nodes (blue) and an arc (orange):
		>>> myMap = vrv.createLeaflet(nodes = myNodes, 
		...                           arcs  = myArc)
		>>>
		>>> # Add red (default) circle markers for the locations:
		>>> for i in range(0, len(myLocs)):
		...    myMap = vrv.addLeafletMarker(mapObject = myMap, 
		...                                 center    = myLocs[i])    
		>>>
		>>> # Convert myBoundary to a 4-point polygon:
		>>> myBoundingRegion = [myBoundary[0], 
		...                     [myBoundary[0][0], myBoundary[1][1]], 
		...                     myBoundary[1], 
		...                     [myBoundary[1][0], myBoundary[0][1]]]
		>>>
		>>> # Add the bounding region to the map:
		>>> myMap = vrv.createLeaflet(mapObject      = myMap, 
		...                           boundingRegion = myBoundingRegion)
		>>> # Display the map:
		>>> myMap
	"""
	# validation
	[valFlag, errorMsg, warningMsg] = valGetMapBoundary(nodes, arcs, locs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	# Adjust the scope of the map to proper
	allLats = []
	allLons = []
	if (nodes is not None):
		allLats.extend(nodes['lat'].tolist())
		allLons.extend(nodes['lon'].tolist())

	if (arcs is not None):
		allLats.extend(arcs['startLat'].tolist())
		allLats.extend(arcs['endLat'].tolist())
		allLons.extend(arcs['startLon'].tolist())
		allLons.extend(arcs['endLon'].tolist())

	if (locs is not None):
		for i in range(len(locs)):
			allLats.append(locs[i][0])
			allLons.append(locs[i][1])

	maxLat = max(allLats)
	minLat = min(allLats)
	maxLon = max(allLons)
	minLon = min(allLons)

	if (abs(maxLat - minLat) < 0.0001):
		maxLat = maxLat + 0.05
		minLat = minLat - 0.05
	if (abs(maxLon - minLon) < 0.0001):
		maxLon = maxLon + 0.05
		minLon = minLon - 0.05

	maxLat = maxLat + 0.01
	minLat = minLat - 0.01
	maxLon = maxLon + 0.01
	minLon = minLon - 0.01

	return [[minLat, maxLon], [maxLat, minLon]]

def convertMatricesDataframeToDictionary(dataframe):
	"""
	This function is intended for use with time/distance matrices, which are stored in veroviz as Python dictionaries. This function transforms a matrix dataframe into  a dictionary, such that the indices of columns and rows become a tuple key for the dictionary.

	Parameters
	----------
	dataframe: pandas.dataframe
		The rows and columns are both integers. There should not be duplicated origin/destination pairs.

	Return
	------
	dictionary
		The keys are tuples of (originIndex, destinationIndex)

	Note
	----
	Pandas dataframes can be confusing when used with time and distance matrices.  In particular, suppose you have a distance dataframe named `distDF`.  The value of `distDF[1][2]` will actually return the distance from 2 to 1.  Conversely, if you have a distance dictionary named `distDict`, the value of `distDict[1,2]` will be the distance from 1 to 2.
	
	Example
	-------
	Prepare some data.
		>>> import veroviz as vrv
		>>> locs = [
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]]
		>>> exampleNodes = vrv.createNodesFromLocs(locs=locs)
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...     nodes        = exampleNodes, 
		...     routeType    = 'fastest', 
		...     dataProvider = 'OSRM-online')
		>>> [timeDict]
		[{(1, 1): 0.0,
		  (1, 2): 2869.9,
		  (1, 3): 4033.9,
		  (2, 1): 2853.3,
		  (2, 2): 0.0,
		  (2, 3): 4138.2,
		  (3, 1): 4037.8,
		  (3, 2): 4055.4,
		  (3, 3): 0.0}]

		>>> print("The travel time from node 1 to node 2 is %.2f seconds" % (timeDict[1, 2]))
		The travel time from node 1 to node 2 is 2869.90 seconds

		
	timeDict is a dictionary.  Convert to a dataframe:
		>>> timeDF = vrv.convertMatricesDictionaryToDataframe(timeDict)
		>>> timeDF

		>>> # NOTE:  The travel time from 1 to 2 is NOT found by timeDF[1][2].
		>>> # INSTEAD, you must use timeDF[2][1]
		>>> # Pandas uses the form timeDF[COLUMN_INDEX][ROW_INDEX]
		>>> timeDF[1][2], timeDF[2][1], timeDict[1, 2], timeDict[2, 1]
		(2853.3, 2869.9, 2869.9, 2853.3)


	We can transform a dataframe into a dictionary
		>>> timeDict2 = vrv.convertMatricesDataframeToDictionary(timeDF)
		>>> timeDict2
		>>> # This should be the same as `timeDict`
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

		>>> # Find the travel time *from* 1 *to* 3:
		>>> timeDict2[1,3]
		4033.9
		
	"""

	dictionary = {}
	try:
		(rowNum, columnNum) = dataframe.shape
		for i in range(rowNum):
			for j in range(columnNum):
				dictionary[dataframe.index[i], dataframe.columns[j]] = dataframe.at[dataframe.index[i], dataframe.columns[j]]
	except:
		print("Error: Duplicated key values, please check the columns and rows of dataframe")

	return dictionary

def convertMatricesDictionaryToDataframe(dictionary):
	"""
	This function is intended for use with time/distance matrices, which are stored in veroviz as Python dictionaries. This function transforms a matrix dictionary into a pandas dataframe.  The dictionary is assumed to have 2-tuple indices (the first index represents the ID of the "from" location, the second index is the ID of the "to" location).  In the resulting pandas dataframe, the row indices will represent the "from" location, the column indices the "to" location.

	Parameters
	----------
	dictionary: 
		The keys are tuples of (originIndex, destinationIndex) format.

	Return
	------
	pandas.dataframe
		The keys in the dictionary should be 2-tuples, the first value will be a row index, the second value will be a column index.

	Note
	----
	Pandas dataframes can be confusing when used with time and distance matrices.  In particular, suppose you have a distance dataframe named `distDF`.  The value of `distDF[1][2]` will actually return the distance from 2 to 1.  Conversely, if you have a distance dictionary named `distDict`, the value of `distDict[1,2]` will be the distance from 1 to 2.
	
	Example
	-------
	Prepare some data.
		>>> import veroviz as vrv
		>>> locs = [
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]]
		>>> exampleNodes = vrv.createNodesFromLocs(locs=locs)
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...     nodes        = exampleNodes, 
		...     routeType    = 'fastest', 
		...     dataProvider = 'OSRM-online')
		>>> [timeDict]
		[{(1, 1): 0.0,
		  (1, 2): 2869.9,
		  (1, 3): 4033.9,
		  (2, 1): 2853.3,
		  (2, 2): 0.0,
		  (2, 3): 4138.2,
		  (3, 1): 4037.8,
		  (3, 2): 4055.4,
		  (3, 3): 0.0}]

		>>> print("The travel time from node 1 to node 2 is %.2f seconds" % (timeDict[1, 2]))
		The travel time from node 1 to node 2 is 2869.90 seconds

		
	timeDict is a dictionary.  Convert to a dataframe:
		>>> timeDF = vrv.convertMatricesDictionaryToDataframe(timeDict)
		>>> timeDF

		>>> # NOTE:  The travel time from 1 to 2 is NOT found by timeDF[1][2].
		>>> # INSTEAD, you must use timeDF[2][1]
		>>> # Pandas uses the form timeDF[COLUMN_INDEX][ROW_INDEX]
		>>> timeDF[1][2], timeDF[2][1], timeDict[1, 2], timeDict[2, 1]
		(2853.3, 2869.9, 2869.9, 2853.3)


	We can transform a dataframe into a dictionary
		>>> timeDict2 = vrv.convertMatricesDataframeToDictionary(timeDF)
		>>> timeDict2
		>>> # This should be the same as `timeDict`
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

		>>> # Find the travel time *from* 1 *to* 3:
		>>> timeDict2[1,3]
		4033.9
	"""

	rows = []
	columns = []
	keys = dictionary.keys()

	for keys in dictionary:
		if (len(keys) != 2):
			print("Error: This dictionary is not a legitimate matrix, the key values should be pairs.")
			return

	try:
		for keys in dictionary:
			if (keys[0] not in rows):
				rows.append(keys[0])
			if (keys[1] not in columns):
				columns.append(keys[1])
		rows = rows.sort()
		columns = columns.sort()

		dataframe = pd.DataFrame(columns=columns, index=rows)
		for keys in dictionary:
			dataframe.at[keys[0], keys[1]] = dictionary[keys]
		
	except:
		print("Error: Failed to convert dictionary to dataframe.")

	return dataframe

def exportDataToCSV(data, filename):
	"""
	Export a dataframe or python time/distance matrix dictionary to a `.csv` file.

	Parameters
	----------
	data: pandas.dataframe or dictionary
		The data to be exported.  This can be a :ref:`Nodes`, :ref:`Arcs`, or :ref:`Assignments` dataframe, or it can be a time/distance python dictionary.
	filename: string
		The path and name of file to be exported.

	Examples
	--------
	The following examples will be the same as examples in :meth:`~veroviz.utilities.importDataFromCSV`.

	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(
		...              locs = [[42.1538, -78.4253], 
		...                      [42.3465, -78.6234], 
		...                      [42.6343, -78.1146]])
		>>> nodesDF	

	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = nodesDF, filename = 'test/nodes.csv')
	
	Import the dataframe we just saved:
		>>> importedNodes = vrv.importDataFromCSV(
		...     dataType = 'nodes',
		...     filename = 'test/nodes.csv')
		>>> importedNodes

	If the data type is inconsistent with the data, an error message will be thrown and nothing will be imported.
		>>> importedArcs = vrv.importDataFromCSV(
		...     dataType = 'arcs', 
		...     filename = 'test/nodes.csv')
		Error: test/nodes.csv was not successfully imported.  Check the data type.

	Similarly we can import and export the 'arcs' and 'assignments' dataframe

	For time/distance matrices, they are saved as dictionaries in VeRoViz, here is an example of how to import/export them.

	Get travel time/distance matrices using the nodes we just created:
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...           nodes        = nodesDF, 
		...           routeType    = 'fastest', 
		...           dataProvider = 'OSRM-online')
		>>> timeDict
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	Export the time dictionary to a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = timeDict, filename = 'test/timeMatrix.csv')

	Import the saved dictionary
		>>> importedTime = vrv.importDataFromCSV(
		...     dataType = 'matrix',
		...     filename = 'test/timeMatrix.csv')
		>>> importedTime
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	"""

	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	# Get directory
	if ("/" in filename):
		path = ""
		pathList = filename.split('/')
		if (len(pathList) > 1):
			for i in range(len(pathList) - 1):
				path = path + pathList[i] + '/'
			if not os.path.exists(path):
				os.makedirs(path, exist_ok=True)

	# Exporting
	if (type(data) is pd.core.frame.DataFrame):
		dataframe = data
		dataframe.to_csv(path_or_buf=filename, encoding='utf-8')
	elif (type(data) is dict):
		dataframe = convertMatricesDictionaryToDataframe(data)
		dataframe.to_csv(path_or_buf=filename, encoding='utf-8')

	if (VRV_SETTING_SHOWOUTPUTMESSAGE):
		print("Message: Data written to %s." % (filename))

	return

def importDataFromCSV(dataType, filename):
	"""
	Import from a `.csv` file into a dataframe or python time/distance matrix dictionary.

	Parameters
	----------
	dataType: string, Required
		The type of data to be imported.  Valid options are 'nodes', 'arcs', 'assignments', or 'matrix'.
	filename: string, Required
		The path and the name of the file to be imported.

	Return
	------
	pandas.dataframe or dictionary
		The resulting object depends on the data that are imported.  If the data are 'nodes', 'arcs' or 'assignments', return pandas.dataframe; otherwise, if the data are 'matrix', return dictionary.

	Examples
	--------
	The following examples will be the same as examples in :meth:`~veroviz.utilities.exportDataToCSV`

	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()

	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(
		...              locs = [[42.1538, -78.4253], 
		...                      [42.3465, -78.6234], 
		...                      [42.6343, -78.1146]])
		>>> nodesDF	

	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = nodesDF, filename = 'test/nodes.csv')
	
	Import the dataframe we just saved:
		>>> importedNodes = vrv.importDataFromCSV(
		...     dataType = 'nodes',
		...     filename = 'test/nodes.csv')
		>>> importedNodes

	If the data type is inconsistent with the data, an error message will be thrown and nothing will be imported.
		>>> importedArcs = vrv.importDataFromCSV(
		...     dataType = 'arcs', 
		...     filename = 'test/nodes.csv')
		Error: test/nodes.csv was not successfully imported.  Check the data type.

	Similarly we can import and export the 'arcs' and 'assignments' dataframe

	For time/distance matrices, they are saved as dictionaries in VeRoViz, here is an example of how to import/export them.

	Get travel time/distance matrices using the nodes we just created:
		>>> [timeDict, distDict] = vrv.getTimeDist2D(
		...           nodes        = nodesDF, 
		...           routeType    = 'fastest', 
		...           dataProvider = 'OSRM-online')
		>>> timeDict
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	Export the time dictionary to a .csv file in a subdirectory named "test":
		>>> vrv.exportDataToCSV(data = timeDict, filename = 'test/timeMatrix.csv')

	Import the saved dictionary
		>>> importedTime = vrv.importDataFromCSV(
		...     dataType = 'matrix',
		...     filename = 'test/timeMatrix.csv')
		>>> importedTime
		{(1, 1): 0.0,
		 (1, 2): 2869.9,
		 (1, 3): 4033.9,
		 (2, 1): 2853.3,
		 (2, 2): 0.0,
		 (2, 3): 4138.2,
		 (3, 1): 4037.8,
		 (3, 2): 4055.4,
		 (3, 3): 0.0}

	"""

	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	# validation - The validation of this script is different from others
	try:
		if (dataType.lower() in {'nodes', 'arcs', 'assignments'}):
			data = pd.read_csv(filename, index_col=0)
			if (dataType.lower() == 'nodes'):
				[valFlag, errorMsg, warningMsg] = valNodes(data)
				if (valFlag and warningMsg == ""):
					# print("Message: %s was successfully imported as Nodes dataframe" % filename)
					pass
				else:
					print("Error: %s was not successfully imported.  Check the data type." % filename)
					return
			elif (dataType.lower() == 'arcs'):
				[valFlag, errorMsg, warningMsg] = valArcs(data)
				if (valFlag and warningMsg == ""):
					# print("Message: %s was successfully imported as Arcs dataframe" % filename)
					pass
				else:
					print("Error: %s was not successfully imported.  Check the data type." % filename)
					return
			elif (dataType.lower() == 'assignments'):
				[valFlag, errorMsg, warningMsg] = valAssignments(data)
				if (valFlag and warningMsg == ""):
					# print("Message: %s was successfully imported as Assignments dataframe" % filename)
					pass
				else:
					print("Error: %s was not successfully imported.  Check the data type." % filename)
					return
			else:
				return

		elif (dataType.lower() == 'matrix'):
			dataframe = pd.read_csv(filename, index_col=0)
			dataframe.columns = dataframe.columns.astype(int)
			data = convertMatricesDataframeToDictionary(dataframe)
		else:
			print("Error: data type not supported, expecting 'nodes', 'arcs', 'assignments' or 'matrix' (for time matrix or distance matrix)")

	except (TypeError, ValueError):
		print("Error: Cannot import file: %s, check if `dataType` is correct for inputs." % (filename))

	except IOError:
		print("Error: Cannot import file: %s" % (filename))

	return data

def exportDataframe(dataframe, filename):
	"""
	Exports a nodes, arcs, or assignments dataframe to a `.csv` file.

	Parameters
	----------
	dataframe: pandas.dataframe, Required
		The dataframe to be exported.  This can be a :ref:`Nodes`, :ref:`Arcs`, or :ref:`Assignments` dataframe.
	filename: string, Required
		The path and the name of file to be exported.

	Example
	-------	
	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(locs=[
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]])
		>>> nodesDF
	
	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataframe(dataframe = nodesDF, filename = 'test/nodes.csv')
	
	Import the saved dataframe:
		>>> importedNodesDF = vrv.importDataframe('test/nodes.csv')
		>>> importedNodesDF
	"""

	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	# Get directory
	if ("/" in filename):
		path = ""
		pathList = filename.split('/')
		if (len(pathList) > 1):
			for i in range(len(pathList) - 1):
				path = path + pathList[i] + '/'
			if not os.path.exists(path):
				os.makedirs(path, exist_ok=True)

	try:
		dataframe.to_csv(path_or_buf=filename, encoding='utf-8')
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Data written to %s." % (filename))
	except:
		print("Error: Cannot export dataframe, please check the inputs.")

	return

def importDataframe(filename, intCols=False, useIndex=True):
	"""
	Imports a VeRoViz nodes, arcs, or assignments dataframe from a .csv file.  This function returns a pandas dataframe.

	Parameters
	----------
	filename: string, Required
		The path and the name of the file to be imported.
	intCols: boolean, Optional, default as False
		If the dataframe column names are integers (rather than text), set `intCols` to be True.  See notes below for more information.
	useIndex: boolean, Optional, default as True
		Setting this value to True means that the first column in the .csv will be used as the row indices.

	Note
	----
	If the dataframe is one of the following, the column names are not integers; leave `intCols=False` (default).  Also, leave `useIndex=True` (default):
	
	- nodes
	- arcs
	- assignments

	If you are importing the following matrices, it is recommended to use `importDataFromCSV()` function, the return value of that function will be a dictionary for matrix.

	- time matrix
	- distance matrix

	Return
	------
	pandas.dataframe
		A dataframe constructed from the contents of the imported .csv file.

	Example
	-------	
	Import veroviz and check if it is the latest version:
		>>> import veroviz as vrv
		>>> vrv.checkVersion()
	
	Create a nodes dataframe:
		>>> nodesDF = vrv.createNodesFromLocs(locs=[
		...     [42.1538, -78.4253], 
		...     [42.3465, -78.6234], 
		...     [42.6343, -78.1146]])
		>>> nodesDF
	
	Save the nodesDF dataframe as a .csv file in a subdirectory named "test":
		>>> vrv.exportDataframe(dataframe = nodesDF, filename = 'test/nodes.csv')
	
	Import the saved dataframe:
		>>> importedNodesDF = vrv.importDataframe('test/nodes.csv')
		>>> importedNodesDF
	"""

	# Replace backslash
	filename = replaceBackslashToSlash(filename)

	if (type(filename) is not str):
		print("Error: filename should be a string, please check the inputs.")
		return

	try:
		if (useIndex):
			df = pd.read_csv(filename, index_col=0)	
		else:
			df = pd.read_csv(filename, index_col=False)	
		if (intCols):
			df.columns = df.columns.astype(int)
	except:
		print("Error: Cannot import %s, please check the inputs." % (filename))

	return df

def getConvexHull(locs):
	"""
	Find the convex hull of a set of points.
	
	Parameters
	----------
	locs: list of lists
		A list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.

	Returns
	-------
	list of lists
		A list of lat/lon coordinates of the convex hull.  This is in the same form as the input points.
		
	Example
	-------
		>>> # Find the convex hull of 5 locs that straddle the Prime Meridian:
		>>> import veroviz as vrv
		>>> locs = [[51.4865,  0.0008], 
		...         [51.4777, -0.0002], 
		...         [51.4801,  0.0029], 
		...         [51.4726, -0.0161], 
		...         [51.4752,  0.0158]]
		>>> convexHull = vrv.getConvexHull(locs)
		>>> convexHull
		[[51.4726, -0.0161], [51.4865, 0.0008], [51.4752, 0.0158]]


		>>> # Display the 5 locations and the convex hull on a map:
		>>> myMap = None
		>>> for loc in locs:
		...     myMap = vrv.addLeafletMarker(mapObject=myMap, center=loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject=myMap, points=convexHull)
		>>> myMap
	"""
	
	# FIXME -- How does this work when crossing meridians?
	# I did some simple tests and it seems to be OK.

	[valFlag, errorMsg, warningMsg] = valGetConvexHull(locs)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	locs2D = []
	for i in range(len(locs)):
		locs2D.append([locs[i][0], locs[i][1]])
	
	ch2D = [locs[i] for i in scipy.spatial.ConvexHull(locs2D).vertices]

	ch = []
	for i in range(len(ch2D)):
		for j in range(len(locs2D)):
			if (abs(ch2D[i][0] - locs2D[j][0]) < 0.0001 and abs(ch2D[i][1] - locs2D[j][1]) < 0.0001):
				ch.append(locs[j])

	return ch

def isPointInPoly(loc, poly):
	"""
	Determine if a point is inside a polygon.  Points that are along the perimeter of the polygon (including vertices) are considered to be "inside".

	Parameters
	----------
	loc: list
		The coordinate of the point, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	poly: list of lists
		A polygon defined as a list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored. 

	Returns
	-------
	boolean
		The point is inside the polygon or not

	Examples
	--------
	Import veroviz:
	    >>> import veroviz as vrv

	Example 1 - Location is inside polygon:
		>>> loc = [42.03, -78.05]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		True
		
		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
	
	Example 2 - Location is outside polygon:
		>>> loc = [42.07, -78.05]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		False

		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 3 - Location is on the polygon boundary:
		>>> loc = [42.05, -78.10]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		True

		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
						
	Example 4 - Location is on a polygon vertex:
		>>> loc = [42.10, -78.10]
		>>> poly = [[42.00, -78.00], [42.10, -78.10], [42.00, -78.10]]
		>>> vrv.isPointInPoly(loc, poly)
		True
		
		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
		
	Example 5 - Non-convex poly region:
		>>> loc = [42.50, -78.90]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [42.2, -78.5], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPointInPoly(loc, poly)

		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
		
	Example 6 - Altitudes are included (but ignored):
		>>> loc = [42.05, -78.10, 100]
		>>> poly = [[42.00, -78.00, 200], [42.10, -78.10, 300], [42.00, -78.10, 200]]
		>>> vrv.isPointInPoly(loc, poly)		
		True
		
		>>> myMap = vrv.addLeafletMarker(center = loc)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
				
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPointInPoly(loc, poly)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	inside = geoIsPointInPoly(loc2D, poly2D)
		
	return inside

def isPathInPoly(path, poly):
	"""
	Determine if a given path is completely within the boundary of a polygon. 

	Parameters
	----------
	path: list of lists
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	poly: list of lists
		A closed polygon defined as a list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.
	
	
	Returns
	-------
	boolean
		True if the path lies entirely inside the polygon; False if at least one point of the path is not inside polygon.

	Examples
	--------
	Import veroviz:
	    >>> import veroviz as vrv

	Example 1 - Entire path is inside polygon:
		>>> path = [[42.50, -78.10], [42.50, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 2 - One of the vertices is on the edge of the polygon:
		>>> path = [[42.50, -78.10], [43.00, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		False

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 3 - Part of the path is outside of the polygon:
		>>> path = [[42.50, -78.10], [43.10, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		False
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 4 - Endpoints are in the polygon, but the poly isn't convex:
		>>> path = [[42.50, -78.10], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [42.2, -78.5], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathInPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 5 - Path and poly coordinates include altitude (which is ignored):
		>>> path = [[42.50, -78.10, 100], [42.50, -78.90, 200]]
		>>> poly = [[42.00, -78.00, 100], 
		...         [43.00, -78.00, 100], 
		...         [42.2, -78.5, 100], 
		...         [43.00, -79.00, 200], 
		...         [42.00, -79.00, 200]]
		>>> vrv.isPathInPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPathInPoly(path, poly)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	inside = geoIsPathInPoly(path2D, poly2D)

	return inside

def isPathCrossPoly(path, poly):
	"""
	Determine if a given path crosses the boundary of a polygon.

	Parameters
	----------
	path: list of lists
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	poly: list of lists
		A closed polygon defined as a list of individual locations, in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.

	Returns
	-------
	boolean
		True if the path have intersection with the polygon, false if no intersection

	Examples
	--------
	First import veroviz
	    >>> import veroviz

	Example 1 - Entire path is inside poly
		>>> path = [[42.50, -78.10], [42.50, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		False

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 2 - One of the vertices is on the edge of poly
		>>> path = [[42.50, -78.10], [43.00, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		True

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap

	Example 3 - Part of the path is outside of poly:
		>>> path = [[42.50, -78.10], [43.10, -78.50], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		True
		
		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap
		
	Example 4 - Endpoints are in poly, but poly isn't convex:
		>>> path = [[42.50, -78.10], [42.50, -78.90]]
		>>> poly = [[42.00, -78.00], [43.00, -78.00], [42.2, -78.5], [43.00, -79.00], [42.00, -79.00]]
		>>> vrv.isPathCrossPoly(path, poly)
		False

		>>> myMap = vrv.addLeafletPolyline(points = path)
		>>> myMap = vrv.addLeafletPolygon(mapObject = myMap, points = poly)
		>>> myMap	
		
	Example 5 - Path and poly include altitudes (which are ignored):
		>>> path = [[42.50, -78.10, 100], [42.50, -78.90, 300]]
		>>> poly = [[42.00, -78.00, 100], 
		...         [43.00, -78.00, 200], 
		...         [42.2, -78.5, 100], 
		...         [43.00, -79.00, 300], 
		...         [42.00, -79.00, 100]]
		>>> vrv.isPathCrossPoly(path, poly)	
		
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPathCrossPoly(path, poly)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])
	poly2D = []
	for i in range(len(poly)):
		poly2D.append([poly[i][0], poly[i][1]])

	crossFlag = geoIsPathCrossPoly(path2D, poly2D)

	return crossFlag

def isPassPath(loc, path, tolerance):
	'''
	Determine if any point along a path is within tolerance meters of a stationary point.
	(did our path pass by the target?)

	Parameters
	----------
	loc: list
		The stationary point to be tested if it has been passed, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	path: list of lists
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  This is considered as an open polyline.
	tolerance: float
		How close must the path be to the stationary location to be considered as "passed".  The units are in meters.
	
		
	Returns
	-------
	boolean
		Whether or not the path passes the point.

	Examples
	--------
	Prepare some data
		>>> import veroviz
		>>> path = [[42.50, -78.10], [42.50, -78.90]]

	Example 1 - The distance from the location to the path exceeds the tolerance.
		>>> awayLoc = [42.51, -78.50]
		>>> vrv.isPassPath(awayLoc, path, 1000)
		False
		
		>>> # Find the minimum distance, in meters, from the location to the path:
		>>> vrv.minDistLoc2Path(awayLoc, path)
		1105.9845259826711

		>>> myMap = vrv.addLeafletMarker(center = awayLoc)
		>>> myMap = vrv.addLeafletPolyline(mapObject = myMap, points = path)
		>>> myMap

	Example 2 - The distance from the location to the path is within the tolerance.
		>>> closeLoc = [42.505, -78.50]
		>>> vrv.isPassPath(closeLoc, path, 1000)
		True
		
		>>> # Find the minimum distance, in meters, from the location to the path:
		>>> vrv.minDistLoc2Path(closeLoc, path)	
		550.5689415111023
		
		>>> myMap = vrv.addLeafletMarker(center = closeLoc)
		>>> myMap = vrv.addLeafletPolyline(mapObject = myMap, points = path)
		>>> myMap
		
	Example 3 - Location and path include altitudes (which are ignored):
		>>> loc  = [42.505, -78.50, 100]
		>>> path = [[42.50, -78.40, 100], 
		...         [42.50, -78.60, 200], 
		...         [42.40, -78.70, 100]]
		>>> vrv.isPassPath(loc, path, 1000)
	'''

	# validation
	[valFlag, errorMsg, warningMsg] = valIsPassPath(loc, path, tolerance)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]
	path2D = []
	for i in range(len(path)):
		path2D.append([path[i][0], path[i][1]])

	passFlag = geoIsPassPath(loc2D, path2D, tolerance)

	return passFlag

def pointInDistance2D(loc, direction, distMeters):
	"""
	Find the [lat, lon, alt] coordinate of a point that is a given distance away from a current location at a given heading. This can be useful for determining where a vehicle may be in the future (assuming constant velocity and straight-line travel).

	Parameters
	----------
	loc: list
		The starting location, expressed as either [lat, lon, alt] or [lat, lon]. If no altitude is provided, it will be assumed to be 0 meters above ground level.		
	direction: float
		The direction of travel from the current location, in units of degrees.  The range is [0, 360], where north is 0 degrees, east is 90 degrees, south is 180 degrees, and west is 270 degrees.
	distMeters: float
		The straight-line distance to be traveled, in meters, from the current location in the given direction.

	Returns
	-------
	list
		A location a given distance away from the given location, in [lat, lon, alt] form.

	Example
	-------
		>>> import veroviz as vrv
		>>> startPt  = [42.80, -78.30, 200]
		>>> heading  = 45 # degrees. travel northeast.
		>>> distance = 300 # meters.
		>>> 
		>>> endPt = vrv.pointInDistance2D(startPt, heading, distance)
		>>> endPt
		
		>>> myArc = vrv.createArcsFromLocSeq(locSeq = [startPt, endPt])
		>>> myMap = vrv.createLeaflet(arcs=myArc)
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=startPt, fillColor='red')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=endPt, fillColor='green')
		>>> myMap
	"""
	
	# validation
	[valFlag, errorMsg, warningMsg] = valPointInDistance2D(loc, direction, distMeters)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	loc2D = [loc[0], loc[1]]

	newLoc = geoPointInDistance2D(loc2D, direction, distMeters)

	if (len(loc) == 3):
		newLoc = [newLoc[0], newLoc[1], loc[2]]

	return newLoc

def minDistLoc2Path(loc, path):
	"""
	Calculate the minimum distance, in [meters], from a single stationary location (target) to any point along a path.

	Parameters
	----------
	loc: list
		The coordinate of the stationary location, in either [lat, lon] or [lat, lon, alt] format.  If provided, the altitude will be ignored.
	path: list of lists
		A list of coordinates in the form of [[lat1, lon1, alt1], [lat2, lon2, alt2], ...] or [[lat1, lon1], [lat2, lon2], ...].  If provided, altitudes will be ignored.  

	Returns
	-------
	float
		The minimum distance, in meters, between the stationary location and the given polyline (path).

	Examples
	--------
	Prepare some data
		>>> import veroviz
		>>> path = [[42.50, -78.10], [42.50, -78.90]]
		>>> loc1 = [42.50, -78.50]
		>>> loc2 = [42.51, -78.50]
		>>> loc3 = [42.51, -78.00]

	Example 1 - The location is on the path:
		>>> vrv.minDistLoc2Path(loc1, path)
		0.0

	Example 2 - The minimum distance is between points on the path:
		>>> vrv.minDistLoc2Path(loc2, path)
		1105.9845259826711
		
	Example 3 - The minimum distance is to an endpoint of the path:
		>>> vrv.minDistLoc2Path(loc3, path)
		8293.970453010765

	Show the objects on a map:
		>>> myMap = vrv.addLeafletMarker(center=loc1, fillColor='blue')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=loc2, fillColor='green')
		>>> myMap = vrv.addLeafletMarker(mapObject=myMap, center=loc3, fillColor='purple')
		>>> myMap = vrv.addLeafletPolyline(mapObject=myMap, points=path)
		>>> myMap
		
	Example 4 - The location and path include altitudes (which are ignored):
		>>> path2 = [[42.50, -78.40, 100], 
		...          [42.50, -78.60, 200], 
		...          [42.40, -78.70, 100]]
		>>> loc4  = [42.51, -78.3, 300]
		>>> vrv.minDistLoc2Path(loc4, path2)

	"""

	[valFlag, errorMsg, warningMsg] = valMinDistLoc2Path(loc, path)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	distMeters = geoMinDistLoc2Path(loc, path)

	return distMeters

def distance2D(loc1, loc2):
	"""
	Calculates the geodesic distance between two locations, using the geopy library.  Altitude is ignored.

	Parameters
	----------
	loc1: list
		First location, in [lat, lon] format.
	loc2: list
		Second location, in [lat, lon] format.
	
	Return
	------
	float
		Geodesic distance between the two locations.

	Example
	-------
		>>> import veroviz as vrv
		>>> loc1 = [42.80, -78.90]
		>>> loc2 = [42.82, -78.92]
		>>> dist2D = vrv.distance2D(loc1, loc2)
		>>> dist2D
		2759.0335974131926
	"""

	[valFlag, errorMsg, warningMsg] = valDistance2D(loc1, loc2)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)
	
	distMeters = geoDistance2D(loc1, loc2)

	return distMeters

def distance3D(loc1, loc2):
	"""
	Estimates the distance between two point, including changes in altitude.  The calculation combines geopy's geodesic distance (along the surface of an ellipsoidal model of the earth) with a simple estimate of additional travel distance due to altitude changes.

	Parameters
	----------
	loc1: list
		First location, in [lat, lon, alt] format.
	loc2: list
		Second location, in [lat, lon, alt] format.
	
	Return
	------
	float
		Distance between the two locations.

	Example
	-------
		>>> import veroviz as vrv
		>>> loc1 = [42.80, -78.90, 0]
		>>> loc2 = [42.82, -78.92, 300]
		>>> dist3D = vrv.distance3D(loc1, loc2)
		>>> dist3D
		2775.2957304861734
	"""
	
	[valFlag, errorMsg, warningMsg] = valDistance3D(loc1, loc2)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	distMeters = geoDistance3D(loc1, loc2)

	return distMeters

def distancePath2D(path):
	"""
	Calculate the total geodesic distance along a path defined by [lat, lon] coordinates.  

	Parameters
	----------
	path: list of lists
		A list of coordinates that form a path, in the format of [[lat, lon], [lat, lon], ...].

	Return
	------
	float
		Total length of the path.

	Example
	-------
		>>> import veroviz as vrv
		>>> locs = [[42.80, -78.90], [42.82, -78.92], [42.84, -78.94]]
		>>> path = vrv.distancePath2D(locs)
		>>> path
		5517.760959357638
	"""

	[valFlag, errorMsg, warningMsg] = valDistancePath2D(path)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	dist = 0
	for i in range(0, len(path) - 1):
		dist += distance2D(path[i], path[i + 1])

	return dist

def getHeading(currentLoc, goalLoc):
	"""
	Finds the heading required to travel from a current location to a goal location.  North is 0-degrees, east is 90-degrees, south is 180-degrees, west is 270-degrees.

	Parameters
	----------
	currentLoc: list
		The [lat, lon] of current location
	goalLoc: list
		The [lat, lon] of goal location

	Return
	------
	float
		Heading at current location towards goal location in degrees.

	Example
	-------
		>>> import veroviz as vrv
		>>> locCurrent = [42.80, -78.90]
		>>> locGoal    = [42.85, -78.85]
		>>> heading = vrv.getHeading(locCurrent, locGoal)
		>>> heading
		36.24057197338239
		
		>>> # View the arc from the current location to the goal:
		>>> arc = vrv.createArcsFromLocSeq(locSeq = [locCurrent, locGoal])
		>>> vrv.createLeaflet(arcs=arc)		
	"""

	[valFlag, errorMsg, warningMsg] = valGetHeading(currentLoc, goalLoc)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	bearingInDegree = geoGetHeading(currentLoc, goalLoc)

	return bearingInDegree

