#!/usr/bin/env python
from __future__ import division
import subprocess
import glob
from os import system
import sys
from os import mkdir
from os.path import exists
from array import array
import math
import re
import time
import datetime
from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,kGreen,kOrange,kSpring,TF1,kAzure, TH2F,TH1F,gPad, TPaveText, TH1,kRed,SetOwnership, TMath
from collections import OrderedDict


berror = False

signal_much_norm = {}
signal_ech_norm = {}
mean_value = {}
mean_error = {}
sigma_value = {}
sigma_error = {}

bg3p_v = {}

bg3p_err = {}



bkg_much_norm = 0
bkg_ech_norm = 0
number_of_channels = 2
number_of_backgrounds = 1

#year = "2016v3"
#year = "2017v2"
year = "2018"

all_years_eaul = True
rate_unc = 1.15
lumi_unc = 1.025
if "2017" in year: lumi_unc = 1.023
if "2016" in year and not all_years_eaul: rate_unc = 1.05
if "2017" in year and not all_years_eaul: rate_unc = 1.15
if "2018" in year and not all_years_eaul: rate_unc = 1.12


# Find all possible MT where we have the normalisation
inputfile = open("AnalysisOutput_"+year+".txt","r")
listOfLines = inputfile.readlines()
i=0
for line in listOfLines:
    if "Muon" in line and "Signal" not in line:
        muon_norm_line =  listOfLines[i+1].strip()
        bkg_much_norm = muon_norm_line.split("N = ")[1]

    if "Electron" in line and "Signal" not in line:
        elec_norm_line =  listOfLines[i+1].strip()
        bkg_ech_norm = elec_norm_line.split("N = ")[1]
        
    if "Muon" in line and "Signal" in line:
        for j in range(i+1,len(listOfLines)):
            if "Electron" in listOfLines[j]: break
            mass = re.findall(r'\d+.\d+',listOfLines[j])[0]
            norm = re.findall(r'\d+.\d+',listOfLines[j])[1]
            signal_much_norm[mass] = norm
            mean_value[mass] = re.findall(r'\d+.\d+',listOfLines[j])[2]
            mean_error[mass] = re.findall(r'\d+.\d+',listOfLines[j])[3]

            sigma_value[mass] = re.findall(r'\d+.\d+',listOfLines[j])[4]
            sigma_error[mass] = re.findall(r'\d+.\d+',listOfLines[j])[5]

    if "Electron" in line and "Signal" in line:
        for j in range(i+1,len(listOfLines)):
            mass = re.findall(r'\d+.\d+',listOfLines[j])[0]
            norm = re.findall(r'\d+.\d+',listOfLines[j])[1]
            signal_ech_norm[mass] = norm

    if "Bg" in line:
        for j in range(i+1,len(listOfLines)):
            if "bg" in listOfLines[j]:
                value = re.findall(r'[-+]?\d+.\d+',listOfLines[j])[0]
                error = re.findall(r'[-+]?\d+.\d+',listOfLines[j])[1]
                key = listOfLines[j].split("  ")[0]
                
                bg3p_v[key] = value
                bg3p_err[key] = error
                
        

    i+=1 

# open file to write
for mass in signal_much_norm:
    outputfile = open("Datacard_"+year+"_M"+str(mass)+".txt",'w')
    outputfile.write("# Version of the 36/pb SingleTth Analysis \n\n")
    outputfile.write("------------------------------ \n")
    outputfile.write("imax  "+str(number_of_channels)+" number of channels \n")
    outputfile.write("jmax  "+str(number_of_backgrounds)+" number of backgrounds \n")
    outputfile.write("kmax  * number of nuisance parameters (sources of systematical uncertainties) \n \n")
    outputfile.write("------------------------------ \n")
    outputfile.write("shapes * * ws_SingleTth_"+str(year)+".root SingleTth:$PROCESS_$CHANNEL \n \n")
    outputfile.write("------------------------------ \n")
    outputfile.write("# name of channels, and number of observed events (total number of event in Data) \n \n")
    outputfile.write("bin            ech            much \n")
    outputfile.write("observation    -1             -1 \n \n")
    outputfile.write("------------------------------ \n")
    outputfile.write("# name of the channel you are considering, name of the process (signal,bkg,...),\n # process unique ID (positive number for backgrounds, and zero or negative for signal)\n # expected events for each process (total number of events in MC)\n \n")
    outputfile.write("bin            ech         ech            much      much \n")
#    outputfile.write("process        MT600       Bkgfunc        MT600     Bkgfunc \n")
#    outputfile.write("process        MT600       roomultipdf        MT600     roomultipdf \n")
    outputfile.write("process        roomultipdf_MT"+str(mass)+"       roomultipdf        roomultipdf_MT"+str(mass)+"     roomultipdf \n")
    outputfile.write("process        0           1              0         1 \n")
    outputfile.write("rate           "+str(signal_ech_norm[mass])+"     "+str(bkg_ech_norm)+"          "+str(signal_much_norm[mass])+"   "+str(bkg_much_norm)+" \n \n")
    outputfile.write("------------------------------ \n")
    outputfile.write("# list of independent sources of uncertainties, and give their effect (syst. error) \n \n")
    outputfile.write("lumi     lnN   "+str(lumi_unc)+"       -    "+str(lumi_unc)+" - \n ")
    outputfile.write("rate_signal     lnN    "+str(rate_unc)+"       -    "+str(rate_unc)+" - \n ")
    outputfile.write("pdf_index_much discrete \n ")
    outputfile.write("pdf_index_ech discrete \n ")
    outputfile.write("pdf_index_MT"+str(mass)+"_much discrete \n ")
    outputfile.write("pdf_index_MT"+str(mass)+"_ech discrete \n ")
    outputfile.write("sg_mean param "+str(mean_value[mass])+"  "+str(mean_error[mass])+" \n ")
    outputfile.write("sg_sigma param "+str(sigma_value[mass])+"  "+str(sigma_error[mass])+" \n ")
    for key in bg3p_v:
        outputfile.write(str(key) +" param "+str(bg3p_v[key])+"  "+str(bg3p_err[key])+" \n ")
    outputfile.write("------------------------------ \n")



    outputfile.close()
