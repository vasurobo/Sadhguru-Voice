# Sadhguru - Voice Clone

Sadhguru voice has been cloned! You heard it right. This is just a basic model which was trained on a very small dataset of Sadhguru's speech found on YouTube. We'll work on improving the model in the future.

Please feel free to use and post your feedbacks.

## Audio Samples

Sentence | Synthesized Audio
------------ | -------------
 Don't Complain On Artificial Intelligence| [Play](https://soundcloud.com/vasanth-kumar-266951636/dont-complain-on-artificial?in=vasanth-kumar-266951636/sets/sadhguru-voice-samples)
I like potato chips | [Play](https://soundcloud.com/vasanth-kumar-266951636/i-like-potato-chips?in=vasanth-kumar-266951636/sets/sadhguru-voice-samples)
How deeply you touch another life is how rich your life. | [Play](https://soundcloud.com/vasanth-kumar-266951636/how-deeply-you-touch-another?in=vasanth-kumar-266951636/sets/sadhguru-voice-samples)
Don't be dead serious about your life  |[Play](https://soundcloud.com/vasanth-kumar-266951636/see-dont-be-dead-serious-about?in=vasanth-kumar-266951636/sets/sadhguru-voice-samples)
If god is watching us the least we can to is be entertaining | [Play](https://soundcloud.com/vasanth-kumar-266951636/if-god-is-watching-the-least?in=vasanth-kumar-266951636/sets/sadhguru-voice-samples)
Namaskaram! I hate this world. | [Play](https://soundcloud.com/vasanth-kumar-266951636/namaskaram-i-hate-this-world?in=vasanth-kumar-266951636/sets/sadhguru-voice-samples)
Let the people suffer and die. | [Play](https://soundcloud.com/vasanth-kumar-266951636/let-the-people-suffer-and-die?in=vasanth-kumar-266951636/sets/sadhguru-voice-samples)

## Checkout the video
[![Youtube Video](https://img.youtube.com/vi/Z4C08eSVYnw/0.jpg)](https://www.youtube.com/watch?v=Z4C08eSVYnw)


## Quick Start

## Requirements

* Python 3.6 or Higher
* Tensorflow 1.14.0/1.15.2 (TESTED) (***Note*** : Won't work on Tensorflow above 1.19)
* Platforms : Ubuntu (***T***) / Windows (***T***) & MacOS  (***Not Tested*** : But should work...)


### Setting Up

    git clone https://github.com/vasurobo/Sadhguru-Voice
    cd Sadhguru-Voice
    pip install -r requirements.txt
    
### Download Model

> Important : Download Voice Model from here : [DOWNLOAD NOW](https://drive.google.com/file/d/1VAjoJioMOdSisYKUrrS_T1BgRpedEOfE/view?usp=sharing).


### Running the application

Now just unzip the downloaded archive & move it into Sadhguru-Voice directory as "voice"

The directory structure should look like below :

* Sadhguru-Voice
  * voice
  * app.py
  * *
  * *

Now everything is ready! Open your terminal and enter "python app.py"

That's all! Voila. Now Open your browser and goto Format: [http://127.0.0.1:5000/](http://127.0.0.1:5000)

## Future

- [x] Clone sadhguru's voice
- [ ] Train on bigger speech dataset of sadhguru to improve voice quality.
- [ ] Add spport for longer sentences.
- [ ] Add support for other languages by training on phonetics, idealy based on IPA.

## Credits & References

* EFFICIENTLY TRAINABLE TEXT-TO-SPEECH SYSTEM BASED ON DEEP CONVOLUTIONAL NETWORKS WITH GUIDED ATTENTION. [Link](https://arxiv.org/pdf/1710.08969.pdf)
* Exploring Transfer Learning for Low Resource Emotional TTS. [Link](https://arxiv.org/pdf/1901.04276.pdf)
* Credits : [Keithito's Tacotron](https://github.com/keithito/tacotron), [Kyubyong's DC-TTS](https://github.com/Kyubyong/dc_tts), [SeanPLeary](https://github.com/SeanPLeary/dc_tts-transfer-learning)



