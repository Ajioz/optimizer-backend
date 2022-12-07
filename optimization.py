from mw_Optimizer import Optimizer, RainFade
from Gaussian import Gaussian 




def search(LTX=3.71, LRX=2.86, ptx=16.0, prx=16.0, gtx=40.5, grx=40.5, rsx=-73.5, freq=12400,):
    '''
        LTX (float) representing the the total system losses in dB at the transmitter
        LRX (float) representing the total system losses in dB at the receiver.
        ptx (floats) represents the transmitter power in dBm.
        prx (floats) represents the receiver power in dBm.
        gtx (floats) represents the transmitter antenna gain in dBi.
        grx (floats) represents the reciever antenna gain in dBi.
        rsx (flaot) represents receiver sensitivity of the antenna
        freg (int) represents the operating frequency of the antenna pair
    '''
    optimization = Optimizer(LTX, LRX, ptx, prx, gtx, grx, rsx, freq)
    rain = RainFade()
    lower_threshold = 1.0
    upper_threshold = 1.5

    step = 0.00
    count = 0

    my_ki = []
    distance = []
    margin = []
    my_fls = []
    my_prx = []

    Avr = []
    Avr_con = []

    FMs = []
    FM_con = []

    while True:
        input_set = optimization.show_input()
        my_los = optimization.los(35, 40)

        ki = optimization.idim_constant(step)
        my_ki.append(ki)

        optimised_distance = optimization.aniebiet()
        distance.append(optimised_distance)

        FLS = optimization.free_space_loss()
        my_fls.append(FLS)

        PRx = optimization.received_power()
        my_prx.append(PRx)

        FM = optimization.fade_margin()
        FMs.append(FM)

        verticalPol = rain.specific_attenuation()

        Av = rain.rain_attenuation(optimised_distance)
        Avr.append(Av)

        Av_condition = Av - 30.0
        Avr_con.append(Av_condition)

        FM_condition = FM - 30.0
        FM_con.append(FM_condition)

        result = FM - Av
        margin.append(result)

        if(result > upper_threshold):
            step += 0.0001
            count += 1

        elif(result < lower_threshold):
            step -= 0.0001
            count += 1

        elif(count >= 60):
            break

    return {
        "Z_Inputs": input_set,
        "LoS": my_los,
        "Vertical_Pol": verticalPol,
        "Ki": my_ki,
        "Distance": distance,
        "Margin": margin,
        "FLs": my_fls,
        "PRx": my_prx,
        "AVr": Avr,
        "AVr_Con": Avr_con,
        "FM": FMs,
        "FM_Con": FM_con
    }


def scatter_plot(distance, margin, FM, Av):
    # x-axis values
    x1 = distance
    # y-axis values
    y1 = margin
    y2 = FM
    y3 = Av

    return {"x1": x1, "y1": y1, "y2": y2, "y3": y3}


def guassian_plot(distance):
    
    OptiGaus = Gaussian()
    data = sorted(distance)

    mean = OptiGaus.calculate_mean(data)
    mean2 = OptiGaus.calculate_mean(distance)
      
    stdev = OptiGaus.calculate_stdev(data)
    stdev2 = 0.625
    
    x1, y1 = OptiGaus.stat_pdf(data, mean, stdev)
    x2, y2 = OptiGaus.stat_pdf(distance, mean2, stdev2)

    return {"x_data": x1, "y_data": y1, "x_data2": x2, "y_data2": y2, "mean": mean, "stdev": stdev}


def compare(distance, margin, FM_con, Av_con):
    # x-axis values
    y1 = margin
    y2 = Av_con
    y3 = FM_con

    # y-axis values
    x1 = distance

    return {"x1": x1, "y1": y1, "y2": y2, "y3": y3}