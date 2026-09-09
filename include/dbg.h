/*
Zed A. Shaw's Awesome Debug Macros
Annotated by Mark Redd
*/

#ifndef __dbg_h__
#define __dbg_h__

// #define NDEBUG

#define C_RED "\x1b[31m"
#define C_GREEN "\x1b[32m"
#define C_YELLOW "\x1b[33m"
#define C_BLUE "\x1b[34m"
#define C_MAGENTA "\x1b[35m"
#define C_CYAN "\x1b[36m"
#define C_RESET "\x1b[0m"

#include <errno.h>
#include <stdio.h>
#include <string.h>

#ifdef NDEBUG
#define debug(M, ...)
#else
#define debug(M, ...)                                                          \
    fprintf(stderr,                                                            \
            "[" C_GREEN "DEBUG" C_RESET "] %s:%d: in_function: %s) " M "\n",   \
            __FILE__, __LINE__, __FUNCTION__, ##__VA_ARGS__)
#endif

#define clean_errno() (errno == 0 ? "None" : strerror(errno))

#define log_err(M, ...)                                                        \
    fprintf(stderr,                                                            \
            "[" C_RED "ERROR" C_RESET                                          \
            "] (%s:%d: in_function: %s errno: %s) " M "\n",                    \
            __FILE__, __LINE__, __FUNCTION__, clean_errno(), ##__VA_ARGS__)

#define log_warn(M, ...)                                                       \
    fprintf(stderr,                                                            \
            "[" C_YELLOW "WARN" C_RESET                                        \
            "] (%s:%d: in_function: %s errno: %s) " M "\n",                    \
            __FILE__, __LINE__, __FUNCTION__, clean_errno(), ##__VA_ARGS__)

#define log_info(M, ...)                                                       \
    fprintf(stderr,                                                            \
            "[" C_CYAN "INFO" C_RESET "] (%s:%d: in_function: %s ) " M "\n",   \
            __FILE__, __LINE__, __FUNCTION__, ##__VA_ARGS__)

#define check(A, M, ...)                                                       \
    if (!(A)) {                                                                \
        log_err(M, ##__VA_ARGS__);                                             \
        errno = 0;                                                             \
        goto error;                                                            \
    }

#define sentinel(M, ...)                                                       \
    {                                                                          \
        log_err(M, ##__VA_ARGS__);                                             \
        errno = 0;                                                             \
        goto error;                                                            \
    }

#define check_mem(A) check((A), "Out of memory.")

#define check_debug(A, M, ...)                                                 \
    if (!(A)) {                                                                \
        debug(M, ##__VA_ARGS__);                                               \
        errno = 0;                                                             \
        goto error;                                                            \
    }

#endif
