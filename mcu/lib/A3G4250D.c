// Madeleine Kan, Sarah Yandell
// mkan@hmc.edu, syandell@hmc.edu
// 2025-11-14
// A3G425D.c
// Description: 

#include "A3G4250D.h"

#include <stdint.h>
#include <stdlib.h>

#include <stm32l432xx.h> // May need to change 

void a3g4250d_init(void) {
    // Ensure CS is low when idle
    digitalWrite(SPI_CE, 0);
    // Set inital 9-bit resolution
    a3g4250d_write_reg(A3G4250D_DEFAULT_CONFIG_9BIT);
}



static void a3g4250d_write_reg(uint8_t data) {
    digitalWrite(SPI_CE, 1);
    spiSendReceive((char)(0x80)); // A7=1 write
    spiSendReceive((char)data);
    digitalWrite(SPI_CE, 0);
    printf ("data: %d \n", data);
}
