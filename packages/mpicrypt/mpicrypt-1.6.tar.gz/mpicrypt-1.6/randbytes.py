import _mpicrypt
from _struct import pack
from math import floor
import time
sha256 = _mpicrypt.sha256

##
## This is based on an implementation in PyCrypto 2.0.1
## This one is only suitable for a single thread
##
def which_pools(r):
    """Return a list of pools indexes (in range(32)) that are to be included during reseed number r.

    According to _Practical Cryptography_, chapter 10.5.2 "Pools":

        "Pool P_i is included if 2**i is a divisor of r.  Thus P_0 is used
        every reseed, P_1 every other reseed, P_2 every fourth reseed, etc."
    """
    # This is a separate function so that it can be unit-tested.
    assert r >= 1
    retval = []
    mask = 0
    for i in range(32):
        # "Pool P_i is included if 2**i is a divisor of [reseed_count]"
        if (r & mask) == 0:
            retval.append(i)
        else:
            break   # optimization.  once this fails, it always fails
        mask = (mask << 1) | 1L
    return retval

class FortunaPool(object):
    def __init__(self): self.reset()
    def reset(self):
        self._h = sha256()
        self.length = 0
    def append(self, data):
        self._h.update(data)
        self.length += len(data)
    def digest(self): return sha256(self._h.digest()).digest()

class _EntropySource(object):
    def __init__(self, accumulator, src_num):
        self._fortuna = accumulator
        self._src_num = src_num
        self._pool_num = 0

    def feed(self, data):
        self._fortuna.add_random_event(self._src_num, self._pool_num, data)
        self._pool_num = (self._pool_num + 1) & 31

class RandomBytes:
    min_pool_size = 64      # TODO: explain why
    reseed_interval = 0.100   # 100 ms    TODO: explain why

    key_size = 32          # key size in octets (256 bits)

    # block_size = 16

    # Because of the birthday paradox, we expect to find approximately one
    # collision for every 2**64 blocks of output from a real random source.
    # However, this code generates pseudorandom data by running AES in
    # counter mode, so there will be no collisions until the counter
    # (theoretically) wraps around at 2**128 blocks.  Thus, in order to prevent
    # Fortuna's pseudorandom output from deviating perceptibly from a true
    # random source, Ferguson and Schneier specify a limit of 2**16 blocks
    # without rekeying.

    # use internal routine if provided
    if hasattr(_mpicrypt, 'urandom'):
            def init(self): pass
            def _reados(self,n): return _mpicrypt.urandom(n)
            def _flushos(self): pass
    else:
        import os
        if os.name == 'posix':
            def init(self):
                import stat
                f = open("/dev/urandom", "rb", 0)
                fmode = os.fstat(f.fileno())[stat.ST_MODE]
                if not stat.S_ISCHR(fmode):
                    f.close()
                    raise TypeError("%r is not a character special device" % (self.name,))
                self.__file = f
            def _reados(self, N):
                return self.__file.read(N)
            def _flushos(self): pass
        elif os.name == 'nt':
            def init(self):
                import winrandom
                self.__winrand = winrandom.new()
            # Unfortunately, research shows that CryptGenRandom doesn't provide
            # forward secrecy and fails the next-bit test unless we apply a
            # workaround, which we do here.  See http://eprint.iacr.org/2007/419
            # for information on the vulnerability.
            def _flushos(self):  self.__winrand.get_bytes(128*1024)
            def _reados(self, N):
                self._flushos()
                self.__winrand.get_bytes(128*1024) 
                data = self.__winrand.get_bytes(N)
                self._flushos()
                return data
        elif hasattr(os, 'urandom'):
            def init(self): pass
            def _reados(self,n): return os.urandom(n)
            def _flushos(self): pass

    def __init__(self):
        self.init() # OS specific init
        self._osrng_es = _EntropySource(self, 255)
        self._time_es = _EntropySource(self, 254)
        self._clock_es = _EntropySource(self, 253)

        self.reseed_count = 0
        self.last_reseed = None
        self.pools = [FortunaPool() for i in range(32)]     # 32 pools
        assert(self.pools[0] is not self.pools[1])

        # generator stuff:
        self.aescounter = _mpicrypt.aes_counter()
        self.key = None

        # Add 256 bits to each of the 32 pools, twice.  (For a total of 16384
        # bits collected from the operating system.)
        for i in range(2):
            block = self._reados(32*32)
            for p in range(32):
                self._osrng_es.feed(block[p*32:(p+1)*32])
            block = None
        self._flushos()

    def get_random_bytes(self,N):
        self._osrng_es.feed(self._reados(8)) # Collect 64 bits of entropy from the operating system and feed it to Fortuna.
        t = time.time() # Add the fractional part of time.time()
        self._time_es.feed(pack("@I", int(2**30 * (t - floor(t))))) 
        t = time.clock()         # Add the fractional part of time.clock()
        self._clock_es.feed(pack("@I", int(2**30 * (t - floor(t)))))
        return self._random_data(N)

    def _random_data(self, bytes):
        current_time = time.time()
        if self.last_reseed > current_time:
            warnings.warn("Clock rewind detected. Resetting last_reseed.", ClockRewindWarning)
            self.last_reseed = None
        if (self.pools[0].length >= self.min_pool_size and
            (self.last_reseed is None or
             current_time > self.last_reseed + self.reseed_interval)):
            self._reseed(current_time)
        # The following should fail if we haven't seeded the pool yet.
        num_full_blocks = bytes >> 20
        remainder = bytes & ((1<<20)-1)
        retval = []
        for i in xrange(num_full_blocks):
            retval.append(self._pseudo_random_data(1<<20))
        retval.append(self._pseudo_random_data(remainder))
        return "".join(retval)

    def _set_key(self, key):
        self.key = key
        self.aescounter.set_key(key)

    def _pseudo_random_data(self, bytes):
        if not (0 <= bytes <= 1048576):
            raise AssertionError("You cannot ask for more than 1 MiB of data per request")
        # Compute the output
        retval = self._generate(bytes)
        # Switch to a new key to avoid later compromises of this output (i.e.
        # state compromise extension attacks)
        self._set_key(self._generate(self.key_size))

        assert len(retval) == bytes
        assert len(self.key) == self.key_size

        return retval

    def _generate(self, bytes):
        if self.key is None: raise AssertionError("generator must be seeded before use")
        retval = []
        while bytes > 0:
            if bytes > 65536: # do in 4KBLOCK segments
                x = self.aescounter.encrypt(65536)
            else:
                x = self.aescounter.encrypt(bytes) # should round up to block size
            retval.append(x)
            bytes -= len(x)
        return "".join(retval)

    def _reseed(self, current_time=None):
        if current_time is None: current_time = time.time()
        seed = []
        self.reseed_count += 1
        self.last_reseed = current_time
        for i in which_pools(self.reseed_count):
            seed.append(self.pools[i].digest())
            self.pools[i].reset()
        seed = "".join(seed)

        if self.key is None: self.key = "\0" * self.key_size
        self._set_key(sha256(sha256(self.key + seed).digest()).digest())
        self.aescounter.incr()
        assert len(self.key) == self.key_size

    def add_random_event(self, source_number, pool_number, data):
        assert 1 <= len(data) <= 32
        assert 0 <= source_number <= 255
        assert 0 <= pool_number <= 31
        self.pools[pool_number].append(chr(source_number))
        self.pools[pool_number].append(chr(len(data)))
        self.pools[pool_number].append(data)

_pool = None
def get_random_bytes(N):
    global _pool
    if _pool is None: _pool = RandomBytes()
    return _pool.get_random_bytes(N)

if __name__ == "__main__":
    print ("RANDOM",repr(get_random_bytes(2)))

