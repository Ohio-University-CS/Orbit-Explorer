//https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/

/*
Notable celestial events
- lunar eclipse
    - Penumbral, Partial, Total, Central, Selenelion
- full moon
- new moon
- supermoon
- blue moon
- lunar occulation
- Planetary retrograde motion
- solar eclipse
    - Total, Annular, Partial, Hybrid, 
- meteor shower
    - meteor outbursts
- comet appearances
- asteroid flybys
- conjuctions
*/
#include "SpiceUsr.h"
#include <stdio.h>
#include <math.h>

#define KERNELS_F "src/kernels/kernels.tm"

class CelestialEvents {
public:
    static void load_kernels();
    static void unload_kernels();
    static void occulation();
private:
    bool kernels_loaded;
};