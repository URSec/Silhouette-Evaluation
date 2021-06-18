/* Common main.c for the benchmarks

   Copyright (C) 2014 Embecosm Limited and University of Bristol
   Copyright (C) 2018 Embecosm Limited

   Contributor: James Pallister <james.pallister@bristol.ac.uk>
   Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>

   This file is part of the Bristol/Embecosm Embedded Benchmark Suite.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.

   SPDX-License-Identifier: GPL-3.0-or-later */

/*
 * Copyright (C) 2019, 2020 University of Rochester
 *
 * Modified to work with Silhouette evaluation by: Zhuojia Shen
 */

#include "stm32f4xx.h"
#include "stm32469i_discovery.h"

#include "support.h"

#ifndef BENCHMARK_NAME
#error "Please define BENCHMARK_NAME!"
#endif

extern int initialise_benchmark(void);
extern int verify_benchmark(int unused);

int main(void)
{
	int i;
	volatile int result = 0;
	int correct;

	uint32_t t_start, t;

	printf("Start to run %s.\n", BENCHMARK_NAME);

	t_start = HAL_GetTick();
	for (i = 0; i < REPEAT_FACTOR; i++) {
		initialise_benchmark();
		asm volatile ("" :: "r" (result) : "memory");
		result = benchmark();
		asm volatile ("" :: "r" (result) : "memory");
	}
	t = HAL_GetTick() - t_start;

	switch (verify_benchmark(result)) {
	case 1:
		printf("Finished in %u ms.", t);
		break;
	case -1:
		printf("Finished in %u ms, but no verify_benchmark() run.", t);
		break;
	default:
		printf("Finished in %u ms, but verify_benchmark() found errors.", t);
		break;
	}
	printf("\n");

	return 0;
}
