#include "CelestialEvents.h"

void CelestialEvents::load_kernels() {
    furnsh_c(KERNELS_F);
}

void CelestialEvents::unload_kernels() {
    unload_c(KERNELS_F);
}

void CelestialEvents::occulation() {
    SpiceDouble starg[6];
    SpiceDouble lt;

    //distance to sun
    spkezr_c(
        "SUN",
        1759252916,
        "J2000",
        "NONE",
        "EARTH",
        starg,
        &lt
    );

    printf("Earth to sun..\n");
    printf("Position (km): %f %f %f\n", starg[0], starg[1], starg[2]);
    printf("Velocity (km/sec): %f %f %f\n", starg[3], starg[4], starg[5]);
    printf("Light time (s): %f\n", lt);

    SpiceDouble values[3];
    SpiceInt dim;

    //get sun radii
    bodvrd_c(
        "SUN",
        "RADII",
        3,
        &dim,
        values
    );

    printf("Sun radii: %f %f %f\n", values[0], values[1], values[2]);

    //sun limb from viewpoint

    SpiceEllipse limb;
    SpiceDouble viewpt [3] = { -starg[0], -starg[1], -starg[2] };
    edlimb_c(
        values[0],
        values[1],
        values[2],
        viewpt,
        &limb
    );

    SpiceDouble ecentr[3];
    SpiceDouble smajor[3];
    SpiceDouble sminor[3];
    el2cgv_c ( &limb, ecentr, smajor, sminor );

    printf( "Limb ellipse as seen from viewpoint:\n" );
    printf( "   Semi-minor axis: %10.6f %10.6f %10.6f\n",
                    sminor[0], sminor[1], sminor[2] );
    printf( "   Semi-major axis: %10.6f %10.6f %10.6f\n",
                    smajor[0], smajor[1], smajor[2] );
    printf( "   Center         : %10.6f %10.6f %10.6f\n",
                    ecentr[0], ecentr[1], ecentr[2] );

}