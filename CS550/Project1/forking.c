#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(void)
{
	int k;
	printf ("Main Process' PID = %d\n", getpid());
	fflush(stdout);
	for (k = 1; k <= 3; k++)
	{
		fork ();
		printf ("k = %d, PPID = %d, pID = %d, I'm Alive!\n", k, getppid(), getpid());
		fflush(stdout);
	}
}

