package com.hubermjonathan.freq;

import net.dv8tion.jda.api.audio.AudioReceiveHandler;
import net.dv8tion.jda.api.audio.CombinedAudio;
import net.dv8tion.jda.api.audio.UserAudio;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.VoiceChannel;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.managers.AudioManager;
import org.jetbrains.annotations.NotNull;

import java.util.Arrays;

public class Listener extends ListenerAdapter {
    @Override
    public void onMessageReceived(@NotNull MessageReceivedEvent event) {
        Message message = event.getMessage();
        String content = message.getContentRaw();
        String[] tokens = content.split(" ");

        if (event.getAuthor().isBot()) return;

        if (tokens[0].equals("..join")) {
            VoiceChannel voiceChannel = message.getMember().getVoiceState().getChannel();
            AudioManager audioManager = event.getGuild().getAudioManager();
            audioManager.openAudioConnection(voiceChannel);
            audioManager.setReceivingHandler(new AudioReceiveHandler() {
                @Override
                public boolean canReceiveCombined() {
                    return true;
                }

                @Override
                public boolean canReceiveUser() {
                    return true;
                }

                @Override
                public void handleCombinedAudio(@NotNull CombinedAudio combinedAudio) {
                }

                @Override
                public void handleUserAudio(@NotNull UserAudio userAudio) {
                    System.out.println(Arrays.toString(userAudio.getAudioData(1)));
                    System.out.println(userAudio.getUser().getName());
                }
            });
        } else if (tokens[0].equals("..leave")) {
            AudioManager audioManager = event.getGuild().getAudioManager();
            audioManager.closeAudioConnection();
        }
    }
}
