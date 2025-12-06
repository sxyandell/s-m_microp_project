
#include "lib/STM32L432KC.h"
#include <stdint.h>

// Choose the output pin for the square wave
// Change this if your buzzer/speaker is on a different pin
#define TONE_OUT_PIN PA5
                              //  0     1     2      3    4     5     6     7
// Switch mapping (active-low):   red   brown yellow blue black red gray white
static const int switch_pins[8] = {PA12, PB0, PB4,   PB6, PA1,  PA0,  PA3,  PA8 };

// Half-periods (microseconds) for notes: C4, D4, E4, F4, G4, A4, B4, C5
// C4=261.63Hz, D4=293.66, E4=329.63, F4=349.23, G4=392.00, A4=440.00, B4=493.88, C5=523.25
static const uint16_t half_us[8] = { 1911, 1703, 1517, 1432, 1276, 1136, 1012, 955 };

// Configure TIM2 for ~1us tick, and provide a local delay_us using TIM2
static void tim2_setup_1us(void) {
	// Enable TIM2 clock
	RCC->APB1ENR1 |= RCC_APB1ENR1_TIM2EN;
	// Set prescaler for 1 MHz timer clock (1 tick = 1us)
	uint32_t psc_div = (uint32_t)(SystemCoreClock / 1000000UL);
	TIM2->PSC = (psc_div > 0 ? (psc_div - 1) : 0);
	// Update, enable counter
	TIM2->EGR |= TIM_EGR_UG;
	TIM2->CR1 |= TIM_CR1_CEN;
}

static void delay_us(uint32_t us) {
	TIM2->ARR = us;
	TIM2->EGR |= TIM_EGR_UG;   // Force update so ARR takes effect
	TIM2->SR &= ~TIM_SR_UIF;   // Clear update flag
	TIM2->CNT = 0;             // Reset counter
	while ((TIM2->SR & TIM_SR_UIF) == 0) {
		// wait
	}
}

// Configure internal pull-ups for the specified pins (active-low switches)
static void enable_pullups_for_switches(void) {
	// PA12, PA8
	GPIOA->PUPDR &= ~(0x3u << (2 * 12));
	GPIOA->PUPDR |=  (0x1u << (2 * 12)); // pull-up
	GPIOA->PUPDR &= ~(0x3u << (2 * 8));
	GPIOA->PUPDR |=  (0x1u << (2 * 8));  // pull-up
        GPIOA->PUPDR &= ~(0x3u << (2 * 0));
	GPIOA->PUPDR |=  (0x1u << (2 * 0)); // pull-up
        GPIOA->PUPDR &= ~(0x3u << (2 * 1));
	GPIOA->PUPDR |=  (0x1u << (2 * 1)); // pull-up
        GPIOA->PUPDR &= ~(0x3u << (2 * 3));
	GPIOA->PUPDR |=  (0x1u << (2 * 3)); // pull-up
	// PB0, PB1, PB6, PB7
	GPIOB->PUPDR &= ~(0x3u << (2 * 0));
	GPIOB->PUPDR |=  (0x1u << (2 * 0));  // pull-up
	GPIOB->PUPDR &= ~(0x3u << (2 * 6));
	GPIOB->PUPDR |=  (0x1u << (2 * 6));  // pull-up
        GPIOB->PUPDR &= ~(0x3u << (2 * 4));
	GPIOB->PUPDR |=  (0x1u << (2 * 4));  // pull-up
}

int main(void) {
	configureFlash();
	configureClock();

	// Enable GPIO ports A, B, C
	gpioEnable(GPIO_PORT_A);
	gpioEnable(GPIO_PORT_B);
	gpioEnable(GPIO_PORT_C);

	// Set switch pins as inputs (active-low)
	for (int i = 0; i < 8; i++) {
		pinMode(switch_pins[i], GPIO_INPUT);
		printf("switch_pins %d\n", switch_pins[i]);

	}
	// Enable internal pull-ups (if external pull-ups are present, this is harmless)
	enable_pullups_for_switches();

	// Configure tone output pin
	pinMode(TONE_OUT_PIN, GPIO_OUTPUT);
	digitalWrite(TONE_OUT_PIN, 0);

	// Configure TIM2 to provide microsecond delays
	tim2_setup_1us();

	int count = 0;
	while (1) {
		int handled = 0;
		for (int i = 0; i < 8; i++) {
			printf("i %d\n", i);
                        delay_us(5000);
			// Active-low read: 0 means pressed
			if (digitalRead(switch_pins[i]) == 0) {
				// Debounce: confirm still pressed after 5 ms
				delay_us(5000);
				if (digitalRead(switch_pins[i]) == 0) {
					handled = 1;
					printf("handled %d\n", i);
					// Play tone while the same key remains pressed; ignore others
					const uint16_t h = half_us[i];
					while (digitalRead(switch_pins[i]) == 0) {
						togglePin(TONE_OUT_PIN);
						//printf("togglePin %d\n", count);
						count++;
						delay_us(h);
					}
					// Key released; ensure output low and debounce release
                                        printf("release %d\n", i);
					digitalWrite(TONE_OUT_PIN, 0);
					delay_us(10000);
					break;
				}
			}
		}

		if (!handled) {
			// Idle
			digitalWrite(TONE_OUT_PIN, 0);
		}
	}
}