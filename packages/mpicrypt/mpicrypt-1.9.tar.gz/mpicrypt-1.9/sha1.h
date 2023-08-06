#ifndef __SHA_H
#define __SHA_H
#ifndef SHA_IMPORT
# define SHA_IMPORT IMPORT
#endif

#include <stdint.h>

typedef void* SHA_CTX;
#define SHA_CTX_SIZE 160 /*max size*/

#if defined(__cplusplus)
extern "C" {
#endif
  uint8_t* sha1(const uint8_t *src, uint32_t srcLen, uint8_t *sink);

  /*op = '1': init sha1, '2': init sha256, 'U':update, 'F':final*/
  void sha_op(char op, SHA_CTX ctx, unsigned char *data, uint32_t len); 
#if defined(__cplusplus)
}
#endif
#endif
