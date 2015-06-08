import java.io.*;
import javax.sound.sampled.*;

public class Test {
	public static void main (String [] args){
		/*
		File file = new File("AveMaria.mp3");
		try {
			AudioInputStream in= AudioSystem.getAudioInputStream(file);
			System.out.print("pls");
			AudioInputStream din = null;
			AudioFormat baseFormat = in.getFormat();
			AudioFormat decodedFormat = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 
			                                            baseFormat.getSampleRate(),
			                                            16,
			                                            baseFormat.getChannels(),
			                                            baseFormat.getChannels() * 2,
			                                            baseFormat.getSampleRate(),
			                                            false);
			din = AudioSystem.getAudioInputStream(decodedFormat, in);
		} catch (Exception e){
			System.out.println(e.getMessage());
		}
		*/
		testPlay("AveMaria.mp3");
	}
	public static void testPlay(String filename)
	{
	  try {
	    File file = new File(filename);
	    AudioInputStream in= AudioSystem.getAudioInputStream(file);
	    AudioInputStream din = null;
	    AudioFormat baseFormat = in.getFormat();
	    AudioFormat decodedFormat = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 
	                                                                                  baseFormat.getSampleRate(),
	                                                                                  16,
	                                                                                  baseFormat.getChannels(),
	                                                                                  baseFormat.getChannels() * 2,
	                                                                                  baseFormat.getSampleRate(),
	                                                                                  false);
	    din = AudioSystem.getAudioInputStream(decodedFormat, in);
	    // Play now. 
	    rawplay(decodedFormat, din);
	    in.close();
	  } catch (Exception e)
	    {

			System.out.print("ok");
	        //Handle exception.
	    }
	}
	private static void rawplay(AudioFormat targetFormat, AudioInputStream din) throws IOException,                                                                                                LineUnavailableException
	{
	  byte[] data = new byte[4096];
	  SourceDataLine line = getLine(targetFormat); 
	  if (line != null)
	  {
	    // Start
	    line.start();
	    int nBytesRead = 0, nBytesWritten = 0;
	    while (nBytesRead != -1)
	    {
	        nBytesRead = din.read(data, 0, data.length);
	        if (nBytesRead != -1) nBytesWritten = line.write(data, 0, nBytesRead);
	    }
	    // Stop
	    line.drain();
	    line.stop();
	    line.close();
	    din.close();
	  } 
	}
	private static SourceDataLine getLine(AudioFormat audioFormat) throws LineUnavailableException
	{
	  SourceDataLine res = null;
	  DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
	  res = (SourceDataLine) AudioSystem.getLine(info);
	  res.open(audioFormat);
	  return res;
	} 
}
