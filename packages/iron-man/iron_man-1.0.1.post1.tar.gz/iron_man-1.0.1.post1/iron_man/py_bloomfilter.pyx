cdef extern from "c_bloomfilter.h":
    ctypedef unsigned long int   uint64_t
    ctypedef unsigned int   uint32_t

    ctypedef struct cbloomfilterctxt:
        uint32_t        capacity;
        uint32_t        hashes;
        uint64_t        bits;
        float           error;
        uint64_t       *seeds;

    void clean_bitmap(char *bitmap, uint32_t len)
    void free_bloomfilter(cbloomfilterctxt * ctxt)
    void init_bloomfilter(cbloomfilterctxt * ctxt, uint32_t capacity, float error,bint prime_length)
    void bf_add(cbloomfilterctxt* ctxt,char *bitmap, const char *data, uint32_t len);
    bint bf_is_contain(cbloomfilterctxt* ctxt,char *bitmap, const char *data, uint32_t len);
    uint64_t hash(const char* data, uint32_t len, uint64_t seed, uint64_t bits);

cdef class CBloomfilter(object):
    cdef cbloomfilterctxt context

    property bits:
        def __get__(self):
            return self.context.bits

    property hashes:
        def __get__(self):
            return self.context.hashes
    def __cinit__(self, capacity, error, prime_length = True):
        init_bloomfilter(&self.context,capacity,error,prime_length)

    def __dealloc__(self):
        free_bloomfilter(&self.context)

    def add(self,bitmap,data):
        key = data.encode()
        bf_add(&self.context, bitmap,key,len(key))

    def is_contain(self,bitmap,data):
        key = data.encode()
        return bf_is_contain(&self.context, bitmap,key,len(key))

    def clean_bitmap(self,bitmap):
        clean_bitmap(bitmap, len(bitmap))

    def hash(self,data):
        key = data.encode()
        offset = []
        for i in range(self.hashes):
            seed = self.context.seeds[i]
            offset.append(hash(key,len(key),seed,self.context.bits))
        return offset
