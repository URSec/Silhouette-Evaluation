/**** START DATASET ****/
#include "th_lib.h"
#include "../loops.h"
static intparts ref_data_2[]={
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,-1,0x00000000,0x00fde198}/*9.917235374450683594e-01*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00829d94}/*1.020433902740478516e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,-3,0x00000000,0x00d6750e}/*2.094309031963348389e-01*/,
	{1,-1,0x00000000,0x00911d62}/*-5.668545961380004883e-01*/,
	{0,3,0x00000000,0x00a1909f}/*1.009780788421630859e+01*/,
	{0,0,0x00000000,0x0082ed6a}/*1.022870302200317383e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,13,0x00000000,0x00a8036f}/*1.075285839843750000e+04*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{1,4,0x00000000,0x00b292fb}/*-2.232176780700683594e+01*/,
	{0,6,0x00000000,0x00c80000}/*1.000000000000000000e+02*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,-1,0x00000000,0x00ff1c1e}/*9.965227842330932617e-01*/,
	{0,6,0x00000000,0x00c945be}/*1.006362152099609375e+02*/,
	{0,-8,0x00000000,0x00a771c9}/*5.109999794512987137e-03*/,
	{1,0,0x00000000,0x00c421c7}/*-1.532280802726745605e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,13,0x00000000,0x00aafdab}/*1.094341699218750000e+04*/
}; /* ref_data */

void init_preset_2() {
presets_loops[2].seed=0x4645ca3;
presets_loops[2].N=0x186a0;
presets_loops[2].tests=0xfef9e797;
presets_loops[2].Loop=0x64;
presets_loops[2].minbits=14;
presets_loops[2].rtype=0;
presets_loops[2].limit_int_input=0;
presets_loops[2].reinit_step=0x1;
presets_loops[2].ref_data=ref_data_2;
}
/**** END DATASET ****/

