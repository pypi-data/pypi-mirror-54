#
#  randpool.py : Cryptographically strong random number generation
#  Jas: Simplified from Python Cryptography Toolkit to be standalone 

try:
  import _mpicrypt
  sha_new = _mpicrypt.sha1
  sha_siz = 20
except:
  try: # non-deprecated for Py2.6
    import hashlib
    sha_new = hashlib.sha1
  except:
    import sha
    sha_new = sha.new
  sha_siz = sha_new().digest_size

import time, array
try:
    # should work without Crypto as well
    from Crypto.Util.number import long_to_bytes
except:
    def long_to_bytes(l):
        s = []
        while l > 0:
            s.insert(0,chr(l&0xff))
            l = l / 256
        return ''.join(s)
try:
    import Crypto.Util.winrandom as winrandom
except:
    winrandom = None

STIRNUM = 3
class RandomPool:
    """randpool.py : Cryptographically strong random number generation.

    The implementation here is similar to the one in PGP.  To be
    cryptographically strong, it must be difficult to determine the RNG's
    output, whether in the future or the past.  This is done by using
    a cryptographic hash function to "stir" the random data.

    Entropy is gathered in the same fashion as PGP; the highest-resolution
    clock around is read and the data is added to the random number pool.
    A conservative estimate of the entropy is then kept.

    If a cryptographically secure random source is available (/dev/urandom
    on many Unixes, Windows CryptGenRandom on most Windows), then use
    it.

    Instance Attributes:
    bits : int
      Maximum size of pool in bits
    bytes : int
      Maximum size of pool in bytes
    entropy : int
      Number of bits of entropy in this pool.

    Methods:
    add_event([s]) : add some entropy to the pool
    get_bytes(int) : get N bytes of random data
    randomize([N]) : get N bytes of randomness from external source
    """


    def __init__(self, numbytes = 160):

        self.bytes = numbytes
        self.bits = self.bytes*8
        self.entropy = 0

        # Construct an array to hold the random pool,
        # initializing it to 0.
        self._randpool = array.array('B', [0]*self.bytes)

        self._event1 = self._event2 = 0
        self._addPos = 0
        self._getPos = sha_siz
        self._lastcounter=time.time()
        self.__counter = 0

        self._measureTickSize()        # Estimate timer resolution
        self._randomize()

    def _updateEntropyEstimate(self, nbits):
        self.entropy += nbits
        if self.entropy < 0:
            self.entropy = 0
        elif self.entropy > self.bits:
            self.entropy = self.bits

    def _randomize(self, N = 0, devname = '/dev/urandom'):
        """_randomize(N, DEVNAME:device-filepath)
        collects N bits of randomness from some entropy source (e.g.,
        /dev/urandom on Unixes that have it, Windows CryptoAPI
        CryptGenRandom, etc)
        DEVNAME is optional, defaults to /dev/urandom.  You can change it
        to /dev/random if you want to block till you get enough
        entropy.
        """
        data = ''
        if N <= 0:
            nbytes = int((self.bits - self.entropy)/8+0.5)
        else:
            nbytes = int(N/8+0.5)
        if winrandom:
            # Windows CryptGenRandom provides random data.
            data = winrandom.new().get_bytes(nbytes)
        else:
            # Many OSes support a /dev/urandom device
            try:
                f=open(devname)
                data=f.read(nbytes)
                f.close()
            except IOError, (num, msg):
                if num!=2: raise IOError, (num, msg)
                # If the file wasn't found, ignore the error
        if data:
            self._addBytes(data)
            # Entropy estimate: The number of bits of
            # data obtained from the random source.
            self._updateEntropyEstimate(8*len(data))
        self.stir_n()                   # Wash the random pool

    def randomize(self, N=0):
        """randomize(N:int)
        use the class entropy source to get some entropy data.
        This is overridden by KeyboardRandomize().
        """
        return self._randomize(N)

    def stir_n(self, N = STIRNUM):
        """stir_n(N)
        stirs the random pool N times
        """
        for i in xrange(N):
            self.stir()

    def stir (self, s = ''):
        """stir(s:string)
        Mix up the randomness pool.  This will call add_event() twice,
        but out of paranoia the entropy attribute will not be
        increased.  The optional 's' parameter is a string that will
        be hashed with the randomness pool.
        """

        entropy=self.entropy            # Save inital entropy value
        self.add_event()

        # Loop over the randomness pool: hash its contents
        # along with a counter, and add the resulting digest
        # back into the pool.
        for i in range(self.bytes / sha_siz):
            h = sha_new(self._randpool)
            h.update(str(self.__counter) + str(i) + str(self._addPos) + s)
            self._addBytes( h.digest() )
            self.__counter = (self.__counter + 1) & 0xFFFFffffL

        self._addPos, self._getPos = 0, sha_siz
        self.add_event()

        # Restore the old value of the entropy.
        self.entropy=entropy


    def get_bytes (self, N):
        """get_bytes(N:int) : string
        Return N bytes of random data.
        """

        s=''
        i, pool = self._getPos, self._randpool
        h=sha_new()
        dsize = sha_siz
        num = N
        while num > 0:
            h.update( self._randpool[i:i+dsize] )
            s = s + h.digest()
            num = num - dsize
            i = (i + dsize) % self.bytes
            if i<dsize:
                self.stir()
                i=self._getPos

        self._getPos = i
        self._updateEntropyEstimate(- 8*N)
        return s[:N]


    def add_event(self, s=''):
        """add_event(s:string)
        Add an event to the random pool.  The current time is stored
        between calls and used to estimate the entropy.  The optional
        's' parameter is a string that will also be XORed into the pool.
        Returns the estimated number of additional bits of entropy gain.
        """
        event = long(time.time()*1000)
        delta = self._noise()
        s = (s + long_to_bytes(event) +
             4*chr(0xaa) + long_to_bytes(delta) )
        self._addBytes(s)
        if event==self._event1 and event==self._event2:
            # If events are coming too closely together, assume there's
            # no effective entropy being added.
            bits=0
        else:
            # Count the number of bits in delta, and assume that's the entropy.
            bits=0
            while delta:
                delta, bits = delta>>1, bits+1
            if bits>8: bits=8

        self._event1, self._event2 = event, self._event1

        self._updateEntropyEstimate(bits)
        return bits

    # Private functions
    def _noise(self):
        # Adds a bit of noise to the random pool, by adding in the
        # current time and CPU usage of this process.
        # The difference from the previous call to _noise() is taken
        # in an effort to estimate the entropy.
        t=time.time()
        delta = (t - self._lastcounter)/self._ticksize*1e6
        self._lastcounter = t
        self._addBytes(long_to_bytes(long(1000*time.time())))
        self._addBytes(long_to_bytes(long(1000*time.clock())))
        self._addBytes(long_to_bytes(long(1000*time.time())))
        self._addBytes(long_to_bytes(long(delta)))

        # Reduce delta to a maximum of 8 bits so we don't add too much
        # entropy as a result of this call.
        delta=delta % 0xff
        return int(delta)


    def _measureTickSize(self):
        # _measureTickSize() tries to estimate a rough average of the
        # resolution of time that you can see from Python.  It does
        # this by measuring the time 100 times, computing the delay
        # between measurements, and taking the median of the resulting
        # list.  (We also hash all the times and add them to the pool)
        interval = [None] * 100
        h = sha_new(`(id(self),id(interval))`)

        # Compute 100 differences
        t=time.time()
        h.update(`t`)
        i = 0
        j = 0
        while i < 100:
            t2=time.time()
            h.update(`(i,j,t2)`)
            j += 1
            delta=int((t2-t)*1e6)
            if delta:
                interval[i] = delta
                i += 1
                t=t2

        # Take the median of the array of intervals
        interval.sort()
        self._ticksize=interval[len(interval)/2]
        h.update(`(interval,self._ticksize)`)
        # mix in the measurement times and wash the random pool
        self.stir(h.digest())

    def _addBytes(self, s):
        "XOR the contents of the string S into the random pool"
        i, pool = self._addPos, self._randpool
        for j in range(0, len(s)):
            pool[i]=pool[i] ^ ord(s[j])
            i=(i+1) % self.bytes
        self._addPos = i

