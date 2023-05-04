from Sample import VoiceSample
import numpy as np
import librosa as lb


def CreateOverlappedData(DataIn: list[VoiceSample]) -> list[VoiceSample]:
    # Creates overlapped Form of passed datased with these settings:
    # Window = 2 * duration of sample
    # Overlap = duration of single sample

    DataOut = []
    StartSample = DataIn[0]

    for Temp in DataIn[1:]:
        DataOut.append(VoiceSample(StartSample.data + Temp.data, True, Temp.time_stamp))
        StartSample = Temp

    return DataOut


def ExtractInformation(DataIn: list[VoiceSample]):
    # Computes all needed indicators 

    for Temp in DataIn:
        Temp.mfcc_get()