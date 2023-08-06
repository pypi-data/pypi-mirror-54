/*
SHA-1 in C
By Steve Reid <steve@edmweb.com>
100% Public Domain

Test Vectors (from FIPS PUB 180-1)
"abc"
  A9993E36 4706816A BA3E2571 7850C26C 9CD0D89D
"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
  84983E44 1C3BD26E BAAE4AA1 F95129E5 E54670F1
A million repetitions of "a"
  34AA973C D4C4DAA4 F61EEB2B DBAD2731 6534016F
*/

#if defined(__i386__) || defined(__alpha__) \
        || (defined(__mips__) && (defined(MIPSEL) || defined (__MIPSEL__))) \
        || defined(_M_IX86) || defined(__amd64__)
#ifndef LITTLE_ENDIAN
#define LITTLE_ENDIAN
#endif
#endif


/* CAREFUL: I notice this option is NOT threadsafe */
/* #define SHA1HANDSOFF * Copies data before messing with it. */

/*#include <stdio.h> */
#include <string.h>

/* This test was looking at __MACH__ in this file, but that's wrong.  It
 * looks like this was correctly fixed in util/sha1.c but not here.  So, I 
 * fixed it here, but we should probably rationalize things so that we all
 * use the same file --higgins 2006-09-08 */
#if defined(__ppc__)
#undef LITTLE_ENDIAN
#endif

#include "platform.h"

#define SHA_IMPORT EXPORT
#include "starimpl.h"
#include "sha1.h"
#include "md5.h"

typedef uint32_t U32;

typedef struct {
    uint32_t state[5];
    uint32_t count[2];
    unsigned char  buffer[64];
    unsigned char scratch[64];
} SHA1_CTX;
typedef struct {
    U32 state[8], curlen;
    U32 length_upper, length_lower;
    unsigned char buf[64];
} hash_state;

typedef struct {
  uint32_t hashsize;
  union {
    SHA1_CTX sha1; //hashsize = 20
    hash_state sha256; //hashsize = 32
    context_md5_t md5; //hashsize = 16
  };
} SHA_CTXn;

#define rol(value, bits) (((value) << (bits)) | ((value) >> (32 - (bits))))

/* blk0() and blk() perform the initial expand. */
/* I got the idea of expanding during the round function from SSLeay */
#ifdef LITTLE_ENDIAN
#define blk0(i) (block->l[i] = (rol(block->l[i],24)&0xFF00FF00) \
    |(rol(block->l[i],8)&0x00FF00FF))
#else
#define blk0(i) block->l[i]
#endif
#define blk(i) (block->l[i&15] = rol(block->l[(i+13)&15]^block->l[(i+8)&15] \
    ^block->l[(i+2)&15]^block->l[i&15],1))

/* (R0+R1), R2, R3, R4 are the different operations used in SHA1 */
#define R0(v,w,x,y,z,i) z+=((w&(x^y))^y)+blk0(i)+0x5A827999+rol(v,5);w=rol(w,30);
#define R1(v,w,x,y,z,i) z+=((w&(x^y))^y)+blk(i)+0x5A827999+rol(v,5);w=rol(w,30);
#define R2(v,w,x,y,z,i) z+=(w^x^y)+blk(i)+0x6ED9EBA1+rol(v,5);w=rol(w,30);
#define R3(v,w,x,y,z,i) z+=(((w|x)&y)|(w&x))+blk(i)+0x8F1BBCDC+rol(v,5);w=rol(w,30);
#define R4(v,w,x,y,z,i) z+=(w^x^y)+blk(i)+0xCA62C1D6+rol(v,5);w=rol(w,30);


/* Hash a single 512-bit block. This is the core of the algorithm. */

void SHA1Transform(uint32_t state[5], unsigned char buffer[64])
{
uint32_t a, b, c, d, e;
typedef union {
    unsigned char c[64];
    uint32_t l[16];
} CHAR64LONG16;
CHAR64LONG16* block;
#ifdef SHA1HANDSOFF
static unsigned char workspace[64];
    block = (CHAR64LONG16*)workspace;
    memcpy(block, buffer, 64);
#else
    block = (CHAR64LONG16*)buffer;
#endif
    /* Copy context->state[] to working vars */
    a = state[0];
    b = state[1];
    c = state[2];
    d = state[3];
    e = state[4];
    /* 4 rounds of 20 operations each. Loop unrolled. */
    R0(a,b,c,d,e, 0); R0(e,a,b,c,d, 1); R0(d,e,a,b,c, 2); R0(c,d,e,a,b, 3);
    R0(b,c,d,e,a, 4); R0(a,b,c,d,e, 5); R0(e,a,b,c,d, 6); R0(d,e,a,b,c, 7);
    R0(c,d,e,a,b, 8); R0(b,c,d,e,a, 9); R0(a,b,c,d,e,10); R0(e,a,b,c,d,11);
    R0(d,e,a,b,c,12); R0(c,d,e,a,b,13); R0(b,c,d,e,a,14); R0(a,b,c,d,e,15);
    R1(e,a,b,c,d,16); R1(d,e,a,b,c,17); R1(c,d,e,a,b,18); R1(b,c,d,e,a,19);
    R2(a,b,c,d,e,20); R2(e,a,b,c,d,21); R2(d,e,a,b,c,22); R2(c,d,e,a,b,23);
    R2(b,c,d,e,a,24); R2(a,b,c,d,e,25); R2(e,a,b,c,d,26); R2(d,e,a,b,c,27);
    R2(c,d,e,a,b,28); R2(b,c,d,e,a,29); R2(a,b,c,d,e,30); R2(e,a,b,c,d,31);
    R2(d,e,a,b,c,32); R2(c,d,e,a,b,33); R2(b,c,d,e,a,34); R2(a,b,c,d,e,35);
    R2(e,a,b,c,d,36); R2(d,e,a,b,c,37); R2(c,d,e,a,b,38); R2(b,c,d,e,a,39);
    R3(a,b,c,d,e,40); R3(e,a,b,c,d,41); R3(d,e,a,b,c,42); R3(c,d,e,a,b,43);
    R3(b,c,d,e,a,44); R3(a,b,c,d,e,45); R3(e,a,b,c,d,46); R3(d,e,a,b,c,47);
    R3(c,d,e,a,b,48); R3(b,c,d,e,a,49); R3(a,b,c,d,e,50); R3(e,a,b,c,d,51);
    R3(d,e,a,b,c,52); R3(c,d,e,a,b,53); R3(b,c,d,e,a,54); R3(a,b,c,d,e,55);
    R3(e,a,b,c,d,56); R3(d,e,a,b,c,57); R3(c,d,e,a,b,58); R3(b,c,d,e,a,59);
    R4(a,b,c,d,e,60); R4(e,a,b,c,d,61); R4(d,e,a,b,c,62); R4(c,d,e,a,b,63);
    R4(b,c,d,e,a,64); R4(a,b,c,d,e,65); R4(e,a,b,c,d,66); R4(d,e,a,b,c,67);
    R4(c,d,e,a,b,68); R4(b,c,d,e,a,69); R4(a,b,c,d,e,70); R4(e,a,b,c,d,71);
    R4(d,e,a,b,c,72); R4(c,d,e,a,b,73); R4(b,c,d,e,a,74); R4(a,b,c,d,e,75);
    R4(e,a,b,c,d,76); R4(d,e,a,b,c,77); R4(c,d,e,a,b,78); R4(b,c,d,e,a,79);
    /* Add the working vars back into context.state[] */
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    state[4] += e;
    /* Wipe variables */
    a = b = c = d = e = 0;
}


/* SHA1Init - Initialize new context */

void SHA1Init(SHA1_CTX* context)
{
    /* SHA1 initialization constants */
    context->state[0] = 0x67452301;
    context->state[1] = 0xEFCDAB89;
    context->state[2] = 0x98BADCFE;
    context->state[3] = 0x10325476;
    context->state[4] = 0xC3D2E1F0;
    context->count[0] = context->count[1] = 0;
}


/* Run your data through this. */

void SHA1Update(SHA1_CTX* context, unsigned char* data, uint32_t len)
{
    uint32_t i, j;

    j = (context->count[0] >> 3) & 63;
    if ((context->count[0] += len << 3) < (len << 3)) context->count[1]++;
    context->count[1] += (len >> 29);
    if ((j + len) > 63) {
        memcpy(&context->buffer[j], data, (i = 64-j));
        SHA1Transform(context->state, context->buffer);
        for ( ; i + 63 < len; i += 64) {
            SHA1Transform(context->state, &data[i]);
        }
        j = 0;
    }
    else i = 0;
    memcpy(&context->buffer[j], &data[i], len - i);
}

/* Run your data through this. */

void SHA1UpdateScratch(SHA1_CTX* context,
		       unsigned char* data, uint32_t len,
		       unsigned char *scratch)
{
    uint32_t i, j;
    j = (context->count[0] >> 3) & 63;
    if ((context->count[0] += len << 3) < (len << 3)) context->count[1]++;
    context->count[1] += (len >> 29);
    if ((j + len) > 63) {
        memcpy(&context->buffer[j], data, (i = 64-j));
        SHA1Transform(context->state, context->buffer);
        for ( ; i + 63 < len; i += 64) {
	    memcpy(scratch, &data[i], 64);
            SHA1Transform(context->state, scratch);
        }
        j = 0;
    }
    else i = 0;
    memcpy(&context->buffer[j], &data[i], len - i);
}

/* Add padding and return the message digest. */

void SHA1Final(unsigned char digest[20], SHA1_CTX* context)
{
uint32_t i, j;
unsigned char finalcount[8];

    for (i = 0; i < 8; i++) {
        finalcount[i] = (unsigned char)((context->count[(i >= 4 ? 0 : 1)]
         >> ((3-(i & 3)) * 8) ) & 255);  /* Endian independent */
    }
    SHA1Update(context, (unsigned char *)"\200", 1);
    while ((context->count[0] & 504) != 448) {
        SHA1Update(context, (unsigned char *)"\0", 1);
    }
    SHA1Update(context, finalcount, 8);  /* Should cause a SHA1Transform() */
    for (i = 0; i < 20; i++) {
        digest[i] = (unsigned char)
         ((context->state[i>>2] >> ((3-(i & 3)) * 8) ) & 255);
    }
    /* Wipe variables */
    i = j = 0;
    memset(context->buffer, 0, 64);
    memset(context->state, 0, 20);
    memset(context->count, 0, 8);
    memset(&finalcount, 0, 8);
#ifdef SHA1HANDSOFF  /* make SHA1Transform overwrite it's own static vars */
    SHA1Transform(context->state, context->buffer);
#endif
}

uint8_t *sha1(const uint8_t *src, uint32_t srcLen, uint8_t *sink) {
  uint8_t scratch[64];
  SHA1_CTX ctx;
  SHA1Init(&ctx);
  SHA1UpdateScratch(&ctx, (uint8_t*)src, srcLen, scratch);
  SHA1Final((uint8_t*)sink, &ctx);
  return sink;
}

static void sha256_done(hash_state * md, unsigned char *hash);
static void sha256_process(hash_state * md, unsigned char *buf, int len);
static void sha256_init(hash_state * md); 

void sha_op(char op, SHA_CTX _ctx, unsigned char *data, uint32_t len) {
  SHA_CTXn *ctx = (SHA_CTXn*) _ctx;
  switch(op) {
  case '5': ctx->hashsize = 16; MD5Init(&ctx->md5); goto u;
  case '2': ctx->hashsize = 32; sha256_init(&ctx->sha256); goto u;
  case '1':
  case 'I': ctx->hashsize = 20; SHA1Init(&ctx->sha1); /*no break*/
  u:
  case 'U': if(len) {
    if(ctx->hashsize == 20)
      SHA1UpdateScratch(&(ctx->sha1),data,len,&(ctx->sha1.scratch[0]));      
    else if(ctx->hashsize == 32) 
      sha256_process(&(ctx->sha256),data,len);
    else if(ctx->hashsize == 16) 
      MD5Update(&(ctx->md5),data,len);
  }; break;
  case 'F': 
    if(len >= ctx->hashsize) {
      if(ctx->hashsize == 20) {
	SHA1_CTX tmp;
	memcpy(&tmp,&(ctx->sha1),sizeof(SHA1_CTX));    /*copy or it will corrupt state*/
	SHA1Final(data, &tmp);
      } else if(ctx->hashsize == 32) 
	sha256_done(&(ctx->sha256),data);
      else if(ctx->hashsize == 16) {
	context_md5_t tmp;
	memcpy(&tmp,&(ctx->md5),sizeof(context_md5_t));    /*copy or it will corrupt state*/
	MD5Final(data, &tmp);
      }
    }
  }
}


/* from Pycrypto toolkit*/

/*
 * An implementation of the SHA-256 hash function, this is endian neutral
 * so should work just about anywhere.
 *
 * This code works much like the MD5 code provided by RSA.  You sha_init()
 * a "sha_state" then sha_process() the bytes you want and sha_done() to get
 * the output.
 *
 * Revised Code:  Complies to SHA-256 standard now.
 *
 * Originally written by Tom St Denis -- http://tomstdenis.home.dhs.org
 *
 * Adapted for PyCrypto by Jeethu Rao, Taylor Boon, and others.
 *
 * ===================================================================
 * The contents of this file are dedicated to the public domain.  To
 * the extent that dedication to the public domain is not available,
 * everyone is granted a worldwide, perpetual, royalty-free,
 * non-exclusive license to exercise all rights associated with the
 * contents of this file for any purpose whatsoever.
 * No rights are reserved.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 * ===================================================================
 *
 */
typedef unsigned char U8;

/* the K array */
static const U32 K[64] = {
    0x428a2f98UL, 0x71374491UL, 0xb5c0fbcfUL, 0xe9b5dba5UL, 0x3956c25bUL,
    0x59f111f1UL, 0x923f82a4UL, 0xab1c5ed5UL, 0xd807aa98UL, 0x12835b01UL,
    0x243185beUL, 0x550c7dc3UL, 0x72be5d74UL, 0x80deb1feUL, 0x9bdc06a7UL,
    0xc19bf174UL, 0xe49b69c1UL, 0xefbe4786UL, 0x0fc19dc6UL, 0x240ca1ccUL,
    0x2de92c6fUL, 0x4a7484aaUL, 0x5cb0a9dcUL, 0x76f988daUL, 0x983e5152UL,
    0xa831c66dUL, 0xb00327c8UL, 0xbf597fc7UL, 0xc6e00bf3UL, 0xd5a79147UL,
    0x06ca6351UL, 0x14292967UL, 0x27b70a85UL, 0x2e1b2138UL, 0x4d2c6dfcUL,
    0x53380d13UL, 0x650a7354UL, 0x766a0abbUL, 0x81c2c92eUL, 0x92722c85UL,
    0xa2bfe8a1UL, 0xa81a664bUL, 0xc24b8b70UL, 0xc76c51a3UL, 0xd192e819UL,
    0xd6990624UL, 0xf40e3585UL, 0x106aa070UL, 0x19a4c116UL, 0x1e376c08UL,
    0x2748774cUL, 0x34b0bcb5UL, 0x391c0cb3UL, 0x4ed8aa4aUL, 0x5b9cca4fUL,
    0x682e6ff3UL, 0x748f82eeUL, 0x78a5636fUL, 0x84c87814UL, 0x8cc70208UL,
    0x90befffaUL, 0xa4506cebUL, 0xbef9a3f7UL, 0xc67178f2UL
};

/* Various logical functions */
#define Ch(x,y,z)    ((x & y) ^ (~x & z))
#define Maj(x,y,z)  ((x & y) ^ (x & z) ^ (y & z))
#define S(x, n)        (((x)>>((n)&31))|((x)<<(32-((n)&31))))
#define R(x, n)        ((x)>>(n))
#define Sigma0(x)    (S(x, 2) ^ S(x, 13) ^ S(x, 22))
#define Sigma1(x)    (S(x, 6) ^ S(x, 11) ^ S(x, 25))
#define Gamma0(x)    (S(x, 7) ^ S(x, 18) ^ R(x, 3))
#define Gamma1(x)    (S(x, 17) ^ S(x, 19) ^ R(x, 10))

/* compress 512-bits */
static void sha_compress(hash_state * md)
{
    U32 S[8], W[64], t0, t1;
    int i;

    /* copy state into S */
    for (i = 0; i < 8; i++)
        S[i] = md->state[i];

    /* copy the state into 512-bits into W[0..15] */
    for (i = 0; i < 16; i++)
        W[i] = (((U32) md->buf[(4 * i) + 0]) << 24) |
            (((U32) md->buf[(4 * i) + 1]) << 16) |
            (((U32) md->buf[(4 * i) + 2]) << 8) |
            (((U32) md->buf[(4 * i) + 3]));

    /* fill W[16..63] */
    for (i = 16; i < 64; i++)
        W[i] = Gamma1(W[i - 2]) + W[i - 7] + Gamma0(W[i - 15]) + W[i - 16];

    /* Compress */
    for (i = 0; i < 64; i++) {
        t0 = S[7] + Sigma1(S[4]) + Ch(S[4], S[5], S[6]) + K[i] + W[i];
        t1 = Sigma0(S[0]) + Maj(S[0], S[1], S[2]);
        S[7] = S[6];
        S[6] = S[5];
        S[5] = S[4];
        S[4] = S[3] + t0;
        S[3] = S[2];
        S[2] = S[1];
        S[1] = S[0];
        S[0] = t0 + t1;
    }

    /* feedback */
    for (i = 0; i < 8; i++)
        md->state[i] += S[i];
}

/* init the SHA state */
void sha256_init(hash_state * md)
{
    md->curlen = md->length_upper = md->length_lower = 0;
    md->state[0] = 0x6A09E667UL;
    md->state[1] = 0xBB67AE85UL;
    md->state[2] = 0x3C6EF372UL;
    md->state[3] = 0xA54FF53AUL;
    md->state[4] = 0x510E527FUL;
    md->state[5] = 0x9B05688CUL;
    md->state[6] = 0x1F83D9ABUL;
    md->state[7] = 0x5BE0CD19UL;
}

void sha256_process(hash_state * md, unsigned char *buf, int len)
{
    while (len--) {
        /* copy byte */
        md->buf[md->curlen++] = *buf++;

        /* is 64 bytes full? */
        if (md->curlen == 64) {
	    U32 orig_length;
            sha_compress(md);
	    orig_length = md->length_lower;
            md->length_lower += 512;
	    if (orig_length > md->length_lower) {
	      md->length_upper++;
	    }
            md->curlen = 0;
        }
    }
}

void sha256_done(hash_state * _md, unsigned char *hash)
{
    int i;
    U32 orig_length;
    hash_state mds;
    hash_state * md = &mds;
    /*copy or it will corrupt state*/
    memcpy(md,_md,sizeof(hash_state));

    /* increase the length of the message */
    orig_length = md->length_lower;
    md->length_lower += md->curlen * 8;
    if (orig_length > md->length_lower) {
        md->length_upper++;
    }

    /* append the '1' bit */
    md->buf[md->curlen++] = 0x80;

    /* if the length is currently above 56 bytes we append zeros
     * then compress.  Then we can fall back to padding zeros and length
     * encoding like normal.
     */
    if (md->curlen > 56) {
        for (; md->curlen < 64;)
            md->buf[md->curlen++] = 0;
        sha_compress(md);
        md->curlen = 0;
    }

    /* pad upto 56 bytes of zeroes */
    for (; md->curlen < 56;)
        md->buf[md->curlen++] = 0;

    /* append length */
    for (i = 56; i < 60; i++)
        md->buf[i] = (md->length_upper >> ((59 - i) * 8)) & 255;
    for (i = 60; i < 64; i++)
        md->buf[i] = (md->length_lower >> ((63 - i) * 8)) & 255;
    sha_compress(md);

    /* copy output */
    for (i = 0; i < 32; i++)
        hash[i] = (md->state[i >> 2] >> (((3 - i) & 3) << 3)) & 255;
}
