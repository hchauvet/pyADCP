#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       libADCP.py
#
#       Copyright 2009 hugo chauvet <chauvet@ipgp.jussieu.fr>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
##############################################################################
#
# Version : 1.O
# Last-modification : 09.02.2014
# author : chauvet
#
##############################################################################
#MYSQL CONFIGURATION
DBuser='root'
DBpasswd=''
DBserv='localhost'
DBname='BaseADCP'
####################################################
#require sudo apt-get install python-mysqldb
import MySQLdb
import matplotlib
from numpy import *
import pylab as m
import threading  #Pour le multiprocessing
import time
import datetime #pour gestion du temps

#THE CLASS RIVER contain all functions for River
class River:

    #constructeur
    def __init__(self,idriverin='',mode='BT',usa=DBuser, pasa=DBpasswd, serva=DBserv, basa=DBname, termode='normal'):
        '''Class Doc : River
        This class permit to load and process ADCP data. This datas are stored in MySQL databases.

        To Initiate this class you need to define the ID of the river, otherwise the program show the list of data presents in databases with their ID.

        [options]

        -mode [default = 'BT'] : permit to chose reference mode for velocity computation made by WinRiverII. You have the choice between 'BT' for bottom trac, 'GGA' for GPS referenced or 'VTG' for GPS ref for fixed points.

        MYSQL variables are stored at the biggining of libADCP.py but you can also edit them when you load this class
        -usa : you can define username for mysql databases
        -pasa : define password for mysql
        -serva : define the mysql server address
        -basa : define mysql database name

        -termode [default = 'normal'] : Change the verbose mode, if the value is not 'normal', the class doesn't show all the messages on screen.
        '''
        #Mysql connection
        self.user=usa
        self.passwd=pasa
        self.serv=serva
        self.base=basa
        self.mode=mode
        self.conn = MySQLdb.connect(self.serv,self.user,self.passwd,self.base)
        self.termode=termode
        self.idriverglobal=idriverin
        self.SelectMode() #In order to get the good id using mode

        #test if idriver is empty
        if self.idriverglobal=='':
            self.SelectRiver()

        #set badValues replacement
        self.badvalue=-30000

    def Dbclose (self):
        """ Function doc
        Permet de fermer la connexion à la dB"""
        self.conn.close()

    def MsgTerm (self,type,msg):
            """ Function in order to display alert and info whith good colors, the type of message to display is define in Type and the messag
            in msg.
            Type :
            0 - ADD
            1 - ERROR
            2 - INFO
            """
            if type==0:
                typeout='\033[92m [ADD] ';
            if type==1:
                typeout='\033[91m'+'[ERROR] '
            if type==2:
                typeout='\033[90m'+'[INFO] '

            if self.termode=='normal':
                print(typeout+'\033[0m '+msg)
            if self.termode=='mysql':
                if type==0:
                    print(typeout+'\033[0m '+msg)


    def SelectMode(self):
        #use the mode (BT,GGA,VTG) to get the good river id
        if self.mode=='BT':
            self.idriver=self.idriverglobal
        else:
            if self.mode=='GGA':
                select='GGAcode'
            if self.mode=='VTG':
                select='VTGcode'

            curs=self.conn.cursor()
            cmd='Select '+select+' FROM ProfileInfo WHERE Profcode='+str(self.idriverglobal)
            mysql=curs.execute(cmd)
            result=array(curs.fetchall())
            curs.close()

            #put the river Profcode in river id
            self.idriver=int(result[0])

            #If self.idriver==0 give a warning
            if self.idriver==0:
                self.MsgTerm(1,'mode '+self.mode+' does not exist')


    #select river method
    def SelectRiver(self):
        #init cursor
        curs=self.conn.cursor()
        #mysql commande
        cmd='SELECT rivername, Profcode, comment FROM ProfileInfo'
        mysql=curs.execute(cmd)
        result=array(curs.fetchall())
        curs.close()
        nbriver=size(result[:,0])
        for i in m.r_[0:nbriver]:
            print("%s \t %s \t %s \n"%(result[i,1],result[i,0],result[i,2]))

        flag = 0
        while flag == 0:
            identer = raw_input("Select one id ? ")
            if identer in result[:,1]:
                self.idriverglobal = int(identer)
                flag = 1
            else:
                MsgTerm(1,"This id doesn't exist RETRY")

    def TestDatas(self,datain):
            #method to test if datas is already loaded
            data_to_load = ''
            for i in datain:
                try:
                    self.datas[i]
                except:
                    data_to_load+=i+','
                    self.MsgTerm(0,'Loading '+i+' datas from Mysql')

            if data_to_load != '' :
                self.GetDatas(data_to_load[:-1])


    #Correction of get data to remove the "s"
    def GetData(self, datasin):
        
        #run GetDatas
        self.GetDatas(datasin)
        
        #Store in self.data 
        self.data = self.datas
        
    #get datas method
    def GetDatas(self,datasin):
        #init self.datas
        try:
            self.datas
        except:
            self.datas={}

        self.MsgTerm(0,'Loading datas  from Mysql in river[]')
        #init sql parser class
        if datasin == 'all' :
            #BESOIN DE DEBUGGUER LES TYPE TXT !!!! DANS Parser !
            datasin = 'NBINS,VM,VVC,ERRV,PG,BCKSB1,BCKSB2,BCKSB3,BCKSB4,NVC,EVC,Q,VD,ETYear,ETMonth,ETDay,ETHour,ETSec,ETMin,ETHund,ENum,NES,PITCH,ROLL,CORRHEAD,ADCPTemp,BTVelE,BTVelN,BTVelUp,BTVelErr,CBD,GGAA,GGAD,GGAHDOP,DB1,DB2,DB3,DB4,TED,TET,TDMG,TDTN,TDTE,LAT,lON,NDInv,NDfnvu,NDfnvu2,DVMP,DVTP,DVBP,DVSSDE,DVSD,DVESDE,DVED,SDML,SDBL,NBINS,MU,VR,IU,ISF,SAF,DCL,BAT,DFCF,NPPE,TPE,PM,NDC,PM,comment,DEPTH'
        sql = Adcp_Sql_Parser(self,datasin)
        #run sql requests
        sql.SqlRequest()


    def ShowProfil(self):
        #method to show profil
        #test if we have the good datas loaded
        for i in ['VM','DEPTH']:
                try:
                        self.datas[i]
                except:
                        self.MsgTerm(0,'Loading '+i+' datas from Mysql')
                        self.GetDatas(i)

        #do the plot
        long=r_[0:self.datas['VM'].shape[1]]
        #f=m.Figure(dpi=100)
        #c=f.add_subplot(111)
        m.pcolor(long,-self.datas['DEPTH'].ravel(),self.datas['VM'])
        m.colorbar()
        #set good limits
        m.xlim(0, max(long))
        m.ylim(min(-self.datas['DEPTH'].ravel()), 0)
        m.show()

    def GetTime(self):
        #method to get time for times series
        self.TestDatas(['ETYear','ETMonth','ETDay','ETHour','ETMin','ETSec','ETHund'])

        #creation du temps prenant en compte les centieme
        tima=self.datas['ETHour']*60.+self.datas['ETMin']+self.datas['ETSec']/60.+self.datas['ETHund']/6000.
        self.time=tima-min(tima)

        #creation d'un datetime
        self.datetime = []
        for i in xrange(len(self.datas['ETYear'])):
            self.datetime.append(datetime.datetime(2000+int(self.datas['ETYear'][i]),int(self.datas['ETMonth'][i]),int(self.datas['ETDay'][i]),int(self.datas['ETHour'][i]),int(self.datas['ETMin'][i]),int(self.datas['ETSec'][i]),int(self.datas['ETHund'][i])))
        #transform into array
        self.datetime = m.array(self.datetime)
        return tima

    def GetBCKS(self):
        #method to get the mean of 4 bacskatter signal from 4 beans
        self.GetDatas('BCKSB1,BCKSB2,BCKSB3,BCKSB4')
        #init the array with good dimention
        self.datas['BCKS']=zeros([self.datas['BCKSB1'][:,0].size,self.datas['BCKSB1'][0,:].size],double)
        #compute the mean
        for i in r_[0:self.datas['BCKSB1'][:,0].size]:
            for j in r_[0:self.datas['BCKSB1'][0,:].size]:
                self.datas['BCKS'][i,j]=mean([self.datas['BCKSB1'][i,j],self.datas['BCKSB2'][i,j],self.datas['BCKSB3'][i,j],self.datas['BCKSB4'][i,j]])

    def ProfVert(self,lim,component):
        """method to compute the temporal mean of velocities
        for each depth between [liminf and limup]
        lim need to be a list or a tuple [liminf,limfsup]
        example [0,1]
        component is the component of the velocity like u,v,w
        """
        self.TestDatas(['DEPTH']);
        self.TestDatas([component]);
        #get time
        #self.GetTime()
        #vmoy=zeros(self.datas[component][:,0].size,double)
        #Modified by CHAUVET intruducing masked_array
        #~ vmoy=[]
        #~ for i in range(self.datas[component][:,0].size):
            #~ tmp=self.datas[component][i,lim[0]:lim[1]]
            #~
            #~ #if isnan(mean(tmp[m.find(tmp!=self.badvalue)]))==False :
            #~ vmoy.append(mean(tmp))

        #NEW VERSION
        vmoy = m.mean(self.datas[component][:,lim[0]:lim[1]],1)
        return m.ma.masked_invalid(vmoy)

    def FondMoy(self):
        #method to define the mean value of bottom
        #Try and add data if it's needed
        self.TestDatas(['DB1','DB2','DB3','DB4'])
        #Find the mean of the 4 signal
        self.fondmoy=zeros(self.datas['DB1'].size,double)+self.badvalue
        for i in xrange(self.datas['DB1'].size):
            #test for badvalues on prend celle qui sont valid
            tmp = []
            for b in ['DB1','DB2','DB3','DB4'] :
                if (self.datas[b].data[i] != self.badvalue and self.datas[b].data[i] != 0) :
                    tmp.append(self.datas[b][i])

            self.fondmoy[i] = mean(tmp)

        self.fondmoy = m.ma.masked_values(self.fondmoy,self.badvalue)

    def ProfLog(self,datain,meanbottom,**kwargs):
        """Method to compute the log law on mean data in order to optain k* and u*
        This return self.wall which is a poly1D class from the regression
        -----------

        datain is a Vertical profile of velocitie
        meanbottom is a value of the mean bottom you can get it with mean(riv.fondmoy)"""
        msg="A FAIRE"
        #test how work kargs
        for key in kwargs:
                print "another keyword arg: %s: %s" % (key, kwargs[key])

        #test if we have DEPTH
        self.TestDatas(['DEPTH'])
        #GET LIMITE OF AVAILABLE DATA FROM MASK
        lims = m.ma.notmasked_edges(datain)
        if lims[1] == -1:
            lims[1] = len(datain)-1 #si toutes les cellules sont valides
        #set DEPTH from bottom
        #test if we want normed or not
        if 'nobottom' in kwargs:
            if kwargs['nobottom']==True:
                z = self.datas['DEPTH'][:lims[1]+1]
        else:
            z=meanbottom-self.datas['DEPTH'][:lims[1]+1]

        datain = datain[:lims[1]+1]
        if 'normed' in kwargs:
            if kwargs['normed']==True:
                #norme the depth by the mean depth of the bottom
                z=z/meanbottom



        #Check if we have put limits
        if 'limsup' in kwargs:
            #Make the fit
            x=log(z[kwargs['limsup']:])
            y=datain[kwargs['limsup']:]
        elif 'liminf' in kwargs:
            x=log(z[:-kwargs['liminf']])
            y=datain[:-kwargs['liminf']]
        else:
            x=log(z)
            y=datain
        #use polyfit
        [c,d]=polyfit(x.ravel(),y,1)
        #store in self.wall and return the value
        self.wall = poly1d([c,d])
        self.MsgTerm(0,'regression coefficients added to self.wall')
        self.MsgTerm(2,self.wall)
        #build a polyome object
        return self.wall

    def WallPlot(self,h=2.7):
            x=r_[-9:log(h):0.1]
            m.plot(self.wall(x),exp(x))

    def GetUstar(self):
        '''return ustar from self.wall polynome
            return la pente fois von karman
        '''
        return self.wall.c[0]*0.41

    def GetZo(self):
        '''return ustar from self.wall polynome
            return la pente fois von karman
        '''
        return exp(-self.wall.c[1]/self.wall.c[0])

    def Fluct(self,compos,rev=0):
        #to compute fluctuation velocities
        #rev for correct bu for inverted profile
        self.TestDatas([compos])
        if rev==1:
            Vmoy=self.ProfVert([0,self.datas[compos][0][:].size],compos)[::-1]
            out=self.datas[compos][::-1][::-1]
        else:
            Vmoy=self.ProfVert([0,self.datas[compos][0][:].size],compos)
            out=self.datas[compos]

        Vprim=m.zeros([len(Vmoy),self.datas[compos][0][:].size])+self.badvalue

        #print(Vprim.size)
        for i in xrange(0,len(Vmoy)):
            for j in xrange(0,len(self.datas[compos][0,:])):
                #if out[i,j]!=self.badvalue:
                Vprim[i,j]=Vmoy[i]-out[i,j]

        return m.ma.masked_invalid(Vprim)

    def VerticalMean(self,vit_data):
        """ Fonction pour faire la moyenne verticale de la vitesse pour un obget rivière
        pour une serie définie par vit_data
        exemple :
        Vmvert=VerticalMean(River(56),'VM') """

        #on reccupère les vitesses
        self.TestDatas([vit_data])
        #riv.FondMoy()

        #make an array with the length of datas
        #Vvertmoy= zeros(len(self.datas[vit_data][0,:]))

        #[OLD VERSION] Modifed with masked_array by Hugo
        #~ for i in range(len(Vvertmoy)):
            #~ #print(mean(riv.datas[vit_data][m.find(riv.datas[vit_data][:,i]!=riv.badvalue),i]))
            #~ Vvertmoy[i]=mean(self.datas[vit_data][find(self.datas[vit_data][:,i]!=self.badvalue),i])
            #~ #If is Nan put to previous value
            #~ if isnan(Vvertmoy[i]):
                #~ MsgTerm(1,'dans vit vertical recopie de la valeur précèdante')
                #~ Vvertmoy[i]=Vvertmoy[i-1]

        return m.mean(self.datas[vit_data],0)

    def FluctCompo (self,component,lim):
        """ Compute the fluctuation for the given component and for size given in argument """
        #compute the mean component
        Meanc=self.ProfVert(lim,component)
        #Compute the out matrix
        fluc=zeros(self.datas[component][0:len(Meanc),lim[0]:lim[1]].shape)
        for i in range(len(fluc[:,0])):
            for j in range(len(fluc[0,:])):
                #test if is a bad value
                tmp=self.datas[component][i,j]
                if tmp!=self.badvalue:
                    fluc[i,j]=tmp-Meanc[i]
                else:
                    fluc[i,j]=self.badvalue
        #add the fluct component to datas
        self.datas['Fluc'+component]=fluc
        self.MsgTerm(0,'Fluctant component to river.datas[Fluc'+component+']')

    def BackScatt (self,beamsnum):
        """ Function doc
        beamsnum is the num of the couple of beam so 1 for (1-3 couple) and 2 for (2-4 couple)"""
        if beamsnum==1 or beamsnum==3 :
            names=['BCKSB1','BCKSB3']
            couple='1-3'
        if beamsnum==2 or beamsnum==4 :
            names=['BCKSB2','BCKSB4']
            couple='2-4'
        #import datas
        self.TestDatas(names)

        #compute the mean for the couple of beam
        out=zeros(self.datas[names[0]].shape)+self.badvalue
        for i in range(len(out[:,0])):
            for j in range(len(out[0,:])):
                #test if they are not badvalues
                if (self.datas[names[0]][i,j]!=self.badvalue) and (self.datas[names[1]][i,j]!=self.badvalue) :
                    out[i,j]=mean([self.datas[names[0]][i,j],self.datas[names[1]][i,j]])

        #DONT WORK IF ONE OF THE TWO ARE BADVALUE AND NOT THE OTHER
        #out=(self.datas[names[0]]+self.datas[names[1]])/2.
        #badvalue are the same because (badvalue+badvalue)/2=badvalue !!!

        self.MsgTerm(0,'mean backscatter for couple '+couple+' in river.datas[BCKSB'+couple+']')
        self.datas['BCKSB'+couple]=out

    def Projection (self,Meanangle):
        """ Function for compute the velocity magnitude in the mean direction whith a given Meanangle"""
        #test that we have VM
        self.TestDatas(['VM'])
        self.TestDatas(['VD'])
        #get the mean direction
        NewVM=zeros(self.datas['VM'].shape)
        V=zeros(self.datas['VM'].shape)

        #[OLD VERSION] Modified by chauvet introducting masked_array
        #Compute the new velocity in the mean plan
        #~ for i in xrange(0,len(NewVM[:,0])):
            #~ for j in xrange(0,len(NewVM[0,:])):
                #~ #test for bad values
                #~ if (Dir[i,j]!=self.badvalue and self.datas['VM'][i,j]!=self.badvalue):
                    #~ NewVM[i,j]=self.datas['VM'][i,j]*cos(Meanangle-Dir[i,j])
                    #~ V[i,j]=self.datas['VM'][i,j]*sin(Meanangle-Dir[i,j])
                #~ else:
                    #~ NewVM[i,j]=self.badvalue
                    #~ V[i,j]=self.badvalue

        #NEW VERSION
        NewVM = self.datas['VM']*cos(m.deg2rad(Meanangle-self.datas['VD']))
        V = self.datas['VM']*sin(m.deg2rad(Meanangle-self.datas['VD']))

        self.MsgTerm(0,'Adding the table of new velocities to River.datas[''NewVM'']')
        self.datas['NewVM']=NewVM
        self.MsgTerm(0,'Adding the table of new velocities transversal curent to River.datas[''V'']')
        self.datas['V']=V

    def AngleVM (self):
        """ Function for compute angle of velocity with artan2 function between NVC and EVC component
        and put the badvalues to badvalue def by user. This function return a table with the size of
        velocity profil """
        #test datas that we need for this function
        self.TestDatas(['VD','EVC','NVC'])
        #Compute the table
        #~ TabAngle=zeros(self.datas['VD'].shape)
        #~ for i in range(len(TabAngle[:,0])):
            #~ for j in range(len(TabAngle[0,:])):
                #test if VD is a badvalue
                #if (self.datas['VD'][i,j]!=self.badvalue):
                #TEST REMOVED BY CHAUVET WHEN INTRODUCING MASKED_ARRAY TYPE
        TabAngle=arctan2(self.datas['EVC'],self.datas['NVC'])
                #else:
                #TabAngle[i,j]=self.badvalue

        return TabAngle

    def MeanDir (self):
        """ Function for compute the mean direction for each depth cells"""

        self.TestDatas(['EVC','NVC'])
        #make an array with the length of datas
        #Dirm=[]


        #for i in range(self.datas['EVC'][:,0].size):
            #[OLD VERSION] modified by chauvet introducing masked_array
            #~ teste=mean(arctan2(self.datas['EVC'][i,m.find(self.datas['EVC'][i,:]!=self.badvalue)],self.datas['NVC'][i,m.find(self.datas['NVC'][i,:]!=self.badvalue)]))
            #~ #check is is not nan
            #~ if isnan(teste)==False:
                #~ Dirm.append(teste)

        #NEW VERSION

        return m.mean(m.arctan2(self.datas['EVC'],self.datas['NVC']),1)

    def VerticalMean(self,vit_data):
        """ Fonction pour faire la moyenne verticale de la vitesse pour un obget rivière
        pour une serie définie par vit_data
        exemple :
        Vmvert=River(56).VerticalMean('VM') """

        #on reccupère les vitesses
        self.TestDatas([vit_data])
        #riv.FondMoy()

        #[MODIFIED BY CHAUVET] introduction des masked_array
        #make an array with the length of datas
        #~ Vvertmoy= zeros(len(self.datas[vit_data][0,:]))
        #~ for i in range(len(Vvertmoy)):
            #~ #print(mean(riv.datas[vit_data][m.find(riv.datas[vit_data][:,i]!=riv.badvalue),i]))
            #~ Vvertmoy[i]=mean(self.datas[vit_data][m.find(self.datas[vit_data][:,i]!=self.badvalue),i])
            #If is Nan put to previous value
            #~ if isnan(Vvertmoy[i]):
                #~ self.MsgTerm(2,'Moyenne = NaN, recopie de la valeur précèdante')
                #~ Vvertmoy[i]=Vvertmoy[i-1]
        return m.mean(self.datas[vit_data],0)

    def Mean2D (self,x,z,dx,dz,component):
        """ Function to make the mean around a point (x,z) extent give by dx and dz
        x and z need to be matrix position not depth and time (use SuperFind)"""
        #define the datas box
        databox=self.datas[component][z-(dz+1):z+dz,x-(dx+1):x+dx]
        meanx=[]
        for i in range(len(databox[:,0])):
            if isnan(mean(databox[i,m.find(databox[i,:]!=self.badvalue)]))==False:
                meanx.append(mean(databox[i,m.find(databox[i,:]!=self.badvalue)]))

        print(meanx)
        return mean(meanx)

    def UW (self,compo):
            """ Function for compute the produc of mean_time(u' * w')
            compo : component for u (expl 'VM' ou 'NewVM' if reprjection)"""

            #test if we have datas
            self.TestDatas([compo])
            [self.TestDatas([i]) for i in ['DEPTH','VVC']]

            #Use Fluct to get the fluct component
            up=self.Fluct(compo)
            wp=self.Fluct('VVC')

            #A table for the multiply between the two with badvalue gestion
            out=m.zeros(up.shape)
            for i in range(len(up[:,0])):
                for j in range(len(up[0,:])):
                    if (up[i,j]!=self.badvalue and wp[i,j]!=self.badvalue):
                        out[i,j]=(up[i,j]*10**(-2))*(wp[i,j]*10**(-2))
                    else:
                        out[i,j]=self.badvalue

            self.datas['upwp']=out
            return out

    def Export (self,name_out,datas_in):
        """ Fonction in order to export datas to ascii format :
        You have to give the output name without extention and to give the datas you wants to export, this
        datas can be a list ['VM','VVC','DEPTH']"""
        #make an export for datas
        #to do : -Faire une option zip pour sortir un fichier zip contenant toute les données
        #    -Faire une option All pour tout sortir.
        if datas_in == 'all':
            datas_in = self.datas.keys()
            
        for i in datas_in:
            #self.TestDatas([i])#check if datas is loaded from mysql
            if i in self.datas.keys():
                nom_out=name_out+'_'+i+'.ASC'
                m.savetxt(nom_out,self.datas[i])

    
    #FONCTION IMPORT FICHIER TEXTE CONTENANT LES INTENSITEES DES 4 BEAM
    def ImportBCKS(self,folder,num_of_measurment,startf='outbcks_',endf='_ASC.TXT'):
        """docstring for ImportBCKS
        Fonction pour importer  les données d'intensitées issue de WinRiver II avec export ascii qui contient dans l'ordre
        intensity beam1 -> intensity beam4
        avec comme separateur ','

        Le fichier est découpé en 4"""

        #on creer le chemin complet pour loader le fichier
        toload = folder + startf + num_of_measurment + endf

        #Chargement des données
        alldatas = m.loadtxt(toload,delimiter=',')

        #Decoupage
        size_of_one = int(m.shape(alldatas)[1]/4.) #taille d'une beam

        #ON charge les données
        datas_name = ['Counts1','Counts2','Counts3','Counts4']
        #On va masquer les badvalues
        badval = -32768

        for i,value in enumerate(datas_name):
            self.datas[value] = m.ma.masked_values(alldatas[:,i*size_of_one:(i+1)*size_of_one].T,badval)
            #MESSSAGE d'AJOUT
            self.MsgTerm(0,"Intensite en counts pour le beam "+str((i+1))+" dans self.datas["+value+"]")

    #FONCTION POUR DEFINIR DES LIMITES
    def Xlim(self,linf,lsup):
        """docstring for Xlim
        Fonction pour definir les limites en x donc en numero d'ensemble.

        Entrées :
        linf : numero de l'ensemble a partir duquel on veut couper
        lsup : numero de l'ensemble jusqu'au quel on veut couper
        """

        #On cheq les données
        for i,value in enumerate(self.datas):
            #2D
            if value  in ['VM','VD','EVC','NVC','VVC','ERRV','BCKSB1','BCKSB2','BCKSB3','BCKSB4','Counts1','Counts2','Counts3','Counts4']:
                self.datas[value] = self.datas[value][:,linf:lsup]

            #1D A COMPLETER
            if value in ['ADCPTemp']:
                self.datas[value] = self.datas[value][linf:lsup]

        #test de coupure du temps aussi
        try:
            self.MsgTerm(2,'Xlim sur le time appliqué')
            self.time = self.time[linf:lsup]
        except Exception, e:
            self.MsgTerm(1,'Pas de temps definiti')


    def MeanCounts(self,nb=4):
        """docstring for MeanCounts
        Permet de faire la moyenne entre les données des intentisées

        Entrée optionnelle :
        nb [defaut = 4] : permet de definir sur combien de beam on fait la moyenne

        Sortie :
        self.datas['Mcounts'] : dans le dictionnaire des données on ajoute Mcounts
        """

        #definition des values sur lequesl on fait la moyenne
        values = ['Counts'+str(i+1) for i in range(nb)]

        #On boucle sur le tableau :
        Mcounts = m.zeros(m.shape(self.datas['Counts1']))
        for i in range(len(self.datas['Counts1'])) :
            for j in range(len(self.datas['Counts1'].T)) :
                Mcounts[i,j] = m.mean([self.datas[value][i,j] for value in values])

        #ON AJOUTE AU DICO EN MASQUANT LES NAN ET ON LE DIT
        self.datas['Mcounts'] = m.ma.masked_where(m.isnan(Mcounts),Mcounts)
        self.MsgTerm(0,'Moyenne des intensitées dans self.datas[Mcounts]')

    #Faire une fonction d'import de fichiers txt pour utilisation de la librairie ADCP.

    def Build_masks (self,datas):
        """ Function doc
        Fonction pour appliquer des masques sur les données
         """
        for i in datas:
            self.datas[i] = m.ma.masked_values(self.datas[i],self.badvalue)

    def ExportPosition (self,name_out,format='txt',process='mean') :
        """ Fonction pour exporter les positions GPS
        [option]
        format : 'txt' [default] exprot en format texte
                 'kml' export au format kml de google
        """

        #recupération du minimum en coord pour chaques points fixes
        datas_gps = m.vstack([self.datas['lON'],self.datas['LAT']])

        if format == 'txt' :
            #Ecriture dans un fichier
            f_out = open(name_out,'w')
            f_out.write("Lat_decim|Lon_decim\n")
            for i in datas_gps.T :
                f_out.write("%f|%f\n"%(i[1],i[0]))
            f_out.close()

        if format == 'kml' :
            #GESTION DES ENTETES ET DES FOOTERS
            kmlHeader = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
             '<Document>\n'
             '<name>'+str(self.idriver)+'</name>\n'
             '<Style id="yellowLineGreenPoly">\n'
            '<LineStyle>\n'
            '<color>7f00ffff</color>\n'
            '<width>4</width>\n'
            '</LineStyle>\n'
            '<PolyStyle>\n'
            '<color>7f00ff00</color>\n'
            '</PolyStyle>\n'
            '</Style>\n'
             )

            kmlFooter = ('</Document>\n'
                        '</kml>\n')

            lat = datas_gps[1]
            lon = datas_gps[0]
            name = m.r_[0:len(lon)]

            kml = ''
            kml += '<Placemark>\n'+'<name>'+str(self.idriver)+'</name>\n'
            kml += '<styleUrl>#yellowLineGreenPoly</styleUrl>'
            kml += (
                '<LineString>\n'
                '<extrude>1</extrude>\n'
                '<tessellate>1</tessellate>\n'
                '<coordinates>')
            for i in xrange(len(name)) :
                #tmp_lon = str(lon[i]).split('.')
                #tmp_lat = str(lat[i]).split('.')
                if (lon[i]!=self.badvalue and lat[i] != self.badvalue) :
                    kml += (
                    '%f,%f,1\n'
                    ) %(lon[i], lat[i])

            kml += ' </coordinates>\n</LineString>\n</Placemark>\n'
            kml_final = kmlHeader + kml + kmlFooter
            print kml_final
            open(name_out,'w').write(kml_final)


        
    def GPSProjDist (self,Po,Pf,zone_in,show=False,border=True,meanlatlon=False):
        """ Function doc
        Fonction pour faire une projection orthogonale des points GPS sur une traversée moyenne définie par les points Po (début) et Pf (fin)

        [entrées]

        Po : liste contenant lat et lon du point de début [lon,lat] en deg (WGS-84)
        Pf : liste contenant idem mais pour le point de fin
        zone: zone utm pour conversion
        border: if border = False trouve les bords a partir du minimum de projection

        [option]
        show [default=False]: Trace la projection si True

        [Sortie]

        Distance cumulée des points reprojetés en m
        +Ajout dans self.datas['d_GPS']
        +Ajout distance de la section dans self.datas['len_section']

        """

        #IMPORT DE LA BIBLIOTHEQUE pyproj pour gerer les projection
        from pyproj import Proj
        #init la projection
        p = Proj(proj='utm',zone=zone_in,ellps='WGS84')


        #DEFINITION DES PTS DEFINISSANT LA DIRECTION DE LA SECTION
        xo, yo = p(Po[0],Po[1])
        xf, yf = p(Pf[0],Pf[1])

        #ON PROJETE LES LON ET LAT DU GPS ET ON LES RAMENE PAR RAPPORT AU PTS_O
        xd, yd = p(self.datas['lON'],self.datas['LAT'])
        #si on donne les moyenne des lat lon
        if meanlatlon:
            xd, yd = p(self.datas['mlON'],self.datas['mLAT'])

        if border:
            #on recentre
            xd = xd - xo
            yd = yd - yo

        #LES NORMES ET ANGLES
        norm = m.sqrt(xd**2+yd**2)
        teta = m.arccos(xd/norm) #angle des vecteurs positions
        tetam = m.arccos((xf-xo)/m.sqrt((xf-xo)**2+(yf-yo)**2))
        #tetam = m.arccos((xf)/m.sqrt((xf)**2+(yf)**2))

        #REPROJECTION
        xnew =  norm * m.cos(tetam-teta) * m.cos(tetam)
        ynew =  norm * m.cos(tetam-teta) * m.sin(tetam)

        if border:
            xnew = xnew
            ynew = ynew
        else:
            #On recentre
            xoo = min(xnew)
            yoo = ynew[xnew==min(xnew)][0]

            xnew = xnew - xoo
            ynew = ynew - yoo

        #CALCUL DES DISTANCES CUMULEES
        dist = m.sqrt((xnew)**2 + (ynew)**2)

        #AFFICHAGE DE LA DISTANCE DE LA SECTION
        print("Largeur de la section %f m"%(m.sqrt((xf-xo)**2. + (yf-yo)**2)))

        if meanlatlon == False:
            self.datas['d_GPS'] = dist
            self.datas['len_section'] = m.sqrt((xf-xo)**2. + (yf-yo)**2)


        #POUR TESTER : REPRESENTATION GRAPHIQUE
        if show:
            m.plot([xo,xf],[yo,yf],'go--')
            m.plot(xd+xo,yd+yo,'r+')
            m.plot(xnew+xo,ynew+yo,'k+')

        return dist,  m.sqrt((xf-xo)**2. + (yf-yo)**2)

    def AddBottom(self,x,ax,size=2,step=1,facec='0.8',edgec='k'):
        """Function to add bottom plot to the axes defined by axes.AxesSubplot classe

        [option]
        size : define size of filled part [default=2]
        facec : define polygons face color
        edgec : define polygons edge color

        [Exemple]
        ax = subplot(111)
        plot(riv.time,blablabla)
        riv.AddBottom(riv.time,ax)
        """

        #MAKE LIST OF COORDINATES
        self.FondMoy()
        verts = [(x[0],-(max(self.fondmoy)+size))] + zip(x[::step],-self.fondmoy[::step]) + [(x[-1],-(max(self.fondmoy)+size))]

        #MAKE POLYGONS
        poly = m.Polygon(verts, facecolor=facec, edgecolor=edgec)

        #DRAW THE ON Axes
        ax.add_patch(poly)
        #update figure
        m.draw()

    def ShowVectorField(self,ref,dirm=0,nb_tobe_masked=10) :
        """Function to plot 3D vector field for mooving ADCP
        """
        from enthought.mayavi.mlab import quiver3d

        if ref == 'TDMG' :
            i = m.argsort(self.datas['TDMG'].data)
        else :
            i = m.argsort(self.datas['d_GPS'])

        #make meshgrid off positions
        y,z = m.meshgrid(self.datas[ref][i],-self.datas['DEPTH'])
        x = z*0
        #Make projection for velocities
        if dirm != 0 :
            Vtmp = self.datas['VM']*m.sin(m.deg2rad(dirm-self.datas['VD']))
            Utmp = self.datas['VM']*m.cos(m.deg2rad(dirm-self.datas['VD']))
        else :
            Vtmp = self.datas['VM']*m.sin(dirm-m.deg2rad(dirm-self.datas['VD']))
            Utmp = self.datas['VM']*m.cos(dirm-m.deg2rad(dirm-self.datas['VD']))

        #Don't take the mask and sort datas like y[ref] and put them in m.s**-1
        U = Utmp.data[:,i]*10**-2
        U[U==self.badvalue*10**-2] = m.NAN
        V = Vtmp.data[:,i]*10**-2
        V[V==self.badvalue*10**-2] = m.NAN
        W = self.datas['VVC'].data[:,i]*10**-2
        W[W==self.badvalue*10**-2] = m.NAN

        #Make the plot with mayavi2
        obj = quiver3d(x,y,z,U,V,W,mask_points=nb_tobe_masked)

        return obj

    #FONCTION POUR CHARGER LES VITESSES DES BEAMS
    def LoadBeamVelo(self,fname):
        '''
            Fonction to load beam velocity from txt file, This file is generated from 
            WinRIVER 2 with personal ascii output option.
            
            This function load and convert beam velocity into instrument refenrence velocity with correction of pitch and roll
            
            TODO:
                Add beam 1-2 solution for W and V with roll correction
                
            INPUTS:
                fname = path to the ascii file 
                
            OUTPUT:
                This function add to self.datas dictionnay:
                    - 'B1','B2','B3','B4' = beam velocity for beams 1,2,3,4
                    - 'W34i','Ui' = velocity in instrument referencial without pitch correction using beam 3 and 4 for computation
                    - 'W34', 'U' = velocity in instrument referencial with pitch correction using beam 3-4 solution
        '''
        
        #TEST IF DATAS NEEDED ARE LOADED
        self.TestDatas(['DEPTH','TDMG','PITCH'])
        
        #CALCUL DES TAILLES
        lenx = len(self.datas['DEPTH'])
        leny = len(self.datas['TDMG'])
    
        data_brut = m.loadtxt(fname,delimiter=',').T #LOAD DATA
        beam_velo = m.ma.masked_equal(data_brut.reshape(4,lenx,leny),-32768) #MASK INVALID AND RESHAPE
        
        #on enregistre
        self.datas['B1'] = beam_velo[0,:,:]
        self.datas['B2'] = beam_velo[1,:,:]
        self.datas['B3'] = beam_velo[2,:,:]
        self.datas['B4'] = beam_velo[3,:,:]
    
        #CALCUL DES COMPOSANTES DANS LE REF DE L'INSTRUMENT
        CC = 2 * cos(m.deg2rad(20))
        CS = 2 * sin(m.deg2rad(20))
        #U = B3+B4 / CS
        self.datas['W34i'] = (self.datas['B3']+self.datas['B4'])/CC
        self.datas['Ui'] = (self.datas['B3']-self.datas['B4'])/CS
        
        #PITCH CORRECTION
        #pp = arctan(tan(deg2rad(pts_fix.datas['PITCH']))*cos(deg2rad(pts_fix.datas['ROLL'])))
        pp = m.deg2rad(self.datas['PITCH'])
        CP = cos(pp)
        SP = sin(pp)
        self.datas['W34'] = CP * self.datas['W34i'] - SP * self.datas['Ui']
        self.datas['U'] = SP * self.datas['W34i'] + CP * self.datas['Ui']
    
    #FUNTION TO COMPUTE DE DISCHARGE (THX MEMET)
    def Discharge(self, vitesses_table, distance_table):
        """
            Function to compute the discharge from ADCP data
            
            #inuts:
                * vitesses_table: A 2D table containing the velocity data
                * distance_table: A 1D array containing the transverse positions
                
            #Example:
            
                riv = River( .... )
                Q, Sec, Velm, W, H = riv.Discharge( riv.datas['VM'], riv.datas['TDMG'] )
            
        """
        
        #Test the data WE NEED THE DEPTH TO BE LOADED
        self.TestDatas(['DEPTH'])
        
        y=m.array( distance_table )
        z=self.datas['DEPTH'].ravel()
        vm=m.array( vitesses_table )
        
        # initialise le débit et les section
        q=[]
        s=[]
        
        for v in vm:
            # cherche les valeurs  de vitesse >= 0 et redimensionne les TDMG
            yy=y[m.nonzero(v>=0)]
            vv=v[m.nonzero(v>=0)]
            #on procède à "l'envers" intégration en largeur puis en hauteur
            if len(yy)>=1:
                s.append(max(yy)-min(yy)) # enregistre la largeur à une profondeur donnée
            else:
                s.append(0) 
            q.append(m.trapz(vv,yy)) # enregistre l'intégrale des vitesses (debit 2D) pour une hauteur donnée
		
        q=m.array(q)

        # Débit
        Q= m.trapz(q,z)+z[0]*q[0]

        # Section
        Sec=m.trapz(s,z) +z[0]*s[0]

        # Vitesse moyenne
        Vel=Q/Sec

        # Largeur
        W=max(s)

        # Hauteur moyenne
        H=(Sec/W)

        #save to datas dict
        self.datas['Discharge'] = Q
        self.datas['Section areea'] = Sec
        self.datas['Mean velocity'] = Vel
        self.datas['Width'] = W
        self.datas['Mean depth'] = H
        
        return Q, Sec, Vel, W, H

    #Function to setup the print
    def __str__(self):
        
        #Get the discharge
        self.TestDatas(['VM','TDMG'])
        Q, Sec, Vel, W, H = self.Discharge( self.datas['VM']*10**-2, self.datas['TDMG'] )
        
        out = """Informations:
        River id = %i
        Discharge Q = %0.3f m**3/s
        Section area S = %0.3f m**2
        Mean velocity V = %0.3f m/s
        Width W = %0.3f m
        Mean depth H = %0.3f m
        """
        
        return out%(int(self.idriverglobal), Q, Sec, Vel, W, H)
        
class Section :
    """ Class doc
    Cette classe permet de faire des sections avec plusieurs mesures statiques

    Entrées :

    -ids : Vecteur avec les ids des points de mesures
    -dists : Vecteur avec les distances des points de mesures
    -data : Liste des données a chargé de la formet 'VM,DEPTH,VVC'

    Options :

    -mode : Mode de mesure de la vitesse BT,VTG,GGA [default = BT]
    """

    def __init__ (self,ids,data,mode='BT',ref='VM', mdir=0, dists=0, datas=None, usa=DBuser, pasa=DBpasswd, serva=DBserv, basa=DBname):
        """ Class initialiser 
        """

        #Stockage des variables
        self.dists = dists
        self.ids = ids
        self.mode = mode
        #FOR OLD COMPATIBILITY
        if datas:
            self.datas = datas
        else:
            self.datas = data
            
        self.data = data
        self.ref = ref
        self.mdir = mdir
        self.pts_fix = {} #initialisation du dictionnaire qui vas contenir les données des points fixes
        self.usa = usa
        self.pasa = pasa
        self.serva = serva
        self.basa = basa
        
        #CHARGEMENT DES DONNEES
        tps1 = time.time()
        self.LoadFromMysql()
        dt = time.time()-tps1
        print("Datas Loaded in %i seconds"%dt)

        #SI on a ref = 'NewVM' on doit lancer la projection
        if self.ref == 'NewVM' :
            [self.pts_fix[i].Projection(self.mdir) for i in self.pts_fix]

    def LoadFromMysql (self):
        """ Function doc :
        Methode permettant de charger les données de tous les points à partir de Mysql"""
        Loaded = [] #Init dico pour le multiThreading
        for i in self.ids :
            print("Loading id %i datas started"%i)
            Load = threader(River(i,self.mode,termode='quiet', usa=self.usa, pasa=self.pasa, serva=self.serva, basa=self.basa), self.datas)
            Load.start() #debut du processus
            Loaded.append(Load)

        #Jointure
        cpt = 0
        for Load in Loaded :
            Load.join()
            self.pts_fix[cpt] = Load.river_in
            cpt+=1


    def MeanVelo (self,proj_pt=False):
        """ Function doc
        This function allow to compute depth and time averaged velocities u,v component.

        Input :
        proj_pt, number of static point on which the stream direction is taken to get u and v of other static points
                 if = False no projection are realised
        Output
        u, streamwise component -- U(cos(mean(dir)-mean(dir_ref))
        v, secondary component -- U(sin(mean(dir)-mean(dir_ref))
        """
        print("TODO")

        for i in self.pts_fix:
            #les bonnes unitées
            #self.pts_fix[i].datas[self.ref] = self.pts_fix[i].datas[self.ref]*10**(-2)

            #Vitesse bruttes moyennées hauteur et sur tout le signal
            self.pts_fix[i].mean=m.mean(self.pts_fix[i].VerticalMean(self.ref))

        if proj_pt:
            u = [self.pts_fix[i].mean*m.cos(m.mean(self.pts_fix[i].meandir[:-4])-m.mean(self.pts_fix[proj_pt].meandir[:-4])) for i in self.pts_fix]
        else:
            u = [self.pts_fix[i].mean for i in self.pts_fix]

        u.insert(0,0) #vitesse nulle RG
        u.insert(len(u),0) #v=0 RD


        self.mean_u = u

        return u

    def ExportPosition (self,name_out,process='mean',format='txt') :
        """ Fonction pour exporter les positions GPS en prennant la moyenne de la serie

        [option]
        process : 'mean' [default] compute the mean of position
                  'first' use the first data of position
        format : 'txt' [default] output a textfile format of positions
                 'kml' export a kml compatible file
        """

        #recupération du minimum en coord pour chaques points fixes
        if process == 'mean' :
            datas_gps = [(self.pts_fix[i].datas['lON'].mean(),self.pts_fix[i].datas['LAT'].mean()) for i in self.pts_fix]
        if process == 'first' :
            datas_gps = [(self.pts_fix[i].datas['lON'][0],self.pts_fix[i].datas['LAT'][0]) for i in self.pts_fix]

        #Ecriture dans un fichier
        f_out = open(name_out,'w')
        if format == 'txt':
            f_out.write("Lat_decim|Lon_decim\n")
            for i in datas_gps :
                f_out.write("%f|%f\n"%(i[1],i[0]))
        if format == 'kml':
            #GESTION DES ENTETES ET DES FOOTERS
            kmlHeader = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
             '<Document>\n'
             '<name>SECTION FIX</name>\n'
             )

            kmlFooter = ('</Document>\n'
                        '</kml>\n')

            lat = array(datas_gps).T[1]
            lon = array(datas_gps).T[0]
            name = m.r_[0:len(lon)]
            kml = ''
            for i in xrange(len(name)) :
                #tmp_lon = str(lon[i]).split('.')
                #tmp_lat = str(lat[i]).split('.')
                if (lon[i]!=self.pts_fix[0].badvalue and lat[i] != self.pts_fix[0].badvalue) :
                    kml += '<Placemark>\n'+'<name>'+str(self.ids[i])+'</name>\n'
                    kml += ('<Point>\n<coordinates>')
                    kml += (
                    '%f,%f,1\n'
                    ) %(lon[i], lat[i])
                    kml += ('</coordinates>\n</Point>\n')
                    kml += '</Placemark>\n'

            kml_final = kmlHeader + kml + kmlFooter

            #WRITE THE FILE
            f_out.write(kml_final)

        f_out.close()

    def DistGPSProj (self,Po,Pf,zone,process='mean') :
        """Fonction pour reprojeter les positions moyenne des pts fixes sur une direction moyennes
        Permet d'avoir une vrai distance à la berge

        [option]
        process : 'mean' [default] use the mean of GPS datas1D
        'first' use the first position
        """

        #MOYENNE DES POSITIONS DES POINTS FIXES
        dist_list = []
        for i in self.pts_fix:
            if process == 'mean' :
                self.pts_fix[i].datas['mlON'] = m.array(m.mean(self.pts_fix[i].datas['lON']))
                self.pts_fix[i].datas['mLAT'] = m.array(m.mean(self.pts_fix[i].datas['LAT']))
            if process == 'first' :
                self.pts_fix[i].datas['mlON'] = m.array(self.pts_fix[i].datas['lON'][0])
                self.pts_fix[i].datas['mLAT']  = m.array(self.pts_fix[i].datas['LAT'][0])

            #On projete
            dist, len_section = self.pts_fix[i].GPSProjDist(Po,Pf,zone,meanlatlon=True)
            dist_list.append(dist)

        self.dGPS = m.array(dist_list)
        self.lensection = len_section

        return self.dGPS

    def LoadBeamVelo(self,prefix,n_file,sufix='_ASC.TXT'):
        '''
            Fonction pour charger et convertir les vitesses radiales (issue de winriver avec un export ascii beam_velo1 -> beam_velo4 séparer par des ',')
            Cette fonction construit automatiquement la suite des noms de fichiers type:
                prefix + 000 + sufix
                prefix + 001 + sufix etc...
                
            Elle applique ensuite la fonction River.LoadBeamVelo pour charger et convertir le fichier
            
            TODO:
                COMPLETLY REWRITE THIS FUNCTION WITH SORT OF FOLDER LISTING TO GET FILE NAMES
                
            INPUTS:
                prefix = chemin pour le fichier jusqu'au numero
                n_file = number of files
                sufix [default='_ASC.TXT'] = fin du fichier
        '''
        
        for i in range(len(self.pts_fix)):
            if i < 10:
                n = '00'+str(i)
            else:
                n = '0'+str(i)
                
            self.pts_fix[i].LoadBeamVelo(prefix+n+sufix)
            self.pts_fix[i].MsqTerm(0,'Load beams velo %d'%i)

    def merge_with_theodo (self, array_of_theo_points, data_to_merge):
        """ Function to merge data from adcp section with theodolite points 
            based on the datetime of the theodolite points object.
        
            Inputs
            ------
            array_of_theo_points: is an array with theodolite point object (cf read_trimble.py for the definition of a theodolite point object)
            data_to_merge: (string) is the name of adcp data to merge 
            
            Examples
            --------
            
            merged_indices, merged_data = section.merge_with_theodo( array([pt1,pt2,...]), "VM")
            
            The linked pts_fix index is also stored in each theodo.point.adcp_id
            
        """
        
        theodo = array_of_theo_points
        dlabel = data_to_merge
        
        output_indices = []
        output_data = []
        output_good_id_theo = []
        
        #Create a table to store indices of valid linked data for each pts_fix
        for i in self.pts_fix:
            self.pts_fix[i].datas['indices_link_theodo'] = []
        #Loop over section fixed points to transform datetime in string without microseconds
        for i in self.pts_fix:
            self.pts_fix[i].datetime_str = m.array([date.strftime('%Y-%m-%d %H:%M:%S')  for date in self.pts_fix[i].datetime])
            
        #loop over time for each theodo points
        for i in xrange(len(theodo)):
            
            point = theodo[i]
            #loop over theodo points 
            not_find = True
            cpt_i = 0
            while not_find:
                ind_data_tmp = m.find( self.pts_fix[cpt_i].datetime_str == str(point.time) )
                
                if ( len(ind_data_tmp) == 0  and cpt_i < ( len(self.pts_fix) - 1 )  ):
                    cpt_i += 1
                else:
                    not_find = False
                    
                
            #store things
            if len(ind_data_tmp) == 0:
                #store the adcp point wich is linked to the theopoint through time
                point.adcp_id = None
                
            else:
                point.adcp_id = cpt_i
                output_indices.append( ind_data_tmp )
                #Sauvegarde des indices pour chaques pts_fix adcp
                self.pts_fix[point.adcp_id].datas['indices_link_theodo'].append( ind_data_tmp )
                
                #test si 2D ou 1D
                if self.pts_fix[cpt_i].datas[dlabel].ndim == 2:
                    output_data.append( m.mean( self.pts_fix[cpt_i].datas[dlabel][:,ind_data_tmp],1) )
                else:
                    output_data.append( m.mean( self.pts_fix[cpt_i].datas[dlabel][:,ind_data_tmp] ) )
                    
                output_good_id_theo.append( i )
                
        return output_indices, output_data, output_good_id_theo 
            
                
            
#CLASS POUR FAIRE DU MULTIPROCESSUS AVEC MYSQL
class threader(threading.Thread):


    def __init__(self,river_object,datas_to_load,meandir=True):
        threading.Thread.__init__(self, target=self.run)  #target indique le nom de la methode a lancer pour chaque thread
        self.river_in = river_object
        self.datas_in = datas_to_load
        self.meandir = meandir

    def run(self):
        #Methode a appliquer
        self.river_in.GetDatas(self.datas_in) #LES DONNEES CLASSIQUES
        self.river_in.FondMoy() #LE FOND
        self.river_in.tps = self.river_in.GetTime() #Le temps

        #Test pour savoir si on doit recupérer la vitesse moyenne
        if self.meandir == True :
            self.river_in.meandir = self.river_in.MeanDir()

        self.river_in.Dbclose()
        return self.river_in


class Adcp_Sql_Parser :
    """ Class doc
    Permet de construire des requetes groupées pour gagner du temps"""

    def __init__ (self,River,datas_in):
        """ Class initialiser
        permet de lancer la class en prenant comme entrée la class River et les datas à charger"""

        self.datas_to_load = datas_in
        self.riv = River
        #On lance la création de la requète
        self.build_sql_dict()

    def build_sql_dict (self) :

        """Methode qui construit le dico des données qui doit êtres récupérer de MYSQL"""

        #Initialisation de la list qui va contenir toutes les entrées
        self.sql_datas = []
        self.cpt2D = 0 #compteur de données 2D
        self.cpt1Dprof = 0 #compteur de données 1D de la table profileInfo
        self.cpt1Dens = 0 #compteur de données 1D de la table EnsembleInfo
        self.cpt1Depth = 0 #compteur de données 1D

        for i in self.datas_to_load.split(',') :

            dico_tmp = {} #on cree un dico temporaire qui permettra de stocker toutes les infos (Nom de variabe, shape:1D ou 2D et table) dans la liste globale

            #TEST SUR LE NOM DE LA VARIABLE

            #le cas des variables 2D qui sont tous dans la tables ADCPDatas
            if i in ['VM','VD','VVC','NVC','EVC','ERRV','PG','BCKSB1','BCKSB2','BCKSB3','BCKSB4','Q'] :
                dico_tmp = {'var_name':i,'table':'ADCPData','shape':2,'where':'Profcode'}
                self.cpt2D+=1

            #le cas des variables 1D dont la clause est sur Profcode (sauf 'DEPTH') et deux tables a regarder EnsembleInfo et ProfileInfo

            elif i in ['DEPTH']:
                dico_tmp = {'var_name':i,'table':'ADCPData','shape':1,'where':'Ensemblecode'}
                self.cpt1Depth+=1

            #cas des ProfileInfo
            elif i in ['DCL','BAT','DFCF','NPPE','TPE','PM','NDC','PM','comment'] :
                dico_tmp = {'var_name':i,'table':'ProfileInfo','shape':1,'where':'Profcode'}
                self.cpt1Dprof+=1

            #avec EnsembleInfo
            else:
                dico_tmp = {'var_name':i,'table':'EnsembleInfo','shape':1,'where':'Profcode'}
                self.cpt1Dens+=1

            self.sql_datas.append(dico_tmp) #on ajoute ce dico à la liste globale


        #Creation des requetes sql à partir de la liste

        #INITIALISATION SI LES COMPTEURS SONT PAS 0
        if self.cpt2D != 0:
            self.request_sql_2D = 'SELECT '
        if self.cpt1Dens != 0:
            self.request_sql_1Dens = 'SELECT '
        if self.cpt1Dprof != 0:
            self.request_sql_1Dprof = 'SELECT '
        if self.cpt1Depth != 0:
            self.request_sql_1Depth = 'SELECT '

        for i in self.sql_datas:
            #test 2D
            if i['shape'] == 2 :
                #Ajout à la requete
                self.request_sql_2D+=i['table']+'.'+i['var_name']+','

            if i['shape'] == 1 :
                #cas de depth
                if i['var_name'] == 'DEPTH' :
                    self.request_sql_1Depth+=i['table']+'.'+i['var_name']
                #cas profileInfo
                elif i['table'] == 'ProfileInfo' :
                    self.request_sql_1Dprof+=i['table']+'.'+i['var_name']+','
                #cas ensembleInfo
                else:
                    self.request_sql_1Dens+=i['table']+'.'+i['var_name']+','

        #FINALISATION DE LA REQUETE [-1] POUR ENLEVER LA DERNIèRE VIRGULE
        if self.cpt2D != 0:
            self.request_sql_2D = self.request_sql_2D[:-1]+' FROM ADCPData,EnsembleInfo WHERE ADCPData.Ensemblecode = EnsembleInfo.Ensemblecode AND EnsembleInfo.Profcode ='+str(self.riv.idriver)
        if self.cpt1Dens != 0:
            self.request_sql_1Dens = self.request_sql_1Dens[:-1]+' FROM EnsembleInfo WHERE EnsembleInfo.Profcode = '+str(self.riv.idriver)
        if self.cpt1Dprof != 0:
            self.request_sql_1Dprof = self.request_sql_1Dprof[:-1]+' FROM ProfileInfo WHERE ProfileInfo.Profcode = '+str(self.riv.idriverglobal)
        if self.cpt1Depth != 0:
            #Besoin de récupérer un ensemblecode
            #init Mysql cursor
            curs=self.riv.conn.cursor()
            curs.execute('SELECT Ensemblecode FROM EnsembleInfo WHERE Profcode='+str(self.riv.idriver)+' LIMIT 1')
            self.enscode=int(curs.fetchone()[0])
            curs.close()
            self.request_sql_1Depth = self.request_sql_1Depth+' FROM ADCPData WHERE ADCPData.Ensemblecode = '+str(self.enscode)

    def SqlRequest (self):

        #LES DONNEES 2D
        if self.cpt2D != 0:
            curs = self.riv.conn.cursor()
            curs.execute(self.request_sql_2D)
            datas2D = m.array(double(curs.fetchall()))
            datas2D = datas2D.T
            noms = [d[0] for d in curs.description]

            #WE NEED TO KNOW THE NUMBER OF BINS TO RESHAPE DATAS
            curs.execute('SELECT NBINS FROM EnsembleInfo WHERE Profcode='+str(self.riv.idriver)+' LIMIT 1')
            self.riv.nbins = int(curs.fetchone()[0])

            for i in xrange(len(noms)):
                b = datas2D[i].reshape(datas2D[i].size/self.riv.nbins,self.riv.nbins)
                #Put same bad value for all datas
                if noms[i] in ['VM','VD','EVC','NVC','VVC','ERRV']:
                    b[where(b==-32768)]=self.riv.badvalue
                if noms[i] in ['BCKSB1','BCKSB2','BCKSB3','BCKSB4']:
                    b[where(b==255)]=self.riv.badvalue

                self.riv.datas[noms[i]] = m.ma.masked_equal(b.T,self.riv.badvalue) #save the datas

            curs.close()

        #LES DONNEES 1D
        if self.cpt1Dens != 0:
            curs=self.riv.conn.cursor()
            curs.execute(self.request_sql_1Dens)
            datas1D=m.array(curs.fetchall())
            noms = [d[0] for d in curs.description]
            for i in xrange(len(noms)):
                b = datas1D.T[i]
                if noms[i] in ['DB1','DB2','DB3','DB4']:
                    b[where(b==-32768)]=self.riv.badvalue
                if noms[i] in ['lON','LAT']:
                    b[where(b==30000)] = self.riv.badvalue

                self.riv.datas[noms[i]] = m.ma.masked_equal(b,self.riv.badvalue)
            curs.close()

        if self.cpt1Dprof != 0:
            curs=self.riv.conn.cursor()
            curs.execute(self.request_sql_1Dprof)
            datas1Dp=m.array(curs.fetchall())
            noms = [d[0] for d in curs.description]
            for i in xrange(len(noms)):

                self.riv.datas[noms[i]] = datas1Dp.T[i]

            curs.close()

        #LA PROFONDEUR
        if self.cpt1Depth != 0:
            curs=self.riv.conn.cursor()
            curs.execute(self.request_sql_1Depth)
            self.riv.datas['DEPTH']=m.array(curs.fetchall())
            curs.close()

class merge ():
    """ 
       Class to manage merged profiles 
       
       NEED TO CHECK IF IT'S BUGGY!!! Hugo 11/02/2013
    """
    
    def __init__ ( self, profiles_list ):
        """ give list of profiles to merge """
        
        self.profiles = profiles_list
        self.MergeDataDict()
        
    def GetDatas( self, datasin ):
        
        for profile in self.profiles:
            profile.GetDatas(datasin)
        
        self.MergeDataDict()
        
    def MergeDataDict( self ):
        self.data = {}
        
        all_keys = self.profiles[0].datas.keys()
        
        for key in all_keys:
            self.data[key] = hstack( [ prof.datas[key].copy() for prof in self.profiles ] )
            
        
###################### FUNCTIONS #######################################
def LoadBeamVelo(pts_fix,fname):
    lenx = len(pts_fix.datas['DEPTH'])
    leny = len(pts_fix.datas['TDMG'])
    
    data_brut = loadtxt(fname,delimiter=',').T
    beam_velo = ma.masked_equal(data_brut.reshape(4,lenx,leny),-32768)
    
    #on enregistre
    pts_fix.datas['B1'] = beam_velo[0,:,:]
    pts_fix.datas['B2'] = beam_velo[1,:,:]
    pts_fix.datas['B3'] = beam_velo[2,:,:]
    pts_fix.datas['B4'] = beam_velo[3,:,:]

    #CALCUL DES COMPOSANTES DANS LE REF DE L'INSTRUMENT
    CC = 2 * cos(deg2rad(20))
    CS = 2 * sin(deg2rad(20))
    #U = B3+B4 / CS
    pts_fix.datas['W34i'] = (pts_fix.datas['B3']+pts_fix.datas['B4'])/CC
    pts_fix.datas['Ui'] = (pts_fix.datas['B3']-pts_fix.datas['B4'])/CS
    
    #PITCH CORRECTION
    #pp = arctan(tan(deg2rad(pts_fix.datas['PITCH']))*cos(deg2rad(pts_fix.datas['ROLL'])))
    pp = deg2rad(pts_fix.datas['PITCH'])
    CP = cos(pp)
    SP = sin(pp)
    pts_fix.datas['W34'] = CP * pts_fix.datas['W34i'] - SP * pts_fix.datas['Ui']
    pts_fix.datas['U'] = SP * pts_fix.datas['W34i'] + CP * pts_fix.datas['Ui']
    

def LatlonToXY (lat,lon,zone_in):
    """
        Convert lat lon from WGS84 to UTM regarding to zone_in given.
        
        Return xi, yi projected
    """
    
    #IMPORT DE LA BIBLIOTHEQUE pyproj pour gerer les projection
    from pyproj import Proj
    #init la projection
    p = Proj(proj='utm',zone=zone_in,ellps='WGS84')
    
    return  p(lat,lon)
        
########################################################################


#N=River(7)
#N.ShowProfil()

