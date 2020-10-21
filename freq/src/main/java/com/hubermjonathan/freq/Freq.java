package com.hubermjonathan.freq;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.requests.GatewayIntent;

import javax.security.auth.login.LoginException;

public class Freq {
    public static void main(String[] args) throws LoginException, InterruptedException {
        JDA jda  = JDABuilder.createDefault(System.getenv("TOKEN")).enableIntents(GatewayIntent.GUILD_MEMBERS).build();
        jda.awaitReady();

        jda.addEventListener(new Listener());
    }
}
