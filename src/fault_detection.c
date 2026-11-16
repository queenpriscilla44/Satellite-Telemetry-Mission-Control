
#include "fault_detection.h"
#include <stdio.h>

int detectFaults(struct Telemetry data)
{
    int faultLevel = FAULT_NONE;

    if (data.temperature > 50.0f || data.temperature < 0.0f) {
        printf("WARNING: Temperature outside normal range!\n");
        faultLevel = FAULT_WARNING;
    }

    if (data.battery_voltage < 6.0f) {
        printf("CRITICAL: Battery voltage too low!\n");
        faultLevel = FAULT_CRITICAL;
    }

    if (data.current > 3.0f) {
        printf("WARNING: Current consumption is high!\n");

        if (faultLevel < FAULT_WARNING)
            faultLevel = FAULT_WARNING;
    }

    if (data.altitude < 400.0f || data.altitude > 550.0f) {
        printf("WARNING: Altitude outside target range!\n");

        if (faultLevel < FAULT_WARNING)
            faultLevel = FAULT_WARNING;
    }

    if (data.gyroscope > 3.0f) {
        printf("WARNING: Excessive gyroscope movement!\n");

        if (faultLevel < FAULT_WARNING)
            faultLevel = FAULT_WARNING;
    }

    return faultLevel;
}
