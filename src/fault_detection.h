
#ifndef FAULT_DETECTION_H
#define FAULT_DETECTION_H

#include "telemetry.h"

#define FAULT_NONE     0
#define FAULT_WARNING  1
#define FAULT_CRITICAL 2

int detectFaults(struct Telemetry data);

#endif
