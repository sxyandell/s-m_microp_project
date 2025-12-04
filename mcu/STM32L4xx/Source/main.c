//  read A3G4250D over SPI and print angular velocity (dps)

#include "main.h"

// initializes ADC and desired channel
// also maps GPIO PA0 to ADC_IN5
// returns ADC pin equivalent to gpio pin
int ADC(int pin){
    pinMode(pin, GPIO_ANALOG); // configure PA0 as analog pin
    initADC();
    int adc_in;
    switch (pin) {
      case(PA0): adc_in = ADC_PA0;
      case(PA1): adc_in = ADC_PA1;
      case(PA2): adc_in = ADC_PA2;
      case(PA3): adc_in = ADC_PA3;
      case(PA4): adc_in = ADC_PA4;
      case(PA5): adc_in = ADC_PA5;
      case(PA6): adc_in = ADC_PA6;
      case(PA7): adc_in = ADC_PA7;
      case(PB0): adc_in = ADC_PB0;
      case(PB1): adc_in = ADC_PB1;
      default: adc_in = ADC_PA0;
    }
    initChannel(adc_in);
    return adc_in;

}


int main(void) {

	configureFlash();
        // dont need this bc it sets PLL as clk source
	configureClock();

      
        // initialize GPIOA,B,C
        gpioEnable(GPIO_PORT_A);
        gpioEnable(GPIO_PORT_B);
        gpioEnable(GPIO_PORT_C);
        RCC->AHB2ENR |= (RCC_AHB2ENR_GPIOAEN | RCC_AHB2ENR_GPIOBEN | RCC_AHB2ENR_GPIOCEN );

        // initialize timer
        RCC->APB1ENR1 |= RCC_APB1ENR1_TIM2EN;
        initTIM(TIM2);

	// initialize SPI: BR=0b011 (fclk/16, 16MHz -> 1MHz) (max 10 MHz), CPOL=1, CPHA=1
	initSPI(0b011, 1, 1);

	// initialize gyro
	a3g_init();
        volatile int16_t x = 0, y = 0, z = 0;


        // config ADC
        int adc_in = ADC(ADC_GPIO_PIN); // ADC_PA0 -> ADC1_IN5
        volatile uint16_t adc_out;


	while (1) {
		a3g_read_dsp(&x, &y, &z);
		printf("Angular velocity: X=%d Y=%d Z=%d dps\n", x, y, z);
                adc_out = readADC(adc_in);
                printf("adc reading: %d \n", adc_out);
                delay_millis(TIM2, 500);
	}
}

