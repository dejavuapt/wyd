
import csv;
import os;
from datetime import date;

class DoingParser:

    def __init__(self, csv_path: str, header: str = "time;doing_text;flag;hours") -> None:
        self.separate_string: list = []
        self.sep:str = ';'
        self.csv_path = csv_path
        self.header_csv = header

    def SetSeparate(self, doing_string: str, sign: str = '|') -> None:
        self.separate_string = doing_string.split(sign);

    def ParseTime(self) -> str:
        return self.separate_string[0]

    def ParseDoing(self) -> str:
        return self.separate_string[1]

    """
    return like [';m;0,5', ';kd;0,2', ';l;0,4']
    """
    def ParseFlags(self) -> list:
        flags: str = self.separate_string[2]
        arr = flags.split(' ') 
        result = [] 
        for i in range(0, len(arr), 2):
            result.append(self.sep + arr[i][2:] + self.sep + arr[i+1]) 
        return result
    

    def CreateTimeDoingStroke(self) -> str:
        return self.ParseTime() + self.sep + self.ParseDoing() + self.sep + self.sep + "\n"
    
    def CreateFlagsStroke(self) -> list:
        return [f'{self.sep}{flag}\n' for flag in self.ParseFlags()]
    
    def WriteInCSV(self) -> None:
        with open(self.csv_path, 'a',encoding='UTF8') as file:
            file.write(self.CreateTimeDoingStroke())
            file.writelines(self.CreateFlagsStroke())


    def RefreshCSV(self) -> None:
        with open(self.csv_path, 'w') as file:
            file.write(self.header + '\n')


    def AddDateRow(self, current_dt: date) -> None:
        with open(self.csv_path, 'a',encoding='UTF8') as file:
            file.write(f'{current_dt.strftime("%d.%m.%y")}{self.sep}{self.sep}{self.sep}')