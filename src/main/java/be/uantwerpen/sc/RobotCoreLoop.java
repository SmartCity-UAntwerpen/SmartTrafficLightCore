package be.uantwerpen.sc;

import be.uantwerpen.sc.controllers.CLightSender;
import be.uantwerpen.sc.controllers.mqtt.MqttLightSubscriber;
import be.uantwerpen.sc.services.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import javax.annotation.PostConstruct;

/**
 * Created by Arthur on 4/05/2016.
 */
@Service
public class RobotCoreLoop implements Runnable
{
    @Autowired
    private MqttLightSubscriber lightSubscriber;

    @Autowired
    private CLightSender cLightSender;

    @Value("${sc.core.ip:localhost}")
    private String serverIP;

    @Value("#{new Integer(${sc.core.port}) ?: 8083}")
    private int serverPort;

    public RobotCoreLoop(){

    }

    @Deprecated
    public void setServerCoreIP(String ip, int port)
    {
        this.serverIP = ip;
        this.serverPort = port;
    }

    public void run() {
        System.out.println("STARTED");

        int c = 0;
        while(c<20){
            cLightSender.sendLightCommand("LIGHT 1 GREEN");
            c++;
        }
        //cLightSender.sendLightCommand("SHUTDOWN");

    }

}
