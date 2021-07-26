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

/* A function pointer originally pointing to bar() */
void (* volatile func_ptr)(void) = &bar;

void __attribute__((noinline))
foo(void)
{
	/*
	 * Corrupt the function pointer to have it point to the middle of
	 * baz().
	 */
	func_ptr = (void (*)(void))((uintptr_t)&baz + 2);

	/* Prevent bar() from being optimized away */
	if (!isatty(0)) {
		bar();
	}

	/* Call through the corrupted function pointer */
	(*func_ptr)();
}

void __attribute__((used, noinline))
bar(void)
{
	printf("Dummy message\n");
}

const char * __attribute__((used)) str = "Forward edge corruption succeeded!\n";

void __attribute__((naked, noinline))
baz(void)
{
	asm volatile ("bx	lr;"
		      "ldr	r0, =str;" /* <- Function pointer value now */
		      "ldr	r0, [r0];"
		      "bl	printf;" /* Print a success message */
		      "bx	lr;");
}

int main(void)
{
	foo();

	return 0;
}

void
MemManage_Handler(void)
{
	/* A CFI violation will lead us here */
	printf("Forward edge corruption failed!\n");

	while (1) {
	}
}
