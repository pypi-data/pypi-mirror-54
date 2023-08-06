
#ifndef  _JS_ALLOC_H_
#define _JS_ALLOC_H_
#  ifdef __cplusplus
     extern "C" {
#  endif

#ifndef JSALLOC_IMPORT
#  ifdef IMPORT
#    define JSALLOC_IMPORT IMPORT
#  else
#    ifdef _WIN32
#      define JSALLOC_IMPORT __declspec( dllimport ) 
#    else
#      define JSALLOC_IMPORT
#    endif
#  endif
#endif

#define JSALLOC_FREE     0
#define JSALLOC_ALLOC    1
#define JSALLOC_ALLOCZ   2
#define JSALLOC_NEW      3
#define JSALLOC_NEWARRAY 4

#define JSALLOC_STRCOPY  10 

#ifdef JS_ALLOC_DEBUG
#  define JS_ALLOC(t,n)      ((t*)(js_allocd(__FILE__, __LINE__,JSALLOC_ALLOC,  0, sizeof(t)*(n), 0)))
#  define JS_ALLOCZ(t,n)     ((t*)(js_allocd(__FILE__, __LINE__,JSALLOC_ALLOCZ, 0, sizeof(t)*(n), 0)))
#  define JS_REALLOC(p,t,n)  ((t*)(js_allocd(__FILE__, __LINE__,JSALLOC_ALLOC,  p, sizeof(t)*(n), 0)))
#  define JS_REALLOCZ(p,t,n) ((t*)(js_allocd(__FILE__, __LINE__,JSALLOC_ALLOCZ, p, sizeof(t)*(n), 0)))
#  define JS_FREE(p)           js_allocd(__FILE__, __LINE__,JSALLOC_FREE,   p, 0, 0)
#  define JS_SIZE(p)     (unsigned int)(js_allocd(__FILE__, __LINE__,JSALLOC_SIZE,   p, 0, 0))
#  define JS_STRCOPY(p)     (char*)(js_allocd(__FILE__, __LINE__,JSALLOC_STRCOPY, (void*)p, 0, 0))
#  define JS_INFO_HERE() do { int __jsinfo = js_thread_info(__FILE__, __LINE__)
#  define JS_INFO_DONE() if(__jsinfo) js_thread_info(0,0); } while(0)
#else
#  define JS_ALLOC(t,n)      ((t*)(js_alloc(JSALLOC_ALLOC,  0, sizeof(t)*(n), 0)))
#  define JS_REALLOC(p,t,n)  ((t*)(js_alloc(JSALLOC_ALLOC,  p, sizeof(t)*(n), 0)))
#  define JS_ALLOCZ(t,n)     ((t*)(js_alloc(JSALLOC_ALLOCZ, 0, sizeof(t)*(n), 0)))
#  define JS_REALLOCZ(p,t,n) ((t*)(js_alloc(JSALLOC_ALLOCZ, p, sizeof(t)*(n), 0)))
#  define JS_FREE(p)           js_alloc(JSALLOC_FREE,   p, 0, 0)
#  define JS_SIZE(p)     (unsigned int)(js_alloc(JSALLOC_SIZE,   p, 0, 0))
#  define JS_STRCOPY(p)     (char*)(js_alloc(JSALLOC_STRCOPY, (void*)p, 0, 0))
#  define JS_INFO_HERE() do { 
#  define JS_INFO_DONE() } while(0)

#endif

#include <stddef.h>

#ifndef STARLIB_CLIENT
JSALLOC_IMPORT
void* js_allocd(const char* fn, int ln, int op, void* p, size_t sz, int align);

JSALLOC_IMPORT
void* js_alloc (int op, void* p, size_t sz, int align);

JSALLOC_IMPORT
int  js_thread_info(const char* fn, int ln);
#endif

#  ifdef __cplusplus
     } /*extern "C"*/
#  endif
#endif
