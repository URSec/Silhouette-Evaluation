/**
  ******************************************************************************
  * @file    main.c
  * @author  Ac6
  * @version V1.0
  * @date    01-December-2013
  * @brief   Default main function.
  ******************************************************************************
*/

/* Includes ------------------------------------------------------------------*/
#include "main.h"

#include <stdio.h>

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

char PinRxBuffer[PINRXBUFFSIZE];
char key[32];
char key_in[32];
char pin[] = "1995";

/* Private function prototypes -----------------------------------------------*/
static void Error_Handler(void);
static void Program_Init(void);
static void print(char *, int len);
/* Private functions ---------------------------------------------------------*/

void lock(void)
{
	BSP_LED_Off(LED4);
}

void unlock(void)
{
	BSP_LED_On(LED4);
}

void rx_from_uart(uint32_t size)
{
	if (size > PINRXBUFFSIZE) {
		Error_Handler();
	}

	scanf("%s", PinRxBuffer);
}

/**
  * @brief  Main program
  * @param  None
  * @retval None
  */
int main(void)
{
	int len;
	int unlock_count = 0;

	unsigned int one = 1;
	unsigned int exp;
	unsigned int ms;
	static char locked[] = "System Locked\n";
	static char enter[] = "Enter Pin:\n";
	static char unlocked[] = "Unlocked\n";
	static char incorrect[] = "Incorrect Pin\n";
	static char waiting[] = "Waiting...\n";
	static char lockout[] = "System Lockout\n";

	uint32_t t;

	printf("Start to run %s\n", BENCHMARK_NAME);
	t = HAL_GetTick();

	Program_Init();
	mbedtls_sha256(pin, PINBUFFSIZE, key, 0);
	while (1) {
		lock();
		print(locked, sizeof(locked));
		unsigned int failures = 0;
		// In Locked State
		while (1) {
			print(enter, sizeof(enter));
			rx_from_uart(5);
			// Hash password received from UART
			mbedtls_sha256(PinRxBuffer, PINRXBUFFSIZE, key_in, 0);
			int i;
			for (i = 0; i < 32; i++) {
				if (key[i] != key_in[i]) {
					break;
				}
			}
			if (i == 32) {
				print(unlocked, sizeof(unlocked));
				unlock_count++;
				if (unlock_count >= 100) {
					goto out;
				}
				break;
			}

			failures++; // Increment number of failures
			print(incorrect, sizeof(incorrect));
			if (failures > 500 && failures <= 510) {
				// Essentially 2^failures
				exp = one << failures;
				// After 5 tries, start waiting around 5 secs
				// and then doubles
				ms = 78 * exp;
				print(waiting, sizeof(waiting));
				HAL_Delay(ms);
			} else if (failures > 1000) {
				print(lockout, sizeof(lockout));
				while (1) {
				}
			}

		}

		unlock();
		// Wait for lock command
		while (1) {
			rx_from_uart(2);
			if (PinRxBuffer[0] == '0') {
				break;
			}
		}
		lock();
	}

out:
	t = HAL_GetTick() - t;
	printf("Elapsed time: %u ms\n", t);

	// Backup while loop
	while (1) {
	}
}


// Call all initializations for program

static void Program_Init(void)
{
	/* Configure LEDs */
	BSP_LED_Init(LED4);
	BSP_LED_Init(LED3);
	BSP_LED_Init(LED2);
	BSP_LED_Init(LED1);

	/* No buffering of input */
	setbuf(stdin, NULL);
}

static void print(char * str, int len)
{
	printf("%s", str);
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  None
  * @retval None
  */
static void Error_Handler(void)
{
	/* Turn LED3 on */
	BSP_LED_On(LED3);
	while (1) {
	}
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t * file, uint32_t line)
{
	/* User can add his own implementation to report the file name and line number,
	   ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */

	/* Infinite loop */
	while (1) {
	}
}
#endif

/******************END OF FILE****/
