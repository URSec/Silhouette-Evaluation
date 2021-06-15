/**** START DATASET ****/
#include "th_lib.h"
#include "../loops.h"
static intparts ref_data_3[]={
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,-1,0x001fae14,0x7ae3425e}/*9.900000000144009160e-01*/,
	{0,10,0x00100400,0x00000000}/*1.025000000000000000e+03*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{1,-2,0x0016c779,0xa6c088b1}/*-3.559250000418031079e-01*/,
	{1,1,0x001b682c,0xc86f8eac}/*-3.425866666702708230e+00*/,
	{0,4,0x00140e40,0xb86cbe68}/*2.005567505507352166e+01*/,
	{0,-1,0x001fae14,0x7ae21cf2}/*9.900000000060613647e-01*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,7,0x0018f999,0x92dcd280}/*1.997999967873511196e+02*/,
	{0,0,0x00195601,0xc2e384db}/*1.583497773441471024e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,0,0x00100000,0x0002b86e}/*1.000000000039587444e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,2,0x0014b717,0x58e23612}/*5.178800000006519966e+00*/,
	{1,0,0x0017477a,0x74d9e4bc}/*-1.454950767946043833e+00*/,
	{0,0,0x00000000,0x00000000}/*0.000000000000000000e+00*/,
	{0,10,0x00190000,0x00000000}/*1.600000000000000000e+03*/,
	{0,11,0x001642b8,0xf2c4e3b8}/*2.849361227181241702e+03*/
}; /* ref_data */

void init_preset_3() {
presets_loops[3].seed=0x4645ca3;
presets_loops[3].N=0x20;
presets_loops[3].tests=0x0fe8e78d;
presets_loops[3].Loop=0x64;
presets_loops[3].minbits=30;
presets_loops[3].rtype=0;
presets_loops[3].limit_int_input=0;
presets_loops[3].reinit_step=0x1;
presets_loops[3].ref_data=ref_data_3;
}
/**** END DATASET ****/

