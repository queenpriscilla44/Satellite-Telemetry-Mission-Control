



#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

#include "sensors.h"
#include "telemetry.h"
#include "fault_detection.h"
#include "health_monitor.h"


/* Save telemetry readings to CSV */
void saveTelemetry(struct Telemetry satellite,
                   int valid,
                   int faultLevel)
{
    FILE *file = fopen("telemetry.csv", "a+");

    if (file == NULL) {
        printf("Error: Could not open telemetry.csv\n");
        return;
    }

    /* Check whether the CSV file is empty */
    fseek(file, 0, SEEK_END);

    if (ftell(file) == 0) {
        fprintf(file,
            "Time,Temperature,Battery Voltage,Current,"
            "Altitude,Gyroscope,Validity,Fault Level\n");
    }

    /* Generate timestamp */
    time_t now = time(NULL);
    struct tm *local = localtime(&now);
    char timestamp[30];

    if (local != NULL) {
        strftime(timestamp, sizeof(timestamp),
                 "%Y-%m-%d %H:%M:%S", local);
    } else {
        snprintf(timestamp, sizeof(timestamp), "Unknown");
    }

    /* Write sensor readings */
    fprintf(file,
        "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%s,%d\n",
        timestamp,
        satellite.temperature,
        satellite.battery_voltage,
        satellite.current,
        satellite.altitude,
        satellite.gyroscope,
        valid ? "VALID" : "INVALID",
        faultLevel
    );

    fclose(file);

    printf("\nTelemetry saved to telemetry.csv\n");
}


/* Main program */
int main(void)
{
    srand((unsigned int)time(NULL));

    printf("=== SATELLITE TELEMETRY LIVE SYSTEM ===\n");
    printf("Generating new telemetry every 2 seconds...\n");
    printf("Press Ctrl + C to stop.\n");
    
    while (1)
    {
        struct Telemetry satellite = generateTelemetry();
        
        printf("\n====================================\n");
        printf("NEW SATELLITE TELEMETRY READING\n");
        printf("====================================\n");

        printf("Temperature     : %.2f C\n", satellite.temperature);
        printf("Battery Voltage : %.2f V\n", satellite.battery_voltage);
        printf("Current         : %.2f A\n", satellite.current);
        printf("Altitude        : %.2f km\n", satellite.altitude);
        printf("Gyroscope       : %.2f deg/s\n", satellite.gyroscope);

        int faultLevel = -1;
        int valid = validateTelemetry(satellite);

        if (valid)
        {
            printf("\nTelemetry data is valid.\n");

            faultLevel = detectFaults(satellite);
            displayHealthStatus(faultLevel);
        }
        else
        {
            printf("\nINVALID TELEMETRY DATA!\n");
            printf("Fault analysis skipped.\n");
        }

        saveTelemetry(satellite, valid, faultLevel);

        Sleep(2000);
    }

    return 0;
}
