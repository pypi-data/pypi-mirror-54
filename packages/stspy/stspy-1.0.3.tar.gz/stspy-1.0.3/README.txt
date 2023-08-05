#####################    STSPY    #########################

Version = 1.0.3

Scanning Tunneling Spectra Python Analysis

Establishes a python class called spectra object with relevant parameters automatically tabulated (and optionally an STM object described below)

In addition, adds a specgrid object which contains similar attributes

To load a spectra from a VERT file, just do: spec = stspy.load_VERT_file(filename)
To load a specgrid file, do: specgrid = stspy.load_specgrid_file(filename) #filename is the .specgridfile, dat file is required to be in the same place as the .specgridfile, but isn't included in the arugment

Spectra (and specgrid) objects have a variety of attributes. 

Automatically pulls parameters of particular importance including:
ZPiezoconst
LockinAmpl

Once called, spectra object contains has the following properties:
V: sample voltage (volts)
z: (Angstroms)
I: current (amps)
dIdV: differential conductance (mV)

Methods available:
average(hyst_cor = True): if there are multiple passes, averages the spectra back and forth. hyst_cor (default True) applies a correction accounting for differences upon sweeping
normalize(kappa): if using a z-ramp, this is useful. Multiplies the current and conductance by exp(-2*kappa*z) where kappa is a provided number (or array same length as z) to be determined by measurement




Another python class is created called STM which has the following properties and default values:
DAC_Voltage_Range = 20000.0: Voltage range of the DAC in mV (i.e. 10V - (-10V) = 20V = 20000mV)
LockinRC_facotr = 7960.0: Mutliplicative factor to get LockinRC param in Hz

Adjust values of this object to account for different STM or versions of stmafm software

Version log:
0.1.0 - Implemented specgrid reader and changed VERT file load syntax
0.1.1 - Small correction for when hyst factor was odd
0.1.2 - Small correction when loading voltage from specgrid file
0.1.3 - Introduced compatability with STMAFM 4.0 Beta version where repeated spectra are labeled as .BAK files
0.1.4 - Added x, y, Length_x, and Length_y properties of spectra, to be used for line spectra profile cuts
1.0.0 - Updated load file speed and upgraded for Python 3 compatibility
1.0.2 - Updated to fix small bug and included a feature to allow d2IdV2 to be read from files
1.0.3 - Updated to fix small bug when averaging d2IdV2