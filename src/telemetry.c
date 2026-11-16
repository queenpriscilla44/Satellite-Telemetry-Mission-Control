
#include "telemetry.h"

int validateTelemetry(struct Telemetry data)
{
    if (data.temperature < -50.0f || data.temperature > 100.0f)
        return 0;

    if (data.battery_voltage < 0.0f || data.battery_voltage > 15.0f)
        return 0;

    if (data.current < 0.0f || data.current > 10.0f)
        return 0;

    if (data.altitude < 0.0f || data.altitude > 1000.0f)
        return 0;

    if (data.gyroscope < -20.0f || data.gyroscope > 20.0f)
        return 0;

    return 1;
}
