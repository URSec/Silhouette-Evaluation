/*
 * Copyright (C) 2019, 2020 University of Rochester
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "stm32f4xx.h"

//=============================================================================
// System clock configuration
//=============================================================================

void Error_Handler(void)
{
	while (1) {
	}
}

/*
 * @brief  System Clock Configuration
 * @param  None
 * @retval None
 */
__attribute__((section("privileged_functions")))
void SystemClock_Config(void)
{
	RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
	RCC_OscInitTypeDef RCC_OscInitStruct = {0};

	/* Enable Power Control clock */
	__HAL_RCC_PWR_CLK_ENABLE();

	/*
	 * The voltage scaling allows optimizing the power consumption when the
	 * device is clocked below the maximum system frequency, to update the
	 * voltage scaling value regarding system frequency refer to product
	 * datasheet.
	 */
	__HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

	/* Enable HSE Oscillator and activate PLL with HSE as source */
	RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
	RCC_OscInitStruct.HSIState = RCC_HSI_ON;
	RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
	RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
	RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
	RCC_OscInitStruct.PLL.PLLM = 8;
	RCC_OscInitStruct.PLL.PLLN = 180;
	RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
	RCC_OscInitStruct.PLL.PLLQ = 4;
	RCC_OscInitStruct.PLL.PLLR = 2;
	if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
		Error_Handler();
	}

	/* Activate the OverDrive to reach the 180 MHz Frequency */
	if (HAL_PWREx_EnableOverDrive() != HAL_OK) {
		Error_Handler();
	}

	/*
	 * Select PLL as system clock source and configure the HCLK, PCLK1 and
	 * PCLK2 clocks dividers.
	 */
	RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_SYSCLK |
				      RCC_CLOCKTYPE_HCLK |
				      RCC_CLOCKTYPE_PCLK1 |
				      RCC_CLOCKTYPE_PCLK2;
	RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
	RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
	RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
	RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;
	if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK) {
		Error_Handler();
	}
}

//=============================================================================
// Console USART configuration
//=============================================================================

UART_HandleTypeDef huart3;

__attribute__((section("privileged_functions")))
void Console_UART_Init(void)
{
	GPIO_InitTypeDef gpio_init_structure = {0};

	/* Enable USART clock */
	__HAL_RCC_USART3_CLK_ENABLE();

	/* Enable GPIO clock */
	__HAL_RCC_GPIOB_CLK_ENABLE();

	/* Configure USART Tx & Rx as alternate function */
	gpio_init_structure.Pin = GPIO_PIN_10 | GPIO_PIN_11;
	gpio_init_structure.Mode = GPIO_MODE_AF_PP;
	gpio_init_structure.Speed = GPIO_SPEED_FREQ_HIGH;
	gpio_init_structure.Pull = GPIO_PULLUP;
	gpio_init_structure.Alternate = GPIO_AF7_USART3;
	HAL_GPIO_Init(GPIOB, &gpio_init_structure);

	/* USART configuration */
	huart3.Instance = USART3;
	huart3.Init.BaudRate = 115200;
	huart3.Init.WordLength = UART_WORDLENGTH_8B;
	huart3.Init.StopBits = UART_STOPBITS_1;
	huart3.Init.Parity = UART_PARITY_NONE;
	huart3.Init.Mode = UART_MODE_TX_RX;
	huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
	huart3.Init.OverSampling = UART_OVERSAMPLING_16;
	if (HAL_UART_Init(&huart3) != HAL_OK) {
		Error_Handler();
	}
}

/*
 * @brief  Retargets the C library printf function to the USART.
 * @param  None
 * @retval None
 */
#ifdef __GNUC__
/* With GCC, small printf (option LD Linker->Libraries->Small printf
   set to 'Yes') calls __io_putchar() */
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif /* __GNUC__ */
PUTCHAR_PROTOTYPE
{
	/*
	 * Place your implementation of fputc here.
	 * e.g. write a character to the USART and Loop until the end of
	 * transmission.
	 */
	HAL_StatusTypeDef status;
	status = HAL_UART_Transmit(&huart3, (uint8_t *)&ch, 1, 0xFFFF);
	return status == HAL_OK ? ch : 0;
}

//=============================================================================
// MPU configuration
//=============================================================================

#define MPU_RN_FLASH	MPU_REGION_NUMBER0
#define MPU_RN_RAM	MPU_REGION_NUMBER1
#define MPU_RN_CCMRAM	MPU_REGION_NUMBER2
#define MPU_RN_SDRAM	MPU_REGION_NUMBER3
#define MPU_RN_SS	MPU_REGION_NUMBER4

extern uint8_t _FLASH_segment_start[];
extern uint8_t _FLASH_segment_end[];
extern uint8_t _RAM_start[];
extern uint8_t _RAM_end[];
extern uint8_t _CCMRAM_start[];
extern uint8_t _CCMRAM_end[];
extern uint8_t _SDRAM_start[];
extern uint8_t _SDRAM_end[];
extern uint8_t _shadow_stack_start[];
extern uint8_t _shadow_stack_end[];

__attribute__((section("privileged_functions")))
void MPU_Init(void)
{
	MPU_Region_InitTypeDef flash = {0};
	MPU_Region_InitTypeDef ram = {0};
	MPU_Region_InitTypeDef ccmram = {0};
	MPU_Region_InitTypeDef sdram = {0};
	MPU_Region_InitTypeDef shadowstack = {0};

	uint8_t usr_ro_perm = MPU_REGION_PRIV_RO_URO;	/* User & kernel RO */
	uint8_t prv_no_perm = MPU_REGION_NO_ACCESS;	/* User & kernel NA */
#ifdef SS_FLIP_USER_KERNEL_PERM
	uint8_t usr_rw_perm = MPU_REGION_PRIV_RW;	/* Kernel RW */
	uint8_t prv_rw_perm = MPU_REGION_FULL_ACCESS;	/* User & kernel RW */
#else
	uint8_t usr_rw_perm = MPU_REGION_FULL_ACCESS;	/* User & kernel RW */
	uint8_t prv_rw_perm = MPU_REGION_PRIV_RW;	/* Kernel RW */
#endif

	if ((MPU->TYPE >> 8) < 5) {
		Error_Handler();
	}

	/* Setup MPU for the flash region */
	flash.Enable = MPU_REGION_ENABLE;
	flash.Number = MPU_RN_FLASH;
	flash.BaseAddress = (uint32_t)_FLASH_segment_start;
	flash.Size = MPU_REGION_SIZE_2MB;
	flash.AccessPermission = usr_ro_perm;
	flash.DisableExec = MPU_INSTRUCTION_ACCESS_ENABLE;
	flash.IsShareable = MPU_ACCESS_SHAREABLE;
	flash.IsCacheable = MPU_ACCESS_CACHEABLE;
	flash.IsBufferable = MPU_ACCESS_BUFFERABLE;
	HAL_MPU_ConfigRegion(&flash);

	/* Setup MPU for the RAM region */
	ram.Enable = MPU_REGION_ENABLE;
	ram.Number = MPU_RN_RAM;
	ram.BaseAddress = (uint32_t)_RAM_start;
	ram.Size = MPU_REGION_SIZE_512KB;
	ram.SubRegionDisable = 0xe0; /* Last 3 subregions exceeding 320 KB */
	ram.AccessPermission = usr_rw_perm;
	ram.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;
	ram.IsShareable = MPU_ACCESS_SHAREABLE;
	ram.IsCacheable = MPU_ACCESS_CACHEABLE;
	ram.IsBufferable = MPU_ACCESS_BUFFERABLE;
	HAL_MPU_ConfigRegion(&ram);

	/* Setup MPU for the CCMRAM region */
	ccmram.Enable = MPU_REGION_ENABLE;
	ccmram.Number = MPU_RN_CCMRAM;
	ccmram.BaseAddress = (uint32_t)_CCMRAM_start;
	ccmram.Size = MPU_REGION_SIZE_64KB;
	ccmram.AccessPermission = usr_rw_perm;
	ccmram.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;
	ccmram.IsShareable = MPU_ACCESS_SHAREABLE;
	ccmram.IsCacheable = MPU_ACCESS_CACHEABLE;
	ccmram.IsBufferable = MPU_ACCESS_BUFFERABLE;
	HAL_MPU_ConfigRegion(&ccmram);

	/* Setup MPU for the SDRAM region */
	sdram.Enable = MPU_REGION_ENABLE;
	sdram.Number = MPU_RN_SDRAM;
	sdram.BaseAddress = (uint32_t)_SDRAM_start;
	sdram.Size = MPU_REGION_SIZE_16MB;
	sdram.SubRegionDisable = 0x80; /* Last subregion for shadow stack */
	sdram.AccessPermission = usr_rw_perm;
	sdram.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;
	sdram.IsShareable = MPU_ACCESS_SHAREABLE;
	sdram.IsCacheable = MPU_ACCESS_CACHEABLE;
	sdram.IsBufferable = MPU_ACCESS_BUFFERABLE;
	HAL_MPU_ConfigRegion(&sdram);

	/* Setup MPU for the shadow stack region */
	shadowstack.Enable = MPU_REGION_ENABLE;
	shadowstack.Number = MPU_RN_SS;
	shadowstack.BaseAddress = (uint32_t)_shadow_stack_start;
	shadowstack.Size = MPU_REGION_SIZE_2MB;
	shadowstack.AccessPermission = prv_rw_perm;
	shadowstack.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;
	shadowstack.IsShareable = MPU_ACCESS_SHAREABLE;
	shadowstack.IsCacheable = MPU_ACCESS_CACHEABLE;
	shadowstack.IsBufferable = MPU_ACCESS_BUFFERABLE;
	HAL_MPU_ConfigRegion(&shadowstack);

	/*
	 * Now enable MPU with:
	 * (1) Default memory map as a background region for privileged access
	 * (2) Using MPU for memory accesses by handlers
	 */
	HAL_MPU_Enable(MPU_CTRL_PRIVDEFENA_Msk | MPU_CTRL_HFNMIENA_Msk);
}
