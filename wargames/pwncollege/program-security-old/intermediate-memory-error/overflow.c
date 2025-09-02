#include <stdio.h>
#include <stdint.h>

int main() {
    unsigned int a = 65536; // Largest possible int
    unsigned int b = 65536;

    printf("%d\n", a*b); // The output here is undefined behavior
    return 0;
}