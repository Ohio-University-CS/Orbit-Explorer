KPL/FK
 
   FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/fk/sites/F6E43606D6D034D768D23.tf
 
   This file was created by PINPOINT.
 
   PINPOINT Version 3.3.0 --- December 13, 2021
   PINPOINT RUN DATE/TIME:    2025-11-29T19:13:31
   PINPOINT DEFINITIONS FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/F6E43606D6D034D768D23.defs
   PINPOINT PCK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/pck/pck00011.tpc
   PINPOINT SPK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/spk/sites/F6E43606D6D034D768D23.spk
 
   The input definitions file is appended to this
   file as a comment block.
 
 
   Body-name mapping follows:
 
\begindata
 
   NAIF_BODY_NAME                      += 'F6E43606D6D034D768D23'
   NAIF_BODY_CODE                      += 399901
 
\begintext
 
 
   Reference frame specifications follow:
 
 
   Topocentric frame F6E43606D6D034D768D23_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame F6E43606D6D034D768D23_TOPO is centered at the
      site F6E43606D6D034D768D23, which has Cartesian coordinates
 
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
 
   FRAME_F6E43606D6D034D768D23_TOPO    =  1399901
   FRAME_1399901_NAME                  =  'F6E43606D6D034D768D23_TOPO'
   FRAME_1399901_CLASS                 =  4
   FRAME_1399901_CLASS_ID              =  1399901
   FRAME_1399901_CENTER                =  399901
 
   OBJECT_399901_FRAME                 =  'F6E43606D6D034D768D23_TOPO'
 
   TKFRAME_1399901_RELATIVE            =  'EARTH_FIXED'
   TKFRAME_1399901_SPEC                =  'ANGLES'
   TKFRAME_1399901_UNITS               =  'DEGREES'
   TKFRAME_1399901_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399901_ANGLES              =  ( -355.9790000000000,
                                             -47.7796200000000,
                                             180.0000000000000 )
 
\begintext
 
 
Definitions file /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/F6E43606D6D034D768D23.defs
--------------------------------------------------------------------------------
 
begindata
 
SITES = ( 'F6E43606D6D034D768D23' )
 
F6E43606D6D034D768D23_CENTER = 399
F6E43606D6D034D768D23_FRAME  = 'EARTH_FIXED'
F6E43606D6D034D768D23_IDCODE = 399901
F6E43606D6D034D768D23_XYZ = ( +4718.939486765214, -331.71847758159765, +4263.763301726129 )
F6E43606D6D034D768D23_BOUNDS = ( @1000-JAN-01, @3000-JAN-01 )
F6E43606D6D034D768D23_UP = 'Z'
F6E43606D6D034D768D23_NORTH = 'X'
 
begintext
 
begintext
 
[End of definitions file]
 
