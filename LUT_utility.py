import numpy as np
import matplotlib.pylab as plt
from scipy import signal

num_samples = 256
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
class SawTable(LookUpTable):
    def __init__(self, num_samples, bit_depth, unsigned = True, type = 'triangle'):
        super().__init__(num_samples, bit_depth, unsigned = True)      
        self._x = np.linspace(0, 1, num_samples)
        
        if type == 'triangle':
            self._width = 0.5
        elif type == 'up':
            self._width = 1
        else:
            self._width = 0

        if unsigned ==True:
            self._y = np.round((bit_depth/2)+ (bit_depth/2)*signal.sawtooth(2 * np.pi * self._x,self._width))
        else:
            self._y = np.round((bit_depth/2)*signal.sawtooth(2 * np.pi * self._x,self._width))
    def plot_saw(self):
        plt.plot(self._x, self._y)
        #plt.xlabel('Angle [rad]')
        #plt.ylabel('sin(x)')
        #plt.axis('tight')
        plt.show()

class ExpTable(LookUpTable):
    def __init__(self, num_samples, bit_depth, unsigned = True):
        super().__init__(num_samples, bit_depth, unsigned = True)

        self._x = np.linspace(-1, 2, num_samples)
        self._y =[]
        self.exp = np.exp(self._x)
        for i in self.exp:
            self._y.append(np.round((bit_depth)* i/self.exp[num_samples-1]))
        #for i in self._y:
        #    print (i)
    def plot_exp(self):
        plt.plot(self._x, self._y)
        plt.show()

#################### main() #################################################    
if __name__ == "__main__":
    lut = ExpTable(num_samples,1024)
    lut.plot_exp()
    #lut.generate_avr_header('tri.h')
    #lut.generate_csv('tri.csv')


    #env_linear = np.arange(0, 257.0) / 256.0

    #env_expo = np.exp(4*env_linear)

    #env_expo_norm = []

    #for i in env_expo:
    #    env_expo_norm.append(i/env_expo[255])

    #plt.plot(env_linear, env_expo_norm)
    #plt.show()
