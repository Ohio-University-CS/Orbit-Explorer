KPL/FK
 
   FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/fk/sites/S00B99E3A66D2436FA49E.tf
 
   This file was created by PINPOINT.
 
   PINPOINT Version 3.3.0 --- December 13, 2021
   PINPOINT RUN DATE/TIME:    2025-11-29T16:25:49
   PINPOINT DEFINITIONS FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/S00B99E3A66D2436FA49E.defs
   PINPOINT PCK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/pck/pck00011.tpc
   PINPOINT SPK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/spk/sites/S00B99E3A66D2436FA49E.spk
 
   The input definitions file is appended to this
   file as a comment block.
 
 
   Body-name mapping follows:
 
\begindata
 
   NAIF_BODY_NAME                      += 'S00B99E3A66D2436FA49E'
   NAIF_BODY_CODE                      += 399901
 
\begintext
 
 
   Reference frame specifications follow:
 
 
   Topocentric frame S00B99E3A66D2436FA49E_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame S00B99E3A66D2436FA49E_TOPO is centered at the
      site S00B99E3A66D2436FA49E, which has Cartesian coordinates
 
         X (km):                  0.4718939486765E+04
         Y (km):                 -0.3317184775816E+03
         Z (km):                  0.4263763301726E+04
 
      and planetodetic coordinates
 
         Longitude (deg):        -4.0210000000000
         Latitude  (deg):        42.2203800000000
         Altitude   (km):         0.9990430231232E-12
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame EARTH_FIXED.
 
 
\begindata
 
   FRAME_S00B99E3A66D2436FA49E_TOPO    =  1399901
   FRAME_1399901_NAME                  =  'S00B99E3A66D2436FA49E_TOPO'
   FRAME_1399901_CLASS                 =  4
   FRAME_1399901_CLASS_ID              =  1399901
   FRAME_1399901_CENTER                =  399901
 
   OBJECT_399901_FRAME                 =  'S00B99E3A66D2436FA49E_TOPO'
 
   TKFRAME_1399901_RELATIVE            =  'EARTH_FIXED'
   TKFRAME_1399901_SPEC                =  'ANGLES'
   TKFRAME_1399901_UNITS               =  'DEGREES'
   TKFRAME_1399901_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399901_ANGLES              =  ( -355.9790000000000,
                                             -47.7796200000000,
                                             180.0000000000000 )
 
\begintext
 
 
Definitions file /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/S00B99E3A66D2436FA49E.defs
--------------------------------------------------------------------------------
 
begindata
 
SITES = ( 'S00B99E3A66D2436FA49E' )
 
S00B99E3A66D2436FA49E_CENTER = 399
S00B99E3A66D2436FA49E_FRAME  = 'EARTH_FIXED'
S00B99E3A66D2436FA49E_IDCODE = 399901
S00B99E3A66D2436FA49E_XYZ = ( +4718.939486765214, -331.71847758159765, +4263.763301726129 )
S00B99E3A66D2436FA49E_BOUNDS = ( @1000-JAN-01, @3000-JAN-01 )
S00B99E3A66D2436FA49E_UP = 'Z'
S00B99E3A66D2436FA49E_NORTH = 'X'
 
begintext
 
begintext
 
[End of definitions file]
 
