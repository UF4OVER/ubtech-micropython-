import machine
import time 
import UTB

adc1 = machine.ADC(machine.Pin(13))
adc1.atten(machine.ADC.ATTN_11DB)

adc2 = machine.ADC(machine.Pin(14))
adc2.atten(machine.ADC.ATTN_11DB)

uart1 = machine.UART(1, tx=1, rx=2, baudrate=115200)
s1 = UTB.UBT_SERVO(uart1,1)
s8 = UTB.UBT_SERVO(uart1,8)




def average(data):
    """
    加权平滑滤波
    
    :param data: 原始数据
    :return: 加权平滑滤波的值
    """
    a = [0, 0, 0, 0]
    weight = [0.4, 0.3, 0.2, 0.1]

    _data = data  
    for i in range(0, 3):
        a[i + 1] = a[i]  
    a[0] = _data

    sum = 0
    ave1 = 0
    for j in a:
        sum += j
    ave1 = sum / 4

    ave2 = 0
    for j in range(0, 4):
        ave2 += a[j] * weight[j]

    return ave2
while True:
    
    ave1 = average(adc1.read_u16())
    ave2 = average(adc2.read_u16())
    
    s1.servo_do(int((ave1/78)-48),0,0,0)
    s8.servo_do(int((ave2/78)-48),0,0,0)    


    time.sleep(0.01)
    
