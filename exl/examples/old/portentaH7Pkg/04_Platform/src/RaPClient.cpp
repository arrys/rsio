#include "RaPClient.h"


// Implementation of the push function
bool RaPClient::push(const char& name, const Flag& item) {
    try {
        
        // implement the MQTT push
        int x=0.0;

         if (name == 'Panomaly'){
            serial.println("Send Panomaly as MQTT message");    //TODO:implement
         }else if (name == 'RobotPose')
         {
            serial.println("Send RobotPose as MQTT message");    //TODO:implement
         }
          

        return true; // Return true if the push was successful
    } catch (const std::exception& e) {
        // Handle any exceptions that might occur
        return false; // Return false if the push failed
    }
}

// Implementation of the push function
bool RaPClient::log(const char& msg) {
    try {
        
        // implement the MQTT log         
        serial.println(msg);    //TODO:implement
        
        return true; // Return true if the push was successful
    } catch (const std::exception& e) {
        // Handle any exceptions that might occur
        return false; // Return false if the push failed
    }
}