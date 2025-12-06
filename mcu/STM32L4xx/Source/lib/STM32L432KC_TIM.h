
// Sarah Yandell
// syandell@hmc.edu
// 2025-11-05
// TIMER.h
// Description: Public definitions for TIM15 delay functions.

#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>


///////////////////////////////////////////////////////////////////////////////
// Definitions
///////////////////////////////////////////////////////////////////////////////

#define __IO volatile


// Base addresses
#define TIM15_BASE (0x40014000UL)

#define PSC_VAL 7999


///////////////////////////////////////////////////////////////////////////////
// Bitfield struct for TIM15
///////////////////////////////////////////////////////////////////////////////

typedef struct
{
  __IO uint32_t CR1;              /* Address offset: 0x00 */
  __IO uint32_t CR2;              /* Address offset: 0x04 */
  __IO uint32_t SMCR;             /* Address offset: 0x08 */
  __IO uint32_t DIER;             /* Address offset: 0x0C */
  __IO uint32_t SR;               /* Address offset: 0x10 */
  __IO uint32_t EGR;              /* Address offset: 0x14 */
  __IO uint32_t CCMR1_OUTPUT;     /* Address offset: 0x18 */
  __IO uint32_t CCMR1_INPUT;      /* Address offset: 0x1C */
  __IO uint32_t CCER;             /* Address offset: 0x20 */
  __IO uint32_t CNT;              /* Address offset: 0x24 */
  __IO uint32_t PSC;              /* Address offset: 0x28 */
  __IO uint32_t ARR;              /* Address offset: 0x2C */
  __IO uint32_t RCR;              /* Address offset: 0x30 */
  __IO uint32_t CCR1;             /* Address offset: 0x34 */
  __IO uint32_t CCR2;             /* Address offset: 0x38 */
  __IO uint32_t RESERVED0;        /* Address offset: 0x3C */
  __IO uint32_t RESERVED1;        /* Address offset: 0x40 */
  __IO uint32_t BTDR;             /* Address offset: 0x44 */
  __IO uint32_t DCR;              /* Address offset: 0x48 */
  __IO uint32_t DMAR;             /* Address offset: 0x4C */
  __IO uint32_t OR1;              /* Address offset: 0x50 */
  __IO uint32_t RESERVED3;        /* Address offset: 0x54 */ 
  __IO uint32_t RESERVED4;        /* Address offset: 0x58 */
  __IO uint32_t RESERVED5;        /* Address offset: 0x5C */                                                          
  __IO uint32_t OR2;              /* Address offset: 0x60 */                                     
} TIM_15_TypeDef;

#define TIM15 ((TIM_15_TypeDef *) TIM15_BASE)

///////////////////////////////////////////////////////////////////////////////
// Function prototypes
///////////////////////////////////////////////////////////////////////////////

void init_delay(void);
void delay(int song_dur);

#endif