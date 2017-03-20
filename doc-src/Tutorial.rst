Tutorial
========

Import new data From WinRiver to MySQL
--------------------------------------

To import data from WinRiver (I or II) to mysql, you can use 2 methods. The first one is a pure python which uses the python WinRiver ascii file parser from  *libImportADCP.py*. The second uses a terminal interface, *Importer.py*, that allows to load huge amount of measurement files contained in folders.

WinRiver ASCII output
*********************

The ascii parser, is build to decode CLASSICAL ASCII output produced by WinRiver. The database is built to store each velocity computation mode (when they are available i.e. when a GPS is connected to the ADCP). You have to export a classical ASCII output for each reference modes (a BT file for bottom track, and if a GPS is plugged: a GGA file and a VTG file). 

1. Open a measurement in WinRiver and select reference mode **BT**.

2. Turn classical ASCII output on.

3. Reprocess your transect.

Then move the created ASCII file to a new folder (I called it BT). And re-start this operation for GPS references GGA and VTG. Don't forget to move files in different folders, otherwise WinRiver recover the previous ASCII file. If you have a lot of measurements the terminal Importer script need to have for on measurement the **same file name for each mode** in different folders. Typically folder names could be BT / GGA / VTG.

Import using a Terminal
***********************

1. First you need to edit the file Importer.py (with a simple text editor) to change the path where libImporterADCP.py is located (line 25)::

	[l 25] sys.path.append('/path/to/libImporter')
	
	Change this line using your path where you install libImporterADCP.py

2. Create a comment file, where your data are located (below is a suggested path tree):

   * \\Data

     * \\BT

       * measure_000_ASC.TXT
       * measure_001_ASC.TXT
       * ...
     * \\GGA

       * measure_000_ASC.TXT
       * measure_001_ASC.TXT
       * ...
     * \\VTG

       * measure_000_ASC.TXT
       * measure_001_ASC.TXT
       * ...
	
   Under linux (Mac also) open a terminal and go where Data folder is located and use **ls** command to create the file comment.txt by listing files in one subfolder for example BT::
	
	ls ./BT > comment.txt

   The file comment.txt should look like this::

	measure_000_ASC.TXT
	measure_001_ASC.TXT
	...

   Now you have to add comment in front of each file names using "|" character as separator::

	measure_000_ASC.TXT|My comment on measurement number 1
	measure_001_ASC.TXT|My comment on measurement number 2
	...

   Your comment file is now ready !

3. Open a terminal, go to the folder where your data is located and type::
	
	/path/to/Importer.py -rivername your_river_name -dbt ./BT -dvtg ./VTG -dgga ./GGA -dcom ./comment.txt -user ADCP -pass ADCP

The description of all options is available in help::

	/path/to/Importer.py -h

Import using python
*******************

If you want to import a single file (just reference BT) or if you want to build your own importer you can use directly libImportADCP.py in a python script.

* Here is an example to import file measure_0_000_BT.TXT with **BT** reference::
	
	#Specify the location of libImportADCP.py
	import sys
	sys.path.append('/path/to/libImportADCP')

	import libImportADCP as importer

	#Init the importer class named AdcpToSql
	#AdcpToSql(
	#	usa=Mysql username [default: 'root']
	#	pasa=Mysql userpass [default: '']
	#	serva=Mysql server address [default: 'localhost']
	#	basa=Mysql database name [default: 'BaseADCP']
	#	mode=reference mode [default: 'BT']

	import_bt = importer.AdcpToSql(mode='BT',usa='ADCP',pasa='ADCP',serva='localhost',basa='BaseADCP')

	#Get the new id for your file from mysql (this check profcode and return max+1)
	import_bt.getnids()
	print("The mysql id for this measurement is %i"%import_bt.nid)

	#Add the path of the file
	import_bt.NameIn('/path/to/measure_0_000_BT.TXT')

	#Add the path and name of sql output file that will be created by the parser
	import_bt.NameOut('/path/to/output.sql')

	#Add river name
	import_bt.rivername('Your river name')

	#Add a comment 
	import_bt.comment('Your comment on this measurement')

	#Parse the Input file -> this create Nameout file containing sql sentences with data
	import_bt.parsADCP()

	#Upload this file to mysql
	import_bt.sourceADCP()

  A more synthetic way::

	#Specify the location of libImportADCP.py
	import sys
	sys.path.append('/home/hugo/developpement/python/adcp/lib')

	import libImportADCP as importer

	#Give all informations at class initialisation
	import_bt = importer.AdcpToSql(mode='BT',nema='/pat/to/measure_0_000_BT.TXT',nemb='/path/to/output.sql', rena='your river name', coma='your comment on this measurement', usa='ADCP',pasa='ADCP',serva='localhost',basa='BaseADCP')
	
	#parse 
	import_bt.parsADCP()
	#source to mysql
	import_bt.sourceADCP()

* For **GGA** or **VTG** file you need to link the id (Profcode in EnsembleInfo table) to the parent BT measurement id (from the code above, the id can be obtain from **import_bt.nid**). This will upload correctly the 2 associated profiles (VTG and GGA) and you don't need to specify river name and comment again. Here is an example for a **GGA file** and a **VTG file**::

	#YOU have to import libImportADCP see example below

    
	#### GGA file ####
	#Don't forget to set the mode to 'GGA'
	import_gga = importer.AdcpToSql(mode='GGA',nema='/pat/to/measure_0_000_GGA.TXT',nemb='/path/to/output.sql')
	
	#Set the parentid (i.e. ProfCode of BT record already presents in MySQL)
	#To Get it you can use libADCP to list rivers present in database 
	#from libADCP import River
	#idriver = River(usa='ADCP', pasa='ADCP')
	
	#or use mysql command "SELECT Profcode, rivername, comment FROM ProfileInfo"

	#here supose BT data have profcode=12
	import_gga.Idparent(12) #you can also specify this id in AdcpToSql with argument parent=12
	#parse and upload
	import_gga.parsADCP()
	import_gga.sourceADCP()

	#### VTG file #####
	#Don't forget to set the mode to 'VTG' and parent to the same measurement BT profcode (here for the example 12)
	import_vtg = importer.AdcpToSql(mode='VTG',perent=12,nema='/pat/to/measure_0_000_VTG.TXT',nemb='/path/to/output.sql')
	#Parse and source
	import_vrg.parsADCP()
	import_vtg.sourceADCP()


Transect or time serie
----------------------

The River class allows to work with single transect or time series (fix location) data.

Get Started (In 3 steps)
************************

1. Some useful import (update path to folder where libADCP.py is located)::
	
	#Add path to library
	import sys
	sys.path.append('/home/your/folder/to/libADCP/')
	
	#yes pylab for do scientific stuff with python
	from pylab import *
	
	#import classes from libADCP
	from libADCP import *
	
2. To begin you need to initialize the River class.::
	
	riverid = 10 #Id of river in mysql database (correspond to cols Profcode from ProfileInfo table)
	mode = 'BT' #Measurement reference mode BT : bottom track
	dbuser='ADCP' #mysql user
	dbpass='TOTO' #mysql user password
	
	#Init the River class
	trav = River(riverid,mode,usa=dbuser,pasa=dbpass)
	
3. Now the most useful thing... Retrieve data from mysql and store them in a python dictionary::

	#The method GetDatas allow to retrieve selected data from mysql 
	trav.GetData('VM,TDMG,VD')

	#The velocity magnitude VM is now stored in
	trav.data['VM']
	
	#check the shape
	shape(trav.data['VM']) #Wow it's a 2D array

	#Idem for Travel meet good TDMG and velocity direction VD
	trav.data['TDMG']
	trav.data['VD']
		
	
Export ADCP data
****************

To export ADCP data of a given profile in a specific folder.

.. code-block:: python

    import libADCP as ADCP
    
    mes = adcp.River(3, mode='BT', usa='ADCP', pasa='ADCP')
    mes.GetData('DEPTH, VM, TDNG, LAT, lON')
    
    mes.Export('./path/to/output/directory','all')
    
Export GPS locations
********************

If you use a GPS with your ADCP during measurements you can export GPS position to KML format or simple text file::
	
	#YOU NEED TO IMPORT lON and LAT data
	trav.GetData('lON,LAT')

	#Export as KML
	trav.ExportPosition('./test.kml',format='kml')

	#As a text file
	trav.ExportPosition('./test.asc',format='txt')	


Compute discharge
*****************

To compute the discharge::

	#You need to create a River object
	riverid = 10 #Id of river in mysql database (correspond to cols Profcode from ProfileInfo table)
	mode = 'BT' #Measurement reference mode BT : bottom track
	dbuser='ADCP' #mysql user
	dbpass='TOTO' #mysql user password
	
	riv = River(riverid,mode,usa=dbuser,pasa=dbpass)
	
	#Then you can simply use print to display usefull informations
	
	print riv
	
	#Or you can get the discharge with the Dicharge method
	
	Q, Sec, Vel, W, H = riv.Discharge()
	
	#Datas computed using riv.Discharge() are also stored in self.datas
	riv.data['Discharge']
	riv.data['Section areea']
	riv.data['Mean velocity']
	riv.data['Width']
	riv.data['Mean depth']
	



