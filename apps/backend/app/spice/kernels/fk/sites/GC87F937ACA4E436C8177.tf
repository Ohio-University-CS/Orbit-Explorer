KPL/FK
 
   FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/fk/sites/GC87F937ACA4E436C8177.tf
 
   This file was created by PINPOINT.
 
   PINPOINT Version 3.3.0 --- December 13, 2021
   PINPOINT RUN DATE/TIME:    2025-11-29T00:24:48
   PINPOINT DEFINITIONS FILE: /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/GC87F937ACA4E436C8177.defs
   PINPOINT PCK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/pck/pck00011.tpc
   PINPOINT SPK FILE:         /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/kernels/spk/sites/GC87F937ACA4E436C8177.spk
 
   The input definitions file is appended to this
   file as a comment block.
 
 
   Body-name mapping follows:
 
\begindata
 
   NAIF_BODY_NAME                      += 'GC87F937ACA4E436C8177'
   NAIF_BODY_CODE                      += 399901
 
\begintext
 
 
   Reference frame specifications follow:
 
 
   Topocentric frame GC87F937ACA4E436C8177_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame GC87F937ACA4E436C8177_TOPO is centered at the
      site GC87F937ACA4E436C8177, which has Cartesian coordinates
 
         X (km):                  0.4242264633896E+04
         Y (km):                 -0.1871503882359E+04
         Z (km):                  0.4364960886646E+04
 
      and planetodetic coordinates
 
         Longitude (deg):       -23.8050000000000
         Latitude  (deg):        43.4627790000000
         Altitude   (km):         0.0000000000000E+00
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame EARTH_FIXED.
 
 
\begindata
 
   FRAME_GC87F937ACA4E436C8177_TOPO    =  1399901
   FRAME_1399901_NAME                  =  'GC87F937ACA4E436C8177_TOPO'
   FRAME_1399901_CLASS                 =  4
   FRAME_1399901_CLASS_ID              =  1399901
   FRAME_1399901_CENTER                =  399901
 
   OBJECT_399901_FRAME                 =  'GC87F937ACA4E436C8177_TOPO'
 
   TKFRAME_1399901_RELATIVE            =  'EARTH_FIXED'
   TKFRAME_1399901_SPEC                =  'ANGLES'
   TKFRAME_1399901_UNITS               =  'DEGREES'
   TKFRAME_1399901_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399901_ANGLES              =  ( -336.1950000000000,
                                             -46.5372210000000,
                                             180.0000000000000 )
 
\begintext
 
 
Definitions file /home/jim/Documents/Classes/CS3560/Orbit-Explorer/apps/backend/app/spice/temp/GC87F937ACA4E436C8177.defs
--------------------------------------------------------------------------------
 
begindata
 
SITES = ( 'GC87F937ACA4E436C8177' )
 
GC87F937ACA4E436C8177_CENTER = 399
GC87F937ACA4E436C8177_FRAME  = 'EARTH_FIXED'
GC87F937ACA4E436C8177_IDCODE = 399901
GC87F937ACA4E436C8177_XYZ = ( +4242.264633896088, -1871.5038823589368, +4364.96088664552 )
GC87F937ACA4E436C8177_BOUNDS = ( @1000-JAN-01, @3000-JAN-01 )
GC87F937ACA4E436C8177_UP = 'Z'
GC87F937ACA4E436C8177_NORTH = 'X'
 
begintext
 
begintext
 
[End of definitions file]
 
