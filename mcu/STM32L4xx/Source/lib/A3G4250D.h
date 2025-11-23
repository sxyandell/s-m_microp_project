// Madeleine Kan, Sarah Yandell
// mkan@hmc.edu, syandell@hmc.edu
// 2025-11-14
// A3G425D.c
// Description: 

#ifndef A3G4250D_H
#define A3G4250D_H
#include <stdint.h>
#include <stdbool.h>
#include <stdbool.h>

// A3G4250D register map
#define A3G4250D_REG_WHO_AM_I     0x0F
#define A3G4250D_REG_CTRL1        0x20
#define A3G4250D_REG_CTRL2        0x21
#define A3G4250D_REG_CTRL3        0x22
#define A3G4250D_REG_CTRL4        0x23
#define A3G4250D_REG_CTRL5        0x24
#define A3G4250D_REG_OUT_X_L      0x28
#define A3G4250D_REG_OUT_Y_L      0x29
#define A3G4250D_REG_OUT_Z_L      0x2A
#define A3G4250D_REG_OUT_X_H      0x2B
#define A3G4250D_REG_OUT_Y_H      0x2C
#define A3G4250D_REG_OUT_Z_H      0x2D

#define A3G4250D_WHO_AM_I_VALUE   0xD3

void a3g_init(void);
void a3g_read_dsp(volatile int16_t *x_dsp, volatile int16_t *y_dsp, volatile int16_t *z_dsp);


#endif // A3G4250D_H