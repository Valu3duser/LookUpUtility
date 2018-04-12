import numpy as np
import matplotlib.pylab as plt
from scipy import signal

num_samples = 255
bit_depth = {   '8 bit' : 255,
                '10 bit': 1023,
                '12 bit': 4095,
                '16 bit': 65535}



class LookUpTable:
    bit_depth = {   '8 bit' : 255,
                    '10 bit': 1023,
                    '12 bit': 4095,
                    '16 bit': 65535}

    def __init__(self, num_samples, bit_depth, unsigned = True):
        self._num_samples = num_samples
        self._unsigned = unsigned
        self._bit_depth = bit_depth
        self._y = None

    def generate_csv(self, filename):
        fo = open(filename, 'w')
        for i in self._y:
            fo.write(str(int(i))+',\n')
        fo.close()
    
    def generate_avr_header(self, filename):
        if self._unsigned:
            var_type = 'uint8_t'
        else:
            var_type = 'int8_t'
        fo = open(filename, 'w')
        fo.write('#include <avr/pgmspace.h>\n')
        fo.write('\nconst '+var_type+' sin_table['+str(self._num_samples)+
                 '] PROGMEM = \n{\n')
        for i in self._y:
            fo.write('\t'+str(int(i))+',\n')
        fo.write('}')
        fo.close()

class SineTable(LookUpTable):
    def __init__(self, num_samples, bit_depth, unsigned = True):
        super().__init__(num_samples, bit_depth, unsigned = True)
        
        self._x = np.linspace(0, 2*np.pi, num_samples)
       
        if unsigned ==True:
            self._y = np.round((bit_depth/2)+((bit_depth/2) * np.sin(self._x)))
        else:
            self._y = np.round(((bit_depth/2) * np.sin(self._x)))
        for i in self._y:
            print(int(i))
    
    def plot_sine(self):
        plt.plot(self._x, self._y)
        plt.xlabel('Angle [rad]')
        plt.ylabel('sin(x)')
        plt.axis('tight')
        plt.show()
class TriangleTable(LookUpTable):
    def __init__(self, num_samples, bit_depth, unsigned = True):
        super().__init__(num_samples, bit_depth, unsigned = True)      
        self._x = np.linspace(0, 1, num_samples)
        if unsigned ==True:
            self._y = np.round((bit_depth/2)+ (bit_depth/2)*signal.sawtooth(2 * np.pi * self._x))
        else:
            self._y = np.round((bit_depth/2)*signal.sawtooth(2 * np.pi * self._x))

    def plot_triangle(self):
        plt.plot(self._x, self._y)
        #plt.xlabel('Angle [rad]')
        #plt.ylabel('sin(x)')
        #plt.axis('tight')
        plt.show()
        signal.

#################### main() #################################################    
if __name__ == "__main__":
    lut = TriangleTable(num_samples,255, False)
    lut.plot_triangle()
    lut.generate_avr_header('tri.h')
    lut.generate_csv('tri.csv')
