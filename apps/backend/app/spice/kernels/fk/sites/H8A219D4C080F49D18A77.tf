KPL/FK
 
   FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/fk/sites/H8A219D4C080F49D18A77.tf
 
   This file was created by PINPOINT.
 
   PINPOINT Version 3.3.0 --- December 13, 2021
   PINPOINT RUN DATE/TIME:    2025-11-29T14:31:14
   PINPOINT DEFINITIONS FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/H8A219D4C080F49D18A77.defs
   PINPOINT PCK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/pck/pck00011.tpc
   PINPOINT SPK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/spk/sites/H8A219D4C080F49D18A77.spk
 
   The input definitions file is appended to this
   file as a comment block.
 
 
   Body-name mapping follows:
 
\begindata
 
   NAIF_BODY_NAME                      += 'H8A219D4C080F49D18A77'
   NAIF_BODY_CODE                      += 399901
 
\begintext
 
 
   Reference frame specifications follow:
 
 
   Topocentric frame H8A219D4C080F49D18A77_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame H8A219D4C080F49D18A77_TOPO is centered at the
      site H8A219D4C080F49D18A77, which has Cartesian coordinates
 
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
 
   FRAME_H8A219D4C080F49D18A77_TOPO    =  1399901
   FRAME_1399901_NAME                  =  'H8A219D4C080F49D18A77_TOPO'
   FRAME_1399901_CLASS                 =  4
   FRAME_1399901_CLASS_ID              =  1399901
   FRAME_1399901_CENTER                =  399901
 
   OBJECT_399901_FRAME                 =  'H8A219D4C080F49D18A77_TOPO'
 
   TKFRAME_1399901_RELATIVE            =  'EARTH_FIXED'
   TKFRAME_1399901_SPEC                =  'ANGLES'
   TKFRAME_1399901_UNITS               =  'DEGREES'
   TKFRAME_1399901_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399901_ANGLES              =  ( -355.9790000000000,
                                             -47.7796200000000,
                                             180.0000000000000 )
 
\begintext
 
 
Definitions file /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/H8A219D4C080F49D18A77.defs
--------------------------------------------------------------------------------
 
begindata
 
SITES = ( 'H8A219D4C080F49D18A77' )
 
H8A219D4C080F49D18A77_CENTER = 399
H8A219D4C080F49D18A77_FRAME  = 'EARTH_FIXED'
H8A219D4C080F49D18A77_IDCODE = 399901
H8A219D4C080F49D18A77_XYZ = ( +4718.939486765214, -331.71847758159765, +4263.763301726129 )
H8A219D4C080F49D18A77_BOUNDS = ( @1000-JAN-01, @3000-JAN-01 )
H8A219D4C080F49D18A77_UP = 'Z'
H8A219D4C080F49D18A77_NORTH = 'X'
 
begintext
 
begintext
 
[End of definitions file]
 
