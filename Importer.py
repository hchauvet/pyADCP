#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Importer.py
#       
#       Copyright 2011 hugo <chauvet[at]ipgp.fr>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.

#############################################################
# Script pour import de grosses données (plusieurs points)  #
#############################################################

#Version : 0.1
#Modification date : 09.03.2011

import pylab as m

#ajout du chemin vers la bibliothèque libImportADCP
import sys
import os
sys.path.append('/path/to/folder/of/libImportADCP/')

#les libraries persos pour ADCP
import libImportADCP as imp

class Importer :
	""" 
	This is the main class of Importer, that contain all methods. The terminal interface is manage by Importer.Terminal method. To use it open a terminal and run this file. You need to define the path were libADCP is located before

	HELP WHEN YOU ARE IN A TERMINAL:

	This program permit to load a lot of ascii files with all of speed reference (BT,GGA,VTG) from WinRiver to mysql. You need to use CLASSIC output from WinRiver II (or II) for each reference mode (BT,GGA,VTG). For a given measurements each files (one per mode, 3 modes BT,GGA,VTG) must have the same name and need to located in different folders. 

	For set comments you need to edit a .txt file with the name of file following (separated by a tab) by the comment like :
	name_of_file_000.TXT [tab] My awersone comment.

	[ Commands ]	
	-h : show this help

	-rivername : Name of the river 
	-dbt : Path to folder containing data with BT reference
	-dgga : Path to folder containing data with GGA reference
	-dvtg : Path to folder containing data with VTG reference
	-dcom : Path to comments file

	-pass : Password for mysql database

	[options] 
	-user : user name for Mysql [default : root]
	-server : server address for Mysql [default : localhost]
	-basename : base name in Mysql [default : BaseADCP]
	"""
	
	def __init__ (self):
		""" Class initialiser
		Define default value for mysql connection
		"""
		
		#Variables
		self.db_user = 'root'
		self.db_pass = ''
		self.db_base = 'BaseADCP'
		self.db_serv = 'localhost'
		
	def Set_directory (self,BT_dir,GGA_dir,VTG_dir):
		""" 
		This function permit to define the folder where are located all the different data.
		"""
				
		self.bt_dir = BT_dir
		self.gga_dir = GGA_dir
		self.vtg_dir = VTG_dir
		
		#verfication
		for i in [self.bt_dir,self.gga_dir,self.vtg_dir] :
			if os.path.isdir(i) == False :
				print('[ERROR] path does not exist : %s'%i)
	
	def Name_builder (self):
		""" 
		Build file names contained in each folder and count them.
		"""
		
		#initialisation des dicos
		self.bt = {}
		self.gga = {}
		self.vtg = {}
		
		#les nom des fichier 
		#BT 
		self.bt['name'] = 	os.listdir(self.bt_dir)
		self.bt['number'] = len(self.bt['name'])
		#GGA
		self.gga['name'] = 	os.listdir(self.gga_dir)
		self.gga['number'] = len(self.gga['name'])
		#VTG
		self.vtg['name'] = 	os.listdir(self.vtg_dir)
		self.vtg['number'] = len(self.vtg['name'])
		
		#Verfication du nombre de donneés (le meme dans les 3 repertoires)
		if self.bt['number'] != self.gga['number'] :
			print('[ERROR] : pas le même nombre de fichiers entre bt et gga')
		
		if self.bt['number'] != self.vtg['number'] :
			print('[ERROR] : pas le même nombre de fichiers entre bt et vtg')
		
		if self.gga['number'] != self.vtg['number'] :
			print('[ERROR] : pas le même nombre de fichiers entre gga et vtg')
	
	def Read_commentfile (self,cmt_file):
		""" 
		Read the comment file (file that contains the file name and a small comment on the value). Files for 3 modes must have the same name.
		
		COMMENT file structure:
		on_measure_file.TXT|Comment1
		an_other.TXT|Comment2
		"""
		brute = m.loadtxt(cmt_file,dtype='S',delimiter='|')
		
		#on va faire correspondre les commentaire avec l'odre des fichier des dictionnaires self.bt, self.gga, self.vtg
		self.datas = {} #init la liste des commentaires	
		list_name = []
		list_com = []
		print("[Files] \nFile name \t\t Comment\n")
		
		#CORRECTION POUR LES FICHIER QUI N'ONT QUE UNE RIVIERE
		if (brute.size==len(brute)) :
			list_com.append(brute[1])
			list_name.append(brute[0])
			
			#On affiche le nom et le commentaire
			print("%s \t %s \n"%(brute[0],brute[1]))
		else: 	
			for i in brute :
				list_com.append(i[1])
				list_name.append(i[0])

			#On affiche le nom et le commentaire
			print("%s \t %s \n"%(i[0],i[1]))
		
		self.datas['com'] = list_com
		self.datas['name'] = list_name
			
	def Terminal (self):
		"""
		Method to set up terminal interface. Parse input parameters and run appropriate methods
		"""
		
		#récupération des arguments
		argu = sys.argv
		
		#On parse les arguments 
		if "-h" in argu:
			print("""

Importer v 0.1 by chauvet
help

This program permit to load a lot of ascii files with all of speed reference (BT,GGA,VTG) from WinRiver to mysql. So you need to use classic output from WinRiver II (or I) for each reference mode (BT,GGA,VTG). 

For set comments you need to edit a .txt file with the name of file following (separated by a tab) by the comment like :
name_of_file_000.TXT|My awersone comment.  For a given measurements each files (one per mode, 3 modes BT,GGA,VTG) must have the same name and need to located in different folders. 

[ Commands ]
-h : show this help

-rivername : Name of the river 
-dbt : Path to folder containing data with BT reference
-dgga : Path to folder containing data with GGA reference
-dvtg : Path to folder containing data with VTG reference
-dcom : Path to comments file

-pass : Password for mysql database

[options] 
-user : user name for Mysql [default : root]
-server : server address for Mysql [default : localhost]
-basename : base name in Mysql [default : BaseADCP]

			"""
			)
			
		else : 
			error = 0 #init error checker
			
			#Nom de la rivière 
			try:
				ind = argu.index("-rivername")
				rname = argu[ind+1]
			except Exception :
				error = 1
				print('[Error] no river name')
			
			#BT path 
			try:
				ind = argu.index("-dbt")
				bt = argu[ind+1]
			except Exception :
				error = 1
				print('[Error] no path for BT folder')	
				
			#GGA path 
			try:
				ind = argu.index("-dgga")
				gga = argu[ind+1]
                isgga = True
			except Exception :
				#error = 1
                isgga = False
				print('[Warning] no path for GGA folder')	
				
			#VTG path 
			try:
				ind = argu.index("-dvtg")
				vtg = argu[ind+1]
                isvtg = True
			except Exception :
				#error = 1
                isvtg = False
				print('[Warning] no path for VTG folder')	
			
			#Comment file 
			try:
				ind = argu.index("-dcom")
				dcom = argu[ind+1]
			except Exception :
				error = 1
				print('[Error] no path for comment file')	
			
			#Passwd for Mysql
			try:
				ind = argu.index("-pass")
				passwd = argu[ind+1]
			except Exception :
				error = 1
				print('[Error] no password for MYSQL')	
				
			#Serveur mysql
			try:
				ind = argu.index("-server")
				self.db_serv = argu[ind+1]
			except :
				self.db_serv
				
			#User name for DB
			try:
				ind = argu.index("-user")
				self.db_user = argu[ind+1]
			except :
				self.db_user
				
			#Db Name 			
			try:
				ind = argu.index("-basename")
				self.db_base = argu[ind+1]
			except :
				print self.db_base
				
			#SI ON A PAS D'ERREUR ON COMMENCE
			if error == 0 :
				#on affiche le résumé
				print("\n[Entries] \nRivername : %s \nPath for bt : %s \nPath for gga : %s \nPath for vtg : %s \nPath for comments : %s \nPassword for Mysql : %s\n\n"%(rname,bt,gga,vtg,dcom,passwd))
				
				#On lance la reconnaissances des fichiers et la construction des noms
				self.Set_directory(bt,gga,vtg)
				self.Name_builder()
				self.Read_commentfile(dcom)
					
				#On commence le traitement
				cpt = 1
				for i in self.datas['name'] :
					print("\n[Info]\nStart parsing file number %i"%(cpt))
					
					#BT 
					imp_bt = imp.AdcpToSql(usa=self.db_user, pasa=passwd, serva=self.db_serv, basa=self.db_base)
					#On récupére l'id
					imp_bt.getnids()
					bt_id = imp_bt.nid #gestion des avancé des id 
					print("Id in mysql : %i"%bt_id)
					
					#On met à jour le fichier de sortie
					imp_bt.NameIn(bt+'/'+i)
					imp_bt.NameOut('./tmp_bt')
					imp_bt.RiverName(rname)
					imp_bt.RiverComm(self.datas['com'][cpt-1])
					
					#Parsing
					print("Parsing File (BT)")
					imp_bt.parsADCP()
					print("uploading to sql")
					imp_bt.sourceADCP()
					
					#GGA 
                    if isgga:
                        imp_gga = imp.AdcpToSql(mode='GGA',parent=bt_id,usa=self.db_user, pasa=passwd, serva=self.db_serv, basa=self.db_base)
                        #On met à jour le fichier de sortie
                        imp_gga.NameIn(bt+'/'+i)
                        imp_gga.NameOut('./tmp_gga')
                        imp_gga.RiverName(rname)
                        imp_gga.RiverComm(self.datas['com'][cpt-1])
                        
                        #Parsing
                        print("Parsing File (GGA)")
                        imp_gga.parsADCP()
                        print("uploading to sql")
                        imp_gga.sourceADCP()
					
					#VTG
                    if isvtg:
                        imp_vtg = imp.AdcpToSql(mode='VTG',parent=bt_id,usa=self.db_user, pasa=passwd, serva=self.db_serv, basa=self.db_base)
                        #On met à jour le fichier de sortie
                        imp_vtg.NameIn(bt+'/'+i)
                        imp_vtg.NameOut('./tmp_gga')
                        imp_vtg.RiverName(rname)
                        imp_vtg.RiverComm(self.datas['com'][cpt-1])
                        
                        #Parsing
                        print("Parsing File (VTG)")
                        imp_vtg.parsADCP()
                        print("uploading to sql")
                        imp_vtg.sourceADCP()
                    
                    #add one to the counter
					cpt+=1
					
if __name__ == '__main__':
	a = Importer()
	a.Terminal()
	#~ a.Set_directory('/home/hugo/datas/adcp/simone11012011/BT','/home/hugo/datas/adcp/simone11012011/GGA','/home/hugo/datas/adcp/simone11012011/VTG')
	#~ a.Name_builder()
	#~ a.Read_commentfile('/home/hugo/datas/adcp/simone11012011/comment.txt')
