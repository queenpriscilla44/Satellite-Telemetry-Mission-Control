
#include <stdlib.h>

#include "sensors.h"

static float randomFloat(float min, float max)
{
    return min + ((float)rand() / RAND_MAX) * (max - min);
}

struct Telemetry generateTelemetry(void)
{
    struct Telemetry data;

    data.temperature = randomFloat(15.0f, 65.0f);
    data.battery_voltage = randomFloat(5.5f, 9.0f);
    data.current = randomFloat(0.5f, 4.0f);
    data.altitude = randomFloat(350.0f, 600.0f);
    data.gyroscope = randomFloat(0.0f, 5.0f);

    return data;
}
