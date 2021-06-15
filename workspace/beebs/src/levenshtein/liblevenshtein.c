
/* BEEBS levenshtein benchmark

   c: levenhstein.c
   Copyright (C) 2011 Miguel Serrano

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


   Copyright (C) 2014 Embecosm Limited and University of Bristol

   Contributor James Pallister <james.pallister@bristol.ac.uk>

   This file is part of the Bristol/Embecosm Embedded Benchmark Suite.
   Originally from https://github.com/miguelvps/c/

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>. */

#include "support.h"

/* This scale factor will be changed to equalise the runtime of the
   benchmarks. */
#define SCALE_FACTOR    (REPEAT_FACTOR >> 0)


#include <string.h>

static int min(int x, int y) {
    return x < y ? x : y;
}

int levenshtein_distance(const char *s, const char *t) {
    int i, j;
    int sl = strlen(s);
    int tl = strlen(t);
#ifdef SS_STACK2HEAP
    int * d = (int *)malloc(sizeof(int) * (sl + 1) * (tl + 1));
    int tmp;
#else
    int d[sl + 1][tl + 1];
#endif

    for (i = 0; i <= sl; i++)
#ifdef SS_STACK2HEAP
        d[i * (tl + 1)] = i;
#else
        d[i][0] = i;
#endif

    for (j = 0; j <= tl; j++)
#ifdef SS_STACK2HEAP
        d[j] = j;
#else
        d[0][j] = j;
#endif

    for (j = 1; j <= tl; j++) {
        for (i = 1; i <= sl; i++) {
            if (s[i - 1] == t[j - 1]) {
#ifdef SS_STACK2HEAP
                d[i * (tl + 1) + j] = d[(i - 1) * (tl + 1) + j - 1];
#else
                d[i][j] = d[i - 1][j - 1];
#endif
            }
            else {
#ifdef SS_STACK2HEAP
                d[i * (tl + 1) + j] = min(d[(i - 1) * (tl + 1) + j] + 1,
                                          min(d[i * (tl + 1) + j - 1] + 1,
                                              d[(i - 1) * (tl + 1) + j - 1] + 1));
#else
                d[i][j] = min(d[i - 1][j] + 1,  /* deletion */
                              min(d[i][j - 1] + 1,  /* insertion */
                                  d[i - 1][j - 1] + 1));    /* substitution */
#endif
            }
        }
    }
#ifdef SS_STACK2HEAP
    tmp = d[sl * (tl + 1) + tl];
    free(d);
    return tmp;
#else
    return d[sl][tl];
#endif
}

const char *strings[] = {"srrjngre", "asfcjnsdkj", "string", "msd",
    "strings"};

void
initialise_benchmark (void)
{
}



int benchmark()
{
  int i, j;
  volatile unsigned sum = 0;

  for(i = 0; i < 5; ++i)
    for(j = 0; j < 5; ++j)
      sum += levenshtein_distance(strings[i], strings[j]);

  return sum;

}

int verify_benchmark(int r)
{
  int exp = 122;
  if (r != exp)
    return 0;
  return 1;
}

