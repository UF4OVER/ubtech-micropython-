"""
基于micro python的UBT-12HB舵机的驱动
目前只有我一个人在写这个驱动
"""

HEAD_one = 0XFA
HEAD_two = 0XAF

sport = 0x01
led_on_off = 0x04
change_id = 0xcd
read_angle = 0x02
set_angle_cor = 0xd2
read_angle_cor = 0xd4
"""
舵机指令
"""


def adv(data):
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


class UBT_SERVO:
    def __init__(self, uart, id):
        self.uart = uart
        self.id = id

    def servo_do(self, Terminal, Time, Achtime8l, Achtime8H):
        """
          :param Terminal: 位置
          :param Time: 时间
          :param Achtime8l:
          :param Achtime8H:
          
          """

        # 校验码

        _check_num = self.id + sport + Terminal + Time + Achtime8l + Achtime8H

        # 发送数据包

        self.uart.write(bytearray([0XFA, 0XAF, self.id, sport, Terminal, Time, Achtime8l, Achtime8H, _check_num, 0XED]))
        self.uart.write("\r\n")

    def change_id(self, New_Id):
        _checknumber = self.id + change_id + New_Id

        self.uart.write(
            bytearray([HEAD_one, HEAD_two, self.id, change_id, 0X00, New_Id, 0x00, 0x00, _checknumber, 0XED]))
        self.uart.write("\r\n")

    def led(self, led):
        """

        :param led: 1:led闪烁
                    2:led灯灭
        """
        _checknumber = self.id + led + led_on_off

        self.uart.write(bytearray([HEAD_one, HEAD_two, self.id, led_on_off, led, 0x00, 0x00, 0x00, _checknumber, 0XED]))
        self.uart.write("\r\n")

    def read_angle(self):
        _checknumber = self.id + read_angle

        self.uart.write(
            bytearray([HEAD_one, HEAD_two, self.id, read_angle, 0X00, 0x00, 0x00, 0x00, _checknumber, 0XED]))
        self.uart.write("\r\n")
        self.uart.read(9)
