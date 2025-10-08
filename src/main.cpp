#include "CelestialEvents.h"

int main() {
    CelestialEvents::load_kernels();
    CelestialEvents::occulation();
    CelestialEvents::unload_kernels();
    return 0;
}
