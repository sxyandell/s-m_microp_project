//  read A3G4250D over SPI and print angular velocity (dps)

#include "STM32L4xx/Source/lib/STM32L432KC.h"
#include "source/lib/A3G4250D.h"
#include <stdint.h>
#include <stdio.h>



int main(void) {

	configureFlash();
	configureClock();
        
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    initTIM(TIM15);
=======
        initTIM(TIM15);
>>>>>>> Stashed changes
=======
        initTIM(TIM15);
>>>>>>> Stashed changes
	// Initialize SPI: BR=0b011 (fclk/16, 16MHz -> 1MHz) (max 10 MHz), CPOL=1, CPHA=1 
	// clock idle high, data captured on rising edge
	// CHECK IF CORRECT
	initSPI(0b011, 1, 1);
	
	a3g_init();

	while (1) {
		float x = 0, y = 0, z = 0;
		a3g_read_dsp(&x, &y, &z);
		printf("Angular velocity: X=%d Y=%d Z=%d dps\n", x, y, z);
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        delay_millis(TIM15, 200);
=======
                delay_millis(TIM15, 500);
>>>>>>> Stashed changes
=======
                delay_millis(TIM15, 500);
>>>>>>> Stashed changes

	}
}

