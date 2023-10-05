#include <wiringPi.h> 
#include <stdio.h> 
#include <stdlib.h>
#include <time.h>

#define PA 2 
#define PB 4 
#define PC 1 
#define PD 16 
#define PE 15 
#define PF 8 
#define PG 9 
#define PDEC 0 
#define PDP1 22 
#define PDP2 23 
#define PDP3 24 
#define PDP4 25

// for anode display
char nums[10] = {0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90};

// Wpi pin numbers
char pins[8] = {PA, PB, PC, PD, PE, PF, PG, PDEC}; 
char pindps[4] = {PDP1, PDP2, PDP3, PDP4};

void clear_pin () 
{
	int i;
	for (i=0; i<8; i++)
		digitalWrite(pins[i], 1); 
	for (i=0; i<4; i++)
		digitalWrite(pindps[i], 0);
}

void set_pin (int n) 
{
	int i;
	for (i=0; i<8; i++)
		digitalWrite(pins[i], (nums[n] >> i) & 0x1);
}

void init_pin ()
{
	int i;
	for (i=0;i<8;i++)
		pinMode(pins[i], OUTPUT); 
	for (i=0;i<4;i++)
        	pinMode(pindps[i], OUTPUT);
}

int main(void)
{
	int i, hour, min; 
	wiringPiSetup( ); 
	init_pin ();

	while(1)
	{
		time_t now;
        	struct tm timeinfo;

        	time(&now);
        	localtime_r(&now, &timeinfo);

		hour = timeinfo.tm_hour;
		min = timeinfo.tm_min;

		clear_pin();
		
		digitalWrite(pindps[0], 1); 
		set_pin(hour / 10);
		delay(1);

		clear_pin();
		digitalWrite(pindps[1], 1);
		set_pin(hour % 10);
		delay(1);

		clear_pin();
		digitalWrite(pindps[2], 1);
		set_pin(min / 10);
		delay(1);

		clear_pin();
		digitalWrite(pindps[3], 1);
		set_pin(min % 10);
		delay(1);
	} 

	clear_pin();

	return 0;
}


