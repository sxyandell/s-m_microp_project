// STM32L432KC_ADC.h
// Header for ADC functions

#ifndef STM32L4_ADC_H
#define STM32L4_ADC_H

#include <stdint.h> // Include stdint header
#include <stm32l432xx.h>

///////////////////////////////////////////////////////////////////////////////
// Definitions
///////////////////////////////////////////////////////////////////////////////

// Values which "val" can take on in digitalWrite()
#define ADC_CLKSRC_NOCLK 0b00
#define ADC_CLKSRC_PLLSAI1 0b01
#define ADC_CLKSRC_SYSCLK 0b11

#define ADC_12BIT_RES 0b00
#define ADC_10BIT_RES 0b01
#define ADC_8BIT_RES 0b10
#define ADC_6BIT_RES 0b11

#define ADC_PA0 5 // ADC1_IN5
#define ADC_PA1 6 // ADC1_IN6
#define ADC_PA2 7 // ADC1_IN7
#define ADC_PA3 8 // ADC1_IN8
#define ADC_PA4 9 // ADC1_IN9
#define ADC_PA5 10 // ADC1_IN10
#define ADC_PA6 11 // ADC1_IN11
#define ADC_PA7 12 // ADC1_IN12
#define ADC_PB0 15 // ADC1_IN5
#define ADC_PB1 16 // ADC1_IN16


///////////////////////////////////////////////////////////////////////////////
// Function prototypes
///////////////////////////////////////////////////////////////////////////////

void initADC(void);
void initChannel(int channelNum);
volatile uint16_t readADC(int channelNum);

#endif