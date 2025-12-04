// STM32L432KC_ADC.c
// Source code for ADC functions
// Madeleine Kan mkan@hmc.edu 2025
// but made referencing code by Kavi Dey kdey@hmc.edu 2023

#include "STM32L432KC_ADC.h"


////////////////////////////////////////////////////////////////////////////////////////////////////
// PIO Helper Functions
////////////////////////////////////////////////////////////////////////////////////////////////////



void initADC(void) {
  ////////////////////
  // ENABLE ADC CLK //
  ////////////////////
  RCC -> AHB2ENR |= _VAL2FLD(RCC_AHB2ENR_ADCEN, 0b1); // enable adc clk
  RCC -> CCIPR |= _VAL2FLD(RCC_CCIPR_ADCSEL, ADC_CLKSRC_SYSCLK); // System clock selected as ADCs clock

  ////////////////
  // AWAKEN ADC //
  ////////////////
  ADC1->CR &= ~ADC_CR_DEEPPWD; // exit deep power down mode
  ADC1->CR |= ADC_CR_ADVREGEN; // enable adc voltage regulator
  //ADC1 -> CR |= _VAL2FLD(ADC_CR_DEEPPWD, 0b0); // exit deep power down mode
  //ADC1 -> CR |= _VAL2FLD(ADC_CR_ADVREGEN, 0b1); // enable adc voltage regulator
  ADC1 -> CFGR |= _VAL2FLD(ADC_CFGR_RES, ADC_6BIT_RES); // define resolution of conversion to be 6 bits

  // voltage regulator startup time = 20 us = 800 / 40 MHz
  volatile int x = 800;
  while (x-- > 0)
    __asm("nop");
 
  ///////////////////
  // CALIBRATE ADC //
  ///////////////////
  ADC1 -> CR |= _VAL2FLD(ADC_CR_ADCAL, 0b1); // write 1 to calibrate ADC, single-ended input
  while (_FLD2VAL(ADC_CR_ADCAL, ADC1->CR) != 0); // Wait until ADCAL is 0 (so ADC is calibrated)
  uint8_t calfact = _FLD2VAL(ADC_CALFACT_CALFACT_S, ADC1->CALFACT);
  printf("adc successfully calibrated! calibration factor: %x \n", calfact);

  //////////////// 
  // ENABLE ADC //
  ////////////////
  ADC1 -> ISR |= _VAL2FLD(ADC_ISR_ADRDY, 0b1); // clear adrdy 
  ADC1 -> CR |= _VAL2FLD(ADC_CR_ADEN, 0b1); // enable ADC
  ADC1 -> IER |= _VAL2FLD(ADC_IER_ADRDYIE, 0b1); //  An interrupt is generated when the ADRDY bit is set.
  while (_FLD2VAL(ADC_ISR_ADRDY, ADC1->ISR) != 1); // Wait until ADC is ready
  ADC1 -> ISR |= _VAL2FLD(ADC_ISR_ADRDY, 0b1); // clear adrdy 

  //////////////////
  // DISABLE ADC  //
  //////////////////
  //ADC1 -> CR |= _VAL2FLD(ADC_CR_ADDIS, 0b1); // disable ADC
  //while (_FLD2VAL(ADC_CR_ADEN, ADC1->CR) != 0); // waut until ADC is disabled

  
}

void initChannel(int channelNum){
  // regular group
  ADC1 -> SQR1 |= _VAL2FLD(ADC_SQR1_L, 0b0000); // 1 conversion
  // hopefully won't freak out if int bc all the top registers are 0...
  ADC1 -> SQR1 |= _VAL2FLD(ADC_SQR1_SQ1, channelNum); // set first conversion in reg seq to channelNum
}

volatile uint16_t readADC(int channelNum){
  // by default, exten=00 and extensel=0 (meaning software trigger mode) and cont=0 (single conversion mode)
  // this means adstart is cleared when eos is asserted

  ADC1 -> CR |= _VAL2FLD(ADC_CR_ADSTART, 0b1); // start regular channel conversion
  while (_FLD2VAL(ADC_ISR_EOS, ADC1->ISR) != 1); // wait for EOS flag to go high (end of conversion sequence reached)
  volatile uint16_t convertedVal = (uint16_t) _FLD2VAL(ADC_DR_RDATA, ADC1->DR); // read 16-bit ADC_DR register... clears EOC flag
  ADC1 -> ISR |= _VAL2FLD(ADC_ISR_EOS, 0b1); // software clear EOS flag

  return convertedVal;
}

