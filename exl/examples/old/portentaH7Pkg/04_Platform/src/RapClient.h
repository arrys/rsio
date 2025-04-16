#ifndef RAPCLIENT_H
#define RAPCLIENT_H

#include <vector>
#include <string>
#include <messages.h>
#include <MQTT.h>



class RaPClient {
public:

    // Constructor to initialize the RaPClient with a reference to Serial
    RaPClient(HardwareSerial& serial) : serial(serial) {}

    // Function to push managed system data using the RaPClient
    bool push(const char& name, const Flag& item);

    // Function to push managed system data using the RaPClient
    bool log(const char& msg);

private:
    std::vector<Flag> Panomaly; // Container to store the elements
    HardwareSerial& serial; // Reference to the Serial object
};

#endif // RAPCLIENT_H