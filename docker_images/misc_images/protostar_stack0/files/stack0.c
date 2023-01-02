#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <ctype.h>


int main(int argc, char** argv)
{
    volatile int modified;
    char buffer[64];
    
    modified = 0;
    gets(buffer);

    if(modified == 0){
        printf("The 'modified' variable has not been changed...\n");
    }
    else{
        printf("The 'modified' variable has been successfully changed !\n");
    }

    return EXIT_SUCCESS;
}
