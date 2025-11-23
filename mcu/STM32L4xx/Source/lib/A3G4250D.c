// Madeleine Kan, Sarah Yandell
// mkan@hmc.edu, syandell@hmc.edu
// 2025-11-14
// A3G425D.c
// Description: 

#include "A3G4250D.h"

#include <stdint.h>
#include <stdio.h>
#include "STM32L432KC_SPI.h"
#include "STM32L432KC_GPIO.h"
#include "STM32L432KC_SPI.h"


static void a3g_write(uint8_t reg, uint8_t value) {
	digitalWrite(SPI_CE, 0);

	// write : [RW, MS, AD5, AD4, AD3, AD2, AD1, AD0]
	// RW = 0, MS = 0, AD = reg
	char write_address = (char) ((reg) & 0x3F);
	spiSendReceive(write_address);
	spiSendReceive((char)value);
	digitalWrite(SPI_CE, 1);
	//printf("wrote %d to %d\n", value, reg);
}

static volatile uint8_t a3g_read(uint8_t reg) {
	digitalWrite(SPI_CE, 0);
	// read : [RW, MS, AD5, AD4, AD3, AD2, AD1, AD0]
	// RW = 1, MS = 0, AD = reg (5:0)
	char send_address = (char) (0x80u | ((reg) & 0x3F));
	spiSendReceive(send_address);
	volatile uint8_t read = (uint8_t)spiSendReceive(0x00);
	digitalWrite(SPI_CE, 1);
        //printf("address being sent: %x\n", send_address);
	//printf("read %d from %x\n", read, reg);
	return read;
}


void a3g_init(void) {
	/// Ensure CS is high when idle
    digitalWrite(SPI_CE, 1);
	
	// Read WHO_AM_I
	volatile uint8_t who = a3g_read(A3G4250D_REG_WHO_AM_I);

	if (who != A3G4250D_WHO_AM_I_VALUE) {
		printf("who: %x \n", who);
                printf("WHO_AM_I mismatch\n");
	}

	// CTRL1 bits: [DDR1,DR0,BW1,BW0,PD,Zen,Yen,Xen] (7.2 in datasheet)
	// DR=01 (200 Hz), BW=10 (50 Hz cutoff), PD=1, Zen=Yen=Xen=1 => 01101111 => 0x6F
	a3g_write(A3G4250D_REG_CTRL1, 0x6F);

	// CTRL2 bits: [0, 0, HPM1, HPM1, HPC3, HPC2, HPC1, HPC0] (7.3 in datasheet)
	// HPM1=0, HPM0=0, HPC3=0, HPC2=0, HPC1=0, HPC0=0 => 00000000 => 0x00
	// leave default (HPF off)
	a3g_write(A3G4250D_REG_CTRL2, 0x00);

	// CTRL3 bits: [I1_Int1, I1_ Boot, H_Lactive, PP_OD, I2_DRDY, I2,WTM, I2_ORun, I2_Empty] (7.4 in datasheet)
	// no interrupts configured
	a3g_write(A3G4250D_REG_CTRL3, 0x00);

	// CTRL4 bits: [0, BLE, 0, 0, -, ST1, ST0, SIM] (7.5 in datasheet)
	// BLE=0 (LSB at lower address), ST=00, SIM=0 (4-wire SPI) => 00000000 => 0x00
	a3g_write(A3G4250D_REG_CTRL4, 0x00);

	// CTRL5 bits: [BOOT, FIFO_EN, -, HPen, INT_Sel1, INT_Sel0, OUT_Sel1, OUT_Sel0] (7.6 in datasheet)
	// BOOT = 0, FIFO_EN=0, HPen=0, INT_Sel1=0, INT_Sel0=0, OUT_Sel1=0, OUT_Sel0=0 => 00000000 => 0x00
	a3g_write(A3G4250D_REG_CTRL5, 0x00);
}

static void a3g_read_raw(volatile int16_t *x_raw, volatile int16_t *y_raw, volatile int16_t *z_raw) {
	volatile uint8_t OUT_X_L = a3g_read(A3G4250D_REG_OUT_X_L);
	volatile uint8_t OUT_X_H = a3g_read(A3G4250D_REG_OUT_X_H);
	volatile uint8_t OUT_Y_L = a3g_read(A3G4250D_REG_OUT_Y_L);
	volatile uint8_t OUT_Y_H = a3g_read(A3G4250D_REG_OUT_Y_H);
	volatile uint8_t OUT_Z_L = a3g_read(A3G4250D_REG_OUT_Z_L);
	volatile uint8_t OUT_Z_H = a3g_read(A3G4250D_REG_OUT_Z_H);
	*x_raw = (volatile int16_t)(OUT_X_L | (OUT_X_H << 8));
	*y_raw = (volatile int16_t)(OUT_Y_L | (OUT_Y_H << 8));
	*z_raw = (volatile int16_t)(OUT_Z_L | (OUT_Z_H << 8));
	//printf("raw: x: %d, y: %d, z: %d\n", *x_raw, *y_raw, *z_raw);
}

// try making xyz floats?
void a3g_read_dsp(volatile int16_t *x_dsp, volatile int16_t *y_dsp, volatile int16_t *z_dsp) {
	volatile int16_t x_raw = 0, y_raw = 0, z_raw = 0;
	a3g_read_raw(&x_raw, &y_raw, &z_raw);

	// Sensitivity 8.75 mdps/digit = 0.00875 dps/LSB
	// dps = raw * 0.00875
	*x_dsp = (volatile int16_t)(x_raw * 0.00875);
	*y_dsp = (volatile int16_t)(y_raw * 0.00875);
	*z_dsp = (volatile int16_t)(z_raw * 0.00875);
	//printf("dsp: x: %d, y: %d, z: %d\n", *x_dsp, *y_dsp, *z_dsp);
}
