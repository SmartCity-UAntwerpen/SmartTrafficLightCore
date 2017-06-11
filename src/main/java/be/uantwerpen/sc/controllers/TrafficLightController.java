package be.uantwerpen.sc.controllers;

import be.uantwerpen.sc.models.LinkEntity;
import be.uantwerpen.sc.models.TrafficLightEntity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by Admin on 10-6-2017.
 */
public class TrafficLightController {

    String coreIp = "143.129.39.151";
    String corePort = "8083";

    public void initiate(long idlink, int progress, String state){
        String data = "";
        try {
            URL url = new URL("http://"+coreIp+":"+corePort+"/tlight/"+idlink+"/"+progress+"/"+state);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

            if (conn.getResponseCode() != 200) {
                throw new RuntimeException("Failed : HTTP error code : "
                        + conn.getResponseCode());
            }

            BufferedReader br = new BufferedReader(new InputStreamReader(
                    (conn.getInputStream())));

            String output;
            System.out.println("Output from Server .... \n");
            while ((output = br.readLine()) != null) {
                data = data + output;
                System.out.println(output);
            }

            TrafficLightEntity trafficLightEntity = new TrafficLightEntity();
            trafficLightEntity.setState(state);
            trafficLightEntity.setTlid(Integer.parseInt(output));
            trafficLightEntity.setPlaceVertex(progress);

            conn.disconnect();

        } catch (MalformedURLException e) {

            e.printStackTrace();

        } catch (IOException e) {

            e.printStackTrace();

        }
    }
}
