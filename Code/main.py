from FMOD import Data
from ..Banks import TriggerBank

if __name__ == '__main__':
    #Init
    TriggerBank.TriggerBank()
    TriggerBank.load()
    TriggerBank.prepare_event()
    Data.Data()
