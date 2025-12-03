// STM32L432KC_ADC.c
// Source code for ADC functions

#include "STM32L432KC_SPI.h"
#include "STM32L432KC_GPIO.h"

////////////////////////////////////////////////////////////////////////////////////////////////////
// PIO Helper Functions
////////////////////////////////////////////////////////////////////////////////////////////////////

//Clock setup
//Look at PLLSAI1config (generally adapt PLL code for the PLLSAI1)
//RCC->PLLSAI1ON
//Wait for RCC->PLLSAI1RDY
//Or MSI is automatically set to sysclk so just set clk to be sysclk?


//Reset ADC1_CCR CKMODe[1:0] bits (set them =00)
//Configure ADC1_CCR  PRESC[3:0] to divide clk by 256

//	- Currently assuming I can ignore AHB clock
//Power up
//	- Set DEPPWD = 0 (exit deep power down mode)
//	- SET ADVREGEN=1 (enable adc voltage reg)
//	- Wait for startup time to configure adc
//		○ Assuming also 20 microsec?
//	- Set ADEN=0 to disable ADC
//	- Optionally, disable voltage regulator w advregen=0
//CALIBRATE ADC
//	- Ensure DEEPPWD=0, ADVREGEN=1, Adc voltage reg startup time has elapsed
//		○ Initialize a timer, hit a delay? 20 microsec
//	- Ensure ADEN=0
//	- Program difsel[i] in adc_difsel
//	- Set Adcaldif=1 for differential input
//	- Wait for adcal=0
//	- Optionally read calibration factor from adc_calfact
//• Enable ADC
//	- Ensure DEPPWD =0 and ADVREGEN=1
//	- Clear ADC_ISR -> ADRDY by writing 1
//	- SET ADEN
//	- SET ADRDYIE=1 for interrupt
//	- Wait until adrdy=1 (ADC setup time will pass)
//	- Optionally, clear ADC_ISR->ADRDY by writing 1


void adcEnable(int port_id) {
  RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN;

}

/* Returns the port ID that corresponds to a given pin.
 *    -- pin: a GPIO pin ID, e.g. PA3
 *    -- return: a GPIO port ID, e.g. GPIO_PORT_ID_A */
int gpioPinOffset(int gpio_pin) {

}
