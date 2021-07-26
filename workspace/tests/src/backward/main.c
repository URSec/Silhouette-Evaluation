/*
 * Copyright (C) 2021 University of Rochester
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

#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

void foo(void);
void bar(void);
void baz(void);

void __attribute__((noinline))
foo(void)
{
	bar();

	/* A failed return address corruption will lead us here */
	printf("Backward edge corruption failed!\n");
}

register char * stack_ptr asm ("sp");

void __attribute__((noinline))
bar(void)
{
	uintptr_t * retaddrslot = (unsigned *)stack_ptr;
	void * retaddr = __builtin_extract_return_addr(__builtin_return_address(0));
	int dummy = isatty(0); /* Make sure a stack frame is set up */

	/* Find the return address slot */
	while (dummy && *retaddrslot != (uintptr_t)retaddr) {
		++retaddrslot;
	}

	/* Corrupt the return address to have it point to baz() */
	*retaddrslot = (uintptr_t)&baz;
}

void __attribute__((noinline))
baz(void)
{
	/* A successful return address corruption will lead us here */
	printf("Backward edge corruption succeeded!\n");

	/* Do malicious computation */
	while (1) {
	}
}

int main(void)
{
	foo();

	return 0;
}
