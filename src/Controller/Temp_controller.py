from . import Freenove_DHT as DHT

DHTPin = 11  # define the pin of DHT11

def loop():
    dht = DHT.DHT(DHTPin)  # create a DHT class object
    counts = 0  # Measurement counts
    while (True):
        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0, 15):
            '''
            read DHT11 and get a return value. Then determine whether data read is normal according
            to the return value
            '''
            chk = dht.readDHT11()
            if (chk is dht.DHTLIB_OK):
                '''
                read DHT11 and get a return value. Then determine
                whether data read is normal according to the return value
                '''
                print("DHT11,OK!")
                break
            time.sleep(0.1)
        print("Humidity : %.2f, \t Temperature : %.2f \n" % (dht.humidity, dht.temperature))
        time.sleep(2)