
/*returns length of output block*/
/* must provide input+16 bytes for output (to handle padding)*/
/* mode = 1(encrypt) , 0(decrypt), 2(counter auto-increment) */
/* for mode2 pass 16byte little endian counter in 'in' */

/* IV (if required by mode) should be passed in in the OUT buffer*/

#define AES_MODE_ENCRYPT 1
#define AES_MODE_CTR     2
#define AES_MODE_CBC     4

int AES_crypt(unsigned char *key,int keylen, int mode,char *in,long inl, char *out,int outl);

