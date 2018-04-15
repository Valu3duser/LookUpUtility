import numpy as np
import matplotlib.pylab as plt
from scipy import signal
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


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

    filename = None
    ver_num = '0.0.1'

    root = tk.Tk()
    root.title('Look Up Table Utility '+ver_num)
    root.geometry('270x160')
    bit_depth_tupple = ('8 bit','10 bit','12 bit','16 bit')
    num_samples = ('32','64','128','256','512','1024')
    wave_shapes = ('Sine','Expo 1', 'Expo 2', 'Triangle', 'Up Saw', 'Down Saw')
    num_samples_choice = tk.StringVar()
    bit_dept_choice = tk.StringVar()
    wave_choice = tk.StringVar()
    num_samples_choice.set('256')
    bit_dept_choice.set('8 bit')
    wave_choice.set('Sine')

    def open_dialog():
        global filename
        if v.get() == 1:
            filename = filedialog.asksaveasfilename(filetypes =(("csv files","*.csv"),),defaultextension = ".csv")
        else:
            filename = filedialog.asksaveasfilename(filetypes =(("C Header files","*.h"),),defaultextension = ".h")
        output_dir_label.config(text = filename)  

    def start():
        messagebox.askyesno(message = num_samples_choice.get())
        #print('Hi')

    

    f2 = tk.Frame(root)
    bd_label = tk.Label(f2, text = 'Bit Depth' )
    bd_label.grid(column = 0, row = 0, sticky='E')
    
    
    opt1 = tk.OptionMenu(f2, bit_dept_choice, *bit_depth_tupple)
    opt1.grid(column = 1, row =0, sticky ='EW')
    opt1.config(width = 18)

    
    sample_label = tk.Label(f2, text = 'Number of Samples' )
    sample_label.grid(column = 0, row = 1, sticky='E')
    opt2 = tk.OptionMenu(f2, num_samples_choice, *num_samples)
    opt2.config(width = 18)
    opt2.grid(column =1, row =1, sticky ='EW')

    wave_label = tk.Label(f2, text = 'Wave Shape')
    wave_label.grid(column = 0, row = 2, sticky='E')
    opt3 = tk.OptionMenu(f2, wave_choice, *wave_shapes)
    opt3.config(width = 18)
    opt3.grid(column =1, row =2, sticky ='EW')

    #f3 = tk.Frame(root)
    #output_label = tk.Label(f3, text = 'Ouput file')
    #output_label.grid(column = 0, row = 2, sticky='W')
    #f3.grid(column= 0, row = 1)

    #output_dir_label = tk.Label(f3)
    #output_dir_label.grid(column = 1, row = 2, sticky='W')
    f2.grid(column =0 , row = 0, sticky = 'W', pady =3)
    f1 = tk.Frame(root)
    output_button = tk.Button(f1, text='Choose output location', command = open_dialog)
    output_button.grid(column =0, row =3)

    v = tk.IntVar()
    v.set(2)

    radio_1 = tk.Radiobutton(f1,text ='csv', variable = v, value = 1)
    radio_1.grid(column = 1, row = 3)

    radio_2 = tk.Radiobutton(f1,text ='avr header', variable = v, value = 2)
    radio_2.grid(column = 2, row = 3)
    f1.grid(column = 0, row = 2, sticky = 'W')

    start_button = tk.Button(f1, text = 'Create LUT', command = start)
    start_button.grid(column =0, row = 4, columnspan = 3, sticky ='EW',pady =3)


    root.mainloop()