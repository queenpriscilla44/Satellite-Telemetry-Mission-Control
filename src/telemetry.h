#ifndef TELEMETRY_H
#define TELEMETRY_H

struct Telemetry {
    float temperature;
    float battery_voltage;
    float current;
    float altitude;
    float gyroscope;
};

int validateTelemetry(struct Telemetry data);

#endif