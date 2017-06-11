package be.uantwerpen.sc.configurations;

import be.uantwerpen.sc.RobotCoreLoop;
import be.uantwerpen.sc.controllers.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationListener;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.event.ContextRefreshedEvent;

/**
 * Created by Thomas on 14/04/2016.
 */
@Configuration
public class SystemLoader implements ApplicationListener<ContextRefreshedEvent>
{
    @Autowired
    private CLightHandler cLightHandler;

    @Value("${sc.core.ip}")
    String serverIP;

    @Value("#{new Integer(${sc.core.port})}")
    int serverPort;

    @Autowired
    private RobotCoreLoop robotCoreLoop;

    //Run after Spring context initialization
    public void onApplicationEvent(ContextRefreshedEvent event)
    {
        //robotCoreLoop = new RobotCoreLoop(queueService, mapController, pathController, pathplanningType, dataService);

        //Temporary fix for new instantiated RobotCoreLoop / QueueConsumer class (no Spring handling)
        robotCoreLoop.setServerCoreIP(serverIP, serverPort);

        new Thread(robotCoreLoop).start();
        new Thread().start();
        //new Thread(cLightHandler).start();
    }
}
