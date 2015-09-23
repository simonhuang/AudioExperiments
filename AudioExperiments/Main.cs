using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Media;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AudioExperiments
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
        }

        private void Main_Load(object sender, EventArgs e)
        {

        }

        private void play_audio(object sender, EventArgs e)
        { 
            string filePath = @"C:\Users\simon_000\Music\test2.wav";
            WaveGenerator wave = new WaveGenerator(WaveExampleType.ExampleSineWave);
            wave.Save(filePath);            

            SoundPlayer player = new SoundPlayer(filePath);
            player.Play();
        }
    }
}