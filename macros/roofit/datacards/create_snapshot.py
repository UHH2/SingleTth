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
from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,kGreen,kOrange,kSpring,TF1,kAzure, TH2F,TH1F,gPad, TPaveText, TH1,kRed,SetOwnership, TMath,TTree, RooRealVar,RooPlot,RooDataHist,RooDataSet, kBlue, kDashed, TTree, kTRUE, kBlack,RooArgSet
from collections import OrderedDict
import argparse
import CMSPlotStyle

parser = argparse.ArgumentParser(description='Plot the signal strength.')
parser.add_argument('-mass', metavar='N', type=int, help='Mass of the signal sample')
parser.add_argument('-signalstrength', metavar='N', type=float,help='Signal Strength of the signal sample')

args = parser.parse_args()
mass = args.mass
signal = args.signalstrength


w_f = TFile.Open('higgsCombineinitial_signal'+str(signal)+'_'+str(mass)+'.FitDiagnostics.mH120.root')
w = w_f.Get('w')
fr_f = TFile.Open('fitDiagnosticsinitial_signal'+str(signal)+'_'+str(mass)+'.root')
fr = fr_f.Get('fit_b')
myargs = RooArgSet(fr.floatParsFinal())
w.saveSnapshot('initialFit',myargs, True)
fout = TFile('initialFitWorkspace.root',"recreate")
fout.WriteTObject(w,'w')
fout.Close()
