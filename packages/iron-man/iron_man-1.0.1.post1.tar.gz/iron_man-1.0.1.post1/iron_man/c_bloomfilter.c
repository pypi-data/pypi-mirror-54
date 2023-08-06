#include "c_bloomfilter.h"

void init_bloomfilter(cbloomfilterctxt * ctxt, uint32_t capacity, float error, int prime_length) {
    // Counter
    uint32_t i;

    ctxt->capacity = capacity;
    ctxt->bits     = (uint64_t)(-(log(error) * capacity) / (log(2) * log(2)));
    if (prime_length)
        ctxt->bits = next_prime_number(ctxt->bits);

    ctxt->hashes   = (uint32_t)(ceil(log(2) * ctxt->bits / capacity));
    ctxt->error    = error;
    ctxt->seeds    = (uint64_t *)(malloc(ctxt->hashes * sizeof(uint64_t)));

    uint32_t a = 1664525;
    uint32_t c = 1013904223;
    uint32_t x = 314159265;
    for (i = 0; i < ctxt->hashes; ++i) {
        ctxt->seeds[i] = x;
        x = a * x + c;
    }
}

void free_bloomfilter(cbloomfilterctxt * ctxt) {
    if (ctxt->seeds) {
        free(ctxt->seeds);
    }
}

uint64_t MurmurHash64A (const void * key, uint32_t len, uint64_t seed )
{
    const uint64_t m = 0xc6a4a7935bd1e995;
    const int r = 47;
    uint64_t h = seed ^ (len * m);
    const uint64_t * data = (const uint64_t *)key;
    const uint64_t * end = data + (len/8);
    while(data != end)
    {
        uint64_t k = *data++;

        k *= m;
        k ^= k >> r;
        k *= m;

        h ^= k;
        h *= m;
    }
    const unsigned char * data2 = (const unsigned char*)data;
    switch(len & 7)
    {
    case 7: h ^= (uint64_t)(data2[6]) << 48;
    case 6: h ^= (uint64_t)(data2[5]) << 40;
    case 5: h ^= (uint64_t)(data2[4]) << 32;
    case 4: h ^= (uint64_t)(data2[3]) << 24;
    case 3: h ^= (uint64_t)(data2[2]) << 16;
    case 2: h ^= (uint64_t)(data2[1]) << 8;
    case 1: h ^= (uint64_t)(data2[0]);
            h *= m;
    };
    h ^= h >> r;
    h *= m;
    h ^= h >> r;
    return h;
}

uint64_t hash(const char* data, uint32_t len, uint64_t seed, uint64_t bits) {
    return MurmurHash64A(data, len, seed) % bits;
}

void add_to_bitarray(char *bitarr, uint64_t num){
    bitarr[num >> SHIFT] |= (1 << (7-num & MASK));  /* MASK is 0x7 */
}

int is_in_bitarray(char *bitarr, int num){
    return bitarr[num >> SHIFT] & (1 << (7-(num & MASK)));
}

void add(char *bitmap, const char *data, uint32_t len, uint64_t *seeds, uint32_t hashes, uint64_t bits){
    uint32_t i;
    uint64_t position;
    for(i=0; i<hashes; i++){
        position = hash(data,len,seeds[i],bits);
        bitmap[position >> SHIFT] |= (1 << (7-(position & MASK)));
    }
}

int is_contain(char *bitmap, const char *data, uint32_t len, uint64_t *seeds, uint32_t hashes, uint64_t bits){
    uint32_t i;
    uint64_t position = hash(data,len,seeds[0],bits);
    int result = bitmap[position >> SHIFT] & (1 << (7-(position & MASK)));
    for(i=1; i<hashes; i++){
        position = hash(data,len,seeds[i],bits);
        result = result&&(bitmap[position >> SHIFT] & (1 << (7-(position & MASK))));
        if(result == 0)
            break;
    }
    return result;
}


void bf_add(cbloomfilterctxt* ctxt, char *bitmap, const char *data, uint32_t len){
    add(bitmap,data, len, ctxt->seeds, ctxt->hashes, ctxt->bits);
}
int bf_is_contain(cbloomfilterctxt* ctxt,char *bitmap, const char *data, uint32_t len){
    return is_contain(bitmap,data,len,ctxt->seeds, ctxt->hashes, ctxt->bits);
}


void clean_bitmap(char *bitmap, uint32_t len){
    uint32_t i;
    for(i = 0; i < len; i++)
        bitmap[i] &= 0;
}

int is_prime_number(uint64_t num){
    if (num == 2) return 1;
    if (num%2 == 0) return 0;
    uint32_t i;
    uint32_t len = (uint32_t)(sqrt((double)num)) + 1;
    for (i = 3; i < len ; i+=2)
        if (num%i == 0)
            return 0;
    return 1;
}

uint64_t next_prime_number(uint64_t num){
    uint64_t i;
    for (i = num; i < 2*num; i++)
        if (is_prime_number(i))
            return i;
    return num;

}