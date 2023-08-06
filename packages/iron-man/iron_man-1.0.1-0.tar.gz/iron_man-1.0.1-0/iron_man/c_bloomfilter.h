    
#include <stdint.h>
#include <math.h>
#include <stdlib.h>
#define SHIFT 3
#define MASK 0x7


typedef struct {
	uint32_t        capacity;
    uint32_t        hashes;
	uint64_t        bits;
	float           error;
	uint64_t       *seeds;
} cbloomfilterctxt;

void init_bloomfilter(cbloomfilterctxt * ctxt, uint32_t capacity, float error,int prime_length);
void free_bloomfilter(cbloomfilterctxt * ctxt);
void clean_bitmap(char *bitmap, uint32_t len);
int is_prime_number(uint64_t num);
uint64_t next_prime_number(uint64_t num);

uint64_t MurmurHash64A (const void * key, uint32_t len, uint64_t seed );
uint64_t hash(const char* data, uint32_t len, uint64_t seed, uint64_t bits);
void add_to_bitarray(char *bitarr, uint64_t num);
int is_in_bitarray(char *bitarr, int num);
void add(char *bitmap, const char *data, uint32_t len, uint64_t *seeds, uint32_t hashes, uint64_t bits);
int is_contain(char *bitmap, const char *data, uint32_t len, uint64_t *seeds, uint32_t hashes, uint64_t bits);

void bf_add(cbloomfilterctxt* ctxt, char *bitmap, const char *data, uint32_t len);
int bf_is_contain(cbloomfilterctxt* ctxt,char *bitmap, const char *data, uint32_t len);