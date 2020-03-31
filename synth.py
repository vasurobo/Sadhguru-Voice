# -*- coding: utf-8 -*-
from __future__ import print_function

from hyperparams import Hyperparams as hp
import numpy as np
import tensorflow as tf
from utils import *
import codecs
import re
import os
import io
import unicodedata
from scipy.io.wavfile import write
from tqdm import tqdm
from networks import TextEnc, AudioEnc, AudioDec, Attention, SSRN
import subprocess
import shlex


class Graph:


    


    def __init__(self,num=1):

        # Load vocabulary
        self.char2idx, self.idx2char = self.load_vocab()

        # Set flag
        training = False

        # Graph
        # Data Feeding
 
         # Synthesize
        self.L = tf.placeholder(tf.int32, shape=(None, None))
        self.mels = tf.placeholder(tf.float32, shape=(None, None, hp.n_mels))
        self.prev_max_attentions = tf.placeholder(tf.int32, shape=(None,))

        
        with tf.variable_scope("Text2Mel"):
            # Get S or decoder inputs. (B, T//r, n_mels)
            self.S = tf.concat((tf.zeros_like(self.mels[:, :1, :]), self.mels[:, :-1, :]), 1)

            # Networks
            with tf.variable_scope("TextEnc"):
                self.K, self.V = TextEnc(self.L, training=training)  # (N, Tx, e)
            with tf.variable_scope("AudioEnc"):
                self.Q = AudioEnc(self.S, training=training)

            with tf.variable_scope("Attention"):
                # R: (B, T/r, 2d)
                # alignments: (B, N, T/r)
                # max_attentions: (B,)
                self.R, self.alignments, self.max_attentions = Attention(self.Q, self.K, self.V,
                                                                         mononotic_attention=(not training),
                                                                         prev_max_attentions=self.prev_max_attentions)
            with tf.variable_scope("AudioDec"):
                self.Y_logits, self.Y = AudioDec(self.R, training=training) # (B, T/r, n_mels)



        # During inference, the predicted melspectrogram values are fed.
        with tf.variable_scope("SSRN"):
            self.Z_logits, self.Z = SSRN(self.Y, training=training)

        with tf.variable_scope("gs"):
            self.global_step = tf.Variable(0, name='global_step', trainable=False)


    def load_vocab(self):
        char2idx = {char: idx for idx, char in enumerate(hp.vocab)}
        idx2char = {idx: char for idx, char in enumerate(hp.vocab)}
        return char2idx, idx2char




class Synthesizer:

    def load_vocab(self):
        char2idx = {char: idx for idx, char in enumerate(hp.vocab)}
        idx2char = {idx: char for idx, char in enumerate(hp.vocab)}
        return char2idx, idx2char

    def text_normalize(self,text):
        text = ''.join(char for char in unicodedata.normalize('NFD', text)
                               if unicodedata.category(char) != 'Mn') # Strip accents

        text = text.lower()
        text = re.sub("[^{}]".format(hp.vocab), " ", text)
        text = re.sub("[ ]+", " ", text)
        return text

    def run_command(self,command):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        print('STDOUT:{}'.format(stdout))


    def load(self):

            session_conf = tf.ConfigProto(
                intra_op_parallelism_threads=2,
                inter_op_parallelism_threads=2)

            self.sess = tf.Session(config=session_conf)

            self.out = io.BytesIO()

            # Load graph
            self.g = Graph(num=1); print("Graph loaded")


            self.sess.run(tf.global_variables_initializer())

            # Restore parameters
            print("Synthesize.py Restore parameters : Text2Mel\n")
            var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'Text2Mel')
            saver1 = tf.train.Saver(var_list=var_list)
            saver1.restore(self.sess, tf.train.latest_checkpoint(hp.voicedir + "-1"))
            print("Text2Mel Restored!")

            var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'SSRN') + \
                       tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'gs')
            saver2 = tf.train.Saver(var_list=var_list)
            saver2.restore(self.sess, tf.train.latest_checkpoint(hp.voicedir + "-2"))
            print("SSRN Restored!")



    



    def synthesize(self,msg):


        # Load vocabulary
        char2idx, idx2char = self.load_vocab()        


        sents = [self.text_normalize(msg).strip() + "E"] # text normalization, E: EOS
        texts = np.zeros((len(sents), hp.max_N), np.int32)
        for i, sent in enumerate(sents):
            texts[i, :len(sent)] = [char2idx[char] for char in sent]
    
        # Load data
        L = texts

        # Feed Forward
            ## mel

        Y = np.zeros((len(L), hp.max_T, hp.n_mels), np.float32)
        prev_max_attentions = np.zeros((len(L),), np.int32)
        for j in tqdm(range(hp.max_T)):
            _gs, _Y, _max_attentions, _alignments = \
                self.sess.run([self.g.global_step, self.g.Y, self.g.max_attentions, self.g.alignments],
                         {self.g.L: L,
                          self.g.mels: Y,
                          self.g.prev_max_attentions: prev_max_attentions})
            Y[:, j, :] = _Y[:, j, :]
            prev_max_attentions = _max_attentions[:, j]

        # Get magnitude
        Z = self.sess.run(self.g.Z, {self.g.Y: Y})

        # Generate wav files
        if not os.path.exists(hp.sampledir): os.makedirs(hp.sampledir)
        
        for i, mag in enumerate(Z):
            print("Generating Wavefile : ", i+1)
            self.wav = spectrogram2wav(mag)
            write(hp.sampledir + "/{}.wav".format(i+1), hp.sr, self.wav)
            #self.run_command("ffmpeg -i videos/talking.wmv -i "+hp.sampledir + "/{}.wav".format(i+1)+" -map 0:v -map 1:a -c:v libx264 -c:a libvorbis -shortest out.mp4")
            write(self.out, hp.sr, self.wav)
            
        #with open("out.mp4","rb") as videof:
         #   vcontent = videof.read()
          #  out = io.BytesIO(vcontent)
        return self.out.getvalue()



#if __name__ == '__main__':




