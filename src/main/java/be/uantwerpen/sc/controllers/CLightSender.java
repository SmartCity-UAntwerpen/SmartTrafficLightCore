package be.uantwerpen.sc.controllers;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

/**
 * Created by Dries on 2/05/2016.
 */
@Service
public class CLightSender
{
    private Socket socket;
    private DataOutputStream dOut;
    private DataInputStream dIn;
    private boolean serverActive;

    @Value("${trafficlightcore.ip:localhost}")
    private String tlightIP;

    @Value("#{new Integer(${trafficlightcore.taskport}) ?: 1313}")
    private int tlightCommandPort;

    public CLightSender()
    {

    }

    @PostConstruct
    private void postConstruct()
    {
        //IP / port-values are initialised at the end of the constructor
        try
        {
            socket = new Socket(tlightIP, tlightCommandPort);
            System.out.println("Communication with TLIGHT: OK!");
            socket.setSoTimeout(500);
            dOut = new DataOutputStream(socket.getOutputStream());
            dIn = new DataInputStream(socket.getInputStream());
            serverActive = true;
        }
        catch(Exception e)
        {
            e.printStackTrace();
            serverActive = false;
        }
    }

    public synchronized boolean sendLightCommand(String str){
        try {
            //byte[] message = str.getBytes();
            //System.out.println(message.toString());
            int attempts = 0;

            str = str.concat("\n");
            byte[] bytes = str.getBytes();

            //while(attempts <5) {
                //Send message
                //dOut.writeInt(message.length); // write length of the message
                dOut.flush();
                dOut.write(bytes);
//                /*
//                //Receive Message
//                try {
//                    //Check if acknowledged
//                    byte[] ackBytes = new byte[4];
//                    dIn.readFully(ackBytes);
//                    String response = new String(ackBytes);
//                    Terminal.printTerminal("Response:" + response);
//                    if(response.startsWith("ACK")  || response.startsWith("Smar")){
//                        //Message acknowledged
//                        return true;
//                    }if(response.startsWith("NACK")){
//                        return false;
//                    }
//
//                    //clear buffer
//                    if(dIn.available() > 0) {
//                        byte[] removed = new byte[dIn.available()];
//                        dIn.readFully(removed);
//                    }
//                }catch(SocketTimeoutException e){
//                    Terminal.printTerminalInfo("SocketTimeout");
//                    e.printStackTrace();
//                }
//                attempts++;
//                */
//            //}

            return true;

        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("IOException");
            return false;
        }
    }

    public boolean close()
    {
        try{
            socket.close();
            return true;
        }catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
}
