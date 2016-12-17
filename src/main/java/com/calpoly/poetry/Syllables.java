package com.calpoly.poetry;

import java.io.*;
import java.util.*;
import java.net.URL;
import com.sun.speech.freetts.lexicon.LetterToSound;
import com.sun.speech.freetts.lexicon.LetterToSoundImpl;
import java.net.MalformedURLException;

/**
 * Hello world!
 *
 */
public class Syllables
{
    public static final String LTS_FILE_URL = "file:./cmulex_lts.bin";
    private LetterToSoundImpl lts;
    public Syllables() {
        URL ltsFileURLPath = null;
        try {
            ltsFileURLPath = new URL(LTS_FILE_URL);
        } catch (MalformedURLException e) {
            System.err.println("Caught Error:" + e);
            System.exit(1);
        }
        try {
            this.lts = new LetterToSoundImpl(ltsFileURLPath, true);
        } catch (IOException e) {
            System.err.println("Caught Error:" + e);
        }
    }
    public String[] getPhonemes(String word) {
        if (word == null) {
            return new String[0];
        }
        String[] rawPhones = this.lts.getPhones(word,"");
        String[] phones = new String[rawPhones.length];
        for (int i = 0; i < rawPhones.length; i++) {
            if (rawPhones[i].equals("ax")) {
                phones[i] = "AH3";
            } else {
                phones[i] = rawPhones[i].toUpperCase();
            }
        }
        return phones;
    }
    public static String phonemesToJSON(String[] phones) {
        String[] quotedPhones = new String[phones.length];
        for (int i = 0; i < phones.length; i++) {
            quotedPhones[i] = "\"" + phones[i] + "\"";
        }
        return "[" + 
            String.join(",",quotedPhones)
            + "]";
    }
    public static void main(String[] args) {
        //URL ltsFileURLPath = null;
        //LetterToSoundImpl lts = null;
        if (args.length < 0) {
            System.exit(22);
        }

        //try {
        //    ltsFileURLPath = new URL(LTS_FILE_URL);
        //} catch (MalformedURLException e) {
        //    System.err.println("Caught Error:" + e);
        //}

        //try {
        //    lts = new LetterToSoundImpl(ltsFileURLPath, true);
        //} catch (IOException e) {
        //    System.err.println("Caught Error:" + e);
        //}
        //String[] phones = lts.getPhones("frabjous", "");

        Syllables syl = new Syllables();
        String[] phones = syl.getPhonemes(args[0]);
        System.out.print(syl.phonemesToJSON(phones));
    }
}
