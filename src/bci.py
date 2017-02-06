import open_bci_v3 as bci

NUM_CHANNELS = 8
data = []

numSamples  = 0

def handleSample(sample):
    channels = sample.channel_data[0:NUM_CHANNELS]
    data.append(channels[4])

    print(channels[4])

def main():
    board = bci.OpenBCIBoard(port='/dev/ttyUSB0', filter_data=True, daisy=False)
    print (board.getNbEEGChannels(), "EEG channels and", 
            board.getNbAUXChannels(), "AUX channels at", 
            board.getSampleRate(), "Hz.")

    board.start_streaming(handleSample)
    while True:
        pass

if __name__ == '__main__':
    main()


