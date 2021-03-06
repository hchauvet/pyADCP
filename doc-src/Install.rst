Installation
============

pyADCP woks on the python 2.x branch.

Requirement
-----------

pyADCP requires several python libraries:

* pylab
* numpy
* matplotlib
* MySQLdb

To install these libraries, you can use the powerful tool python pip (a repository with easy instal procedure) `Python pip <http://pypi.python.org/pypi/pip>`_. 

It also require MySQL server (see MySQL setup section).

On Linux all these are common packages, and can be easily installed via package managers.

.. note:: 
   On windows you can install python Anaconda distribution that
   contain a lot of python libraries (pylab, numpy, matplotlib,
   etc...) `Anaconda (use the 2.X branch) <https://www.continuum.io/downloads>`_.

Downloads
---------

Go to the `pyADCP github page <https://github.com/hchauvet/pyADCP>`_ and download the
repository. This repository contains:

* **BaseADCP.sql**, The BaseADCP schema of the MySQL database to
  create them.

* **libADCP.py**, the main library to work with ADCP data stored in MySQL.

* **libImportADCP.py**, manage how to convert WinRIVER ascii data to
  sql and import them to a MySQL database.

* **Importer.py**, a terminal interface to import large data-sets. 

MySQL setup
-----------

1. You need to install MySQL server on your computer.
   
   * Install guide :

     - `Ubuntu <http://doc.ubuntu-fr.org/mysql>`_ 
     - `Generic Linux/Mac/Windows
       <http://dev.mysql.com/doc/refman/5.0/en/installing.html>`_



2. In a terminal launch mysql (or run mysql terminal on windows) and
   connect with the root account::

	mysql -uroot -p

3. Create a database named BaseADCP and exit mysql.::

	create database BaseADCP;
	exit;

4. Import the structure of BaseADCP located in the file
   **BaseADCP.sql**.::

	mysql -uroot -pyourpass BaseADCP < BaseADCP.sql

Your done with the installation of the MySQL database you can now
import data following `this tutorial <Tutorial.html#import-new-data-from-winriver-to-mysql>`_

Database Structure 
******************
.. image:: images/BaseADCP.jpg

ADCPData Structure
##################

This table contains information relative to 4-Beams measurements link to EnsembleInfo by **Ensemblecode**.

+-------------+-------+----+------+
|Colonne      |Type   |Null|Défaut|
+=============+=======+====+======+
|//**Dcode**//|int(11)|Non |      |
+-------------+-------+----+------+
|Ensemblecode |int(11)|Non |      |
+-------------+-------+----+------+
|DEPTH        |float  |Non |      |
+-------------+-------+----+------+
|VM           |float  |Non |      |
+-------------+-------+----+------+
|VD           |float  |Non |      |
+-------------+-------+----+------+
|EVC          |float  |Non |      |
+-------------+-------+----+------+
|NVC          |float  |Non |      |
+-------------+-------+----+------+
|VVC          |float  |Non |      |
+-------------+-------+----+------+
|ERRV         |float  |Non |      |
+-------------+-------+----+------+
|BCKSB1       |float  |Non |      |
+-------------+-------+----+------+
|BCKSB2       |float  |Non |      |
+-------------+-------+----+------+
|BCKSB3       |float  |Non |      |
+-------------+-------+----+------+
|BCKSB4       |float  |Non |      |
+-------------+-------+----+------+
|PG           |float  |Non |      |
+-------------+-------+----+------+
|Q            |float  |Non |      |
+-------------+-------+----+------+

EnsembleInfo Structure 
######################

This table contains information relative to one Ensemble of measurements link to 
the table ProfileInfo by **Profcode**.

+--------------------+----------+----+------+
|Colonne             |Type      |Null|Défaut|
+--------------------+----------+----+------+
|Profcode            |int(11)   |Non |      |
+--------------------+----------+----+------+
|//**Ensemblecode**//|int(11)   |Non |      |
+--------------------+----------+----+------+
|ETYear              |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|ETMonth             |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|ETDay               |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|ETHour              |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|ETMin               |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|ETSec               |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|ETHund              |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|ENum                |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|NES                 |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|PITCH               |float     |Oui |NULL  |
+--------------------+----------+----+------+
|ROLL                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|CORRHEAD            |float     |Oui |NULL  |
+--------------------+----------+----+------+
|ADCPTemp            |float     |Oui |NULL  |
+--------------------+----------+----+------+
|BTVelE              |float     |Oui |NULL  |
+--------------------+----------+----+------+
|BTVelN              |float     |Oui |NULL  |
+--------------------+----------+----+------+
|BTVelUp             |float     |Oui |NULL  |
+--------------------+----------+----+------+
|BTVelErr            |float     |Oui |NULL  |
+--------------------+----------+----+------+
|CBD                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|GGAA                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|GGAD                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|GGAHDOP             |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DB1                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DB2                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DB3                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DB4                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|TED                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|TET                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|TDTN                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|TDTE                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|TDMG                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|LAT                 |double    |Oui |NULL  |
+--------------------+----------+----+------+
|lON                 |double    |Oui |NULL  |
+--------------------+----------+----+------+
|NDInv               |float     |Oui |NULL  |
+--------------------+----------+----+------+
|NDfnvu              |float     |Oui |NULL  |
+--------------------+----------+----+------+
|NDfnvu2             |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DVMP                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DVTP                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DVBP                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DVSSDE              |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DVSD                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DVESDE              |float     |Oui |NULL  |
+--------------------+----------+----+------+
|DVED                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|SDML                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|SDBL                |float     |Oui |NULL  |
+--------------------+----------+----+------+
|NBINS               |int(11)   |Oui |NULL  |
+--------------------+----------+----+------+
|MU                  |varchar(2)|Oui |NULL  |
+--------------------+----------+----+------+
|VR                  |varchar(3)|Oui |NULL  |
+--------------------+----------+----+------+
|IU                  |varchar(6)|Oui |NULL  |
+--------------------+----------+----+------+
|ISF                 |float     |Oui |NULL  |
+--------------------+----------+----+------+
|SAF                 |float     |Oui |NULL  |
+--------------------+----------+----+------+

ProfileInfo Structure
#####################

This table contains information relative to one measurement.

+----------------+-----------+----+------+
|Colonne         |Type       |Null|Défaut|
+----------------+-----------+----+------+
|//**Profcode**//|int(11)    |Non |      |
+----------------+-----------+----+------+     
|rivername       |varchar(55)|Oui |NULL  |
+----------------+-----------+----+------+
|DCL             |int(11)    |Non |      |
+----------------+-----------+----+------+
|BAT             |int(11)    |Non |      |
+----------------+-----------+----+------+
|DFCF            |int(11)    |Non |      |
+----------------+-----------+----+------+
|NDC             |int(11)    |Oui |NULL  |
+----------------+-----------+----+------+
|NPPE            |int(11)    |Oui |NULL  |
+----------------+-----------+----+------+
|TPE             |int(11)    |Oui |NULL  |
+----------------+-----------+----+------+
|PM              |int(11)    |Oui |NULL  |
+----------------+-----------+----+------+
|comment         |blob       |Oui |NULL  |
+----------------+-----------+----+------+
|Type            |int(11)    |Non |0     |
+----------------+-----------+----+------+
|GGAcode         |int(11)    |Non |0     |
+----------------+-----------+----+------+
|VTGcode         |int(11)    |Non |0     |
+----------------+-----------+----+------+

  
