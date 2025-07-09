#ifndef SETTINGS_H_
#define SETTINGS_H_

// Defining macros for all PCF8574 Pins
#define P0                         0
#define P1                         1
#define P2                         2
#define P3                         3
#define P4                         4
#define P5                         5
#define P6                         6
#define P7                         7

// EEPROM Settings
#define EEPROM_SIZE                100
#define MAX_STRING_SIZE            50

// TFT Settings
#define TFT_CS                     15
#define TFT_DC                     2
#define TFT_RESET                  0

// RELAY Settings
#define RELAY1                     P0
#define RELAY2                     P1

// BUTTON Settings
#define BUTTON1                    P2
#define BUTTON2                    P3
#define BUTTON3                    P4

// Module Pins
#define DHT_PIN                    12
#define LDR_PIN                    A0

// PROGRAM CONSTANTS
#define TEMPERATURE_THRESHHOLD     25
#define LIGHT_INTENSITY_THRESHHOLD 100
#define BACKGROUND_COLOR           0

#endif