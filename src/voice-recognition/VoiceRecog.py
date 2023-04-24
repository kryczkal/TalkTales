from Sample import Sample
import numpy as np
import librosa as lb


def CreateOverlappedData(DataIn: list[Sample]) -> list[Sample]:
    # Creates overlapped Form of passed datased with these settings:
    # Window = 2 * duration of sample
    # Overlap = duration of single sample

    DataOut = []
    StartSample = DataIn[0]

    for Temp in DataIn[1:]:
        DataOut.append(Sample(StartSample.ByteData + Temp.ByteData, True, Temp.TimeStamp))
        StartSample = Temp

    return DataOut


def ExtractInformation(DataIn: list[Sample]):
    # Computes all needed indicators 

    for Temp in DataIn:
        Temp.GetMfcc()