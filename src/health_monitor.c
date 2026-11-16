
#include <stdio.h>
#include "health_monitor.h"

void displayHealthStatus(int faultLevel)
{
    printf("\n=== SATELLITE HEALTH STATUS ===\n");

    if (faultLevel == 0) {
        printf("STATUS: NORMAL\n");
        printf("Satellite is operating normally.\n");
    }
    else if (faultLevel == 1) {
        printf("STATUS: WARNING\n");
        printf("Attention required. Check sensor readings.\n");
    }
    else if (faultLevel == 2) {
        printf("STATUS: CRITICAL\n");
        printf("Immediate attention required!\n");
    }
    else {
        printf("STATUS: UNKNOWN\n");
    }
}
