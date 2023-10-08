
import csv;
import os;

class DoingParser:

    def __init__(self, doing_string: str, sign: str = '|') -> None:
        self.separate_string: list = doing_string.split(sign)
        print(self.separate_string)
        self.sep:str = ';'

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
    
    def WriteInCSV(self, path_of_csv: str) -> None:
        with open(path_of_csv, 'a',encoding='UTF8') as file:
            file.write(self.CreateTimeDoingStroke())
            file.writelines(self.CreateFlagsStroke())


    def RefreshCSV(self, path_of_csv: str, header:str) -> None:
        with open(path_of_csv, 'w') as file:
            file.write(header + '\n')