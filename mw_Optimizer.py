import math


class Optimizer():
    """ 
    Microwave Optimization class between line of sight mask. 
    Classical representation of properties and their respective effect in the value chian.

    Attributes:
        LTX (float) representing the the total system losses in dB at the transmitter
        LRX (float) representing the total system losses in dB at the receiver.
        ptx (floats) represents the transmitter power in dBm.
        prx (floats) represents the receiver power in dBm.
        gtx (floats) represents the transmitter antenna gain in dBi.
        grx (floats) represents the reciever antenna gain in dBi.
        rsx (flaot) represents receiver sensitivity of the antenna
        freg (int) represents the operating frequency of the antenna pair
        ki (float) represents the idim constant
        LOS (float) represents the maximum line-of-sight path distance in kilometers

    """

    def __init__(self,
                 LTX=3.71,
                 LRX=2.86,
                 transmitter_power=16.0,
                 receiver_power=16.0,
                 antenna_gain_receiver=40.5,
                 antenna_gain_transmitter=40.5,
                 sensivity_threshold=-73.5,
                 operating_frequency=12400,
                 ):

        self.ltx = LTX
        self.lrx = LRX
        self.grx = antenna_gain_receiver
        self.gtx = antenna_gain_transmitter
        self.ptx = transmitter_power
        self.prx = receiver_power
        self.rsx = sensivity_threshold
        self.freq = operating_frequency
        self.ki = 0.4951
        self.LOS = 0.0


    def show_input(self):
        return { 
                "LTX":self.ltx, 
                "LRX": self.lrx, 
                "GRX": self.grx, 
                "GTX": self.gtx, 
                "PTX": self.ptx, 
                "PRX": self.prx, 
                "RSX": self.rsx, 
                "Frequency": self.freq 
        }
    
       
    def los(self, hTX, hRX):
        """
            This method calculate the path loss of the pair antenna
        """
        self.LOS = 4.124*(math.sqrt(hTX) + math.sqrt(hRX))
        return self.LOS

    def idim_constant(self, step=0.00):
        """
            This method calculate the idim constant required to find optimization
        """
        self.ki += step
        return self.ki

    def aniebiet(self):
        """
            This method calculate the aniebet equation whose output is optimized distance
        """
        optimize_distance = self.ki * math.sqrt(self.LOS)
        return optimize_distance

    def free_space_loss(self):
        """
            This method calculate the free path loss of the pair antenna
        """
        fls = 32.45 + (20 * math.log10(self.aniebiet())) + \
            (20 * math.log10(self.freq))
        return fls              # fls == Lpath

    def received_power(self):
        """
        Received Signal Level
        With all the input parameters to the link budget, the power level arriving at the receiver’s input can be calculated

        """
        prx = self.ptx - self.ltx + self.gtx - \
            self.free_space_loss() + self.grx - self.lrx
        return prx

    def fade_margin(self):
        """
            This method calculate the fade margin of the link budget
        """
        fm = self.received_power() - self.rsx
        return fm


class RainFade():

    def __init__(self, rain_rate=115, v_polarization=0.1170, av=0.9700):
        self.R = rain_rate
        self.Kv = v_polarization
        self.av = av
        self.Yrv = 0.0


    def specific_attenuation(self):
        """
            This method calculate the specific attenuation for vertical polarization
            This is required to calculate the rain attenuation
        """
        self.Yrv = self.Kv * math.pow(self.R, self.av)
        return self.Yrv


    def d0(self):
        """
            This method calculate vertical polarization distance
            This is required to calculate the rain attenuation
        """
        return (35 * math.exp(-0.015 * 100))


    def rain_attenuation(self, d):
        """
            This method calculate the rain attenuation
        """
        avr_up = self.Yrv * d
        avr_dwn = 1 + (d / self.d0())
        avr = avr_up / avr_dwn
        return avr