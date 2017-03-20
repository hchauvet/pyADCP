-- phpMyAdmin SQL Dump
-- version 3.4.5deb1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le : Ven 13 Avril 2012 à 15:36
-- Version du serveur: 5.1.62
-- Version de PHP: 5.3.6-13ubuntu3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: `BaseADCP`
--

-- --------------------------------------------------------

--
-- Structure de la table `ADCPData`
--

CREATE TABLE IF NOT EXISTS `ADCPData` (
  `Dcode` int(11) NOT NULL AUTO_INCREMENT,
  `Ensemblecode` int(11) NOT NULL,
  `DEPTH` float NOT NULL,
  `VM` float NOT NULL,
  `VD` float NOT NULL,
  `EVC` float NOT NULL,
  `NVC` float NOT NULL,
  `VVC` float NOT NULL,
  `ERRV` float NOT NULL,
  `BCKSB1` float NOT NULL,
  `BCKSB2` float NOT NULL,
  `BCKSB3` float NOT NULL,
  `BCKSB4` float NOT NULL,
  `PG` float NOT NULL,
  `Q` float NOT NULL,
  PRIMARY KEY (`Dcode`),
  KEY `IND_ens` (`Ensemblecode`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

-- --------------------------------------------------------

--
-- Structure de la table `EnsembleInfo`
--

CREATE TABLE IF NOT EXISTS `EnsembleInfo` (
  `Profcode` int(11) NOT NULL,
  `Ensemblecode` int(11) NOT NULL AUTO_INCREMENT,
  `ETYear` int(11) DEFAULT NULL,
  `ETMonth` int(11) DEFAULT NULL,
  `ETDay` int(11) DEFAULT NULL,
  `ETHour` int(11) DEFAULT NULL,
  `ETMin` int(11) DEFAULT NULL,
  `ETSec` int(11) DEFAULT NULL,
  `ETHund` int(11) DEFAULT NULL,
  `ENum` int(11) DEFAULT NULL,
  `NES` int(11) DEFAULT NULL,
  `PITCH` float DEFAULT NULL,
  `ROLL` float DEFAULT NULL,
  `CORRHEAD` float DEFAULT NULL,
  `ADCPTemp` float DEFAULT NULL,
  `BTVelE` float DEFAULT NULL,
  `BTVelN` float DEFAULT NULL,
  `BTVelUp` float DEFAULT NULL,
  `BTVelErr` float DEFAULT NULL,
  `CBD` float DEFAULT NULL,
  `GGAA` float DEFAULT NULL,
  `GGAD` float DEFAULT NULL,
  `GGAHDOP` float DEFAULT NULL,
  `DB1` float DEFAULT NULL,
  `DB2` float DEFAULT NULL,
  `DB3` float DEFAULT NULL,
  `DB4` float DEFAULT NULL,
  `TED` float DEFAULT NULL,
  `TET` float DEFAULT NULL,
  `TDTN` float DEFAULT NULL,
  `TDTE` float DEFAULT NULL,
  `TDMG` float DEFAULT NULL,
  `LAT` double DEFAULT NULL,
  `lON` double DEFAULT NULL,
  `NDInv` float DEFAULT NULL,
  `NDfnvu` float DEFAULT NULL,
  `NDfnvu2` float DEFAULT NULL,
  `DVMP` float DEFAULT NULL,
  `DVTP` float DEFAULT NULL,
  `DVBP` float DEFAULT NULL,
  `DVSSDE` float DEFAULT NULL,
  `DVSD` float DEFAULT NULL,
  `DVESDE` float DEFAULT NULL,
  `DVED` float DEFAULT NULL,
  `SDML` float DEFAULT NULL,
  `SDBL` float DEFAULT NULL,
  `NBINS` int(11) DEFAULT NULL,
  `MU` varchar(2) DEFAULT NULL,
  `VR` varchar(3) DEFAULT NULL,
  `IU` varchar(6) DEFAULT NULL,
  `ISF` float DEFAULT NULL,
  `SAF` float DEFAULT NULL,
  PRIMARY KEY (`Ensemblecode`),
  KEY `IND_Ens_Prof` (`Profcode`,`Ensemblecode`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

-- --------------------------------------------------------

--
-- Structure de la table `Metatable`
--

CREATE TABLE IF NOT EXISTS `Metatable` (
  `metaID` int(11) NOT NULL AUTO_INCREMENT,
  `TabName` varchar(50) NOT NULL,
  `FieldName` varchar(50) NOT NULL,
  `FieldDes` blob,
  PRIMARY KEY (`metaID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

-- --------------------------------------------------------

--
-- Structure de la table `ProfileInfo`
--

CREATE TABLE IF NOT EXISTS `ProfileInfo` (
  `Profcode` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Profcode pour mode Bt',
  `rivername` varchar(55) DEFAULT NULL,
  `DCL` int(11) NOT NULL,
  `BAT` int(11) NOT NULL,
  `DFCF` int(11) NOT NULL,
  `NDC` int(11) DEFAULT NULL,
  `NPPE` int(11) DEFAULT NULL,
  `TPE` int(11) DEFAULT NULL,
  `PM` int(11) DEFAULT NULL,
  `comment` blob,
  `Type` int(11) NOT NULL DEFAULT '0' COMMENT '0 space 1 time',
  `GGAcode` int(11) NOT NULL DEFAULT '0' COMMENT 'Profcode pour le mode GGA',
  `VTGcode` int(11) NOT NULL DEFAULT '0' COMMENT 'Profcode pour le mode VTG',
  PRIMARY KEY (`Profcode`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

-- --------------------------------------------------------


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
