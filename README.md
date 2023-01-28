# Tiny Bandit

![Tiny Bandit logo](images/icon-128.png)

Inspired by the prior [Tiny TV](https://github.com/eat-sleep-code/tiny-tv) project, we are back with Tiny Bandit.  Tiny Bandit is a miniaturized version of a casino gaming machine that can support multiple simple games.  

The initial games that will be included are:

- Slots 
- FlappyBird<sup> [1](#credit01)</sup> 
- Magic 8<sup> [2](#credit02)</sup>    
---

## Game Development

Interested in adding your own simple game to this project?   If so, here are a few guidelines.

- Your game must be written in Python 3 and utilize the current PyGame library
- Your game must run in a self-contained sub folder
- Your game must expose a base class called `Game`
- Your game must expect no more than two external button inputs (left and right) and/or touchscreen input
- Your game must use the included `gpio.py` for GPIO interactions 

---

## Installation

Installation of the program, any software prerequisites, as well as the display driver can be completed with the following two-line install script.

```
wget -q https://raw.githubusercontent.com/eat-sleep-code/tiny-bandit/main/install-tiny-bandit.sh -O ~/install-tiny-bandit.sh
sudo chmod +x ~/install-tiny-bandit.sh && ~/install-tiny-bandit.sh
```

---

## Audio Settings

If you are using a USB audio device you may need to edit the `/usr/share/alsa/alsa.conf` file for audio output to function properly.  Set the following values:

```sh
defaults.ctl.card 1
defaults.pcm.card 1
```
---

## Autostart at Bash Login
To autostart the program as soon as a Bash shell login occurs, execute the following command:

```
sudo nano .bashrc
```

Add the following line to the end of the file and then save the file:

```
sudo python3 ~/tiny-bandit/tiny-bandit.py --noX=True
```

---

## Autostart at Desktop Login

To autostart the program as soon as the Raspberry Pi OS desktop starts, execute the following command:

```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

Add the following line to the end of the file and then save the file:

```
@lxterminal --geometry=1x1 -e sudo python3 /home/pi/tiny-bandit/tiny-bandit.py
```

---

## To-Do List:

- [X] Display current coins (and freeplays?)
- [X] Add or deduct coins (and freeplays?)
- [X] Add jackpot image 
- [X] Add wild image 
- [X] Add actual mask
- [X] Add splash screen / menu
- [X] Write install script
- [X] Add Sounds for FlappyBird
- [X] Blit text for Magic 8 result
- [ ] Blit helper text to tell user to click button?
- [ ] Add icons and menu icons for Lucky Day
- [ ] Finish Lucky Day
- [ ] Build physical Tiny Bandit machine and document the process
- [ ] Ensure buttons are correctly setup to trigger games as appropriate
- [ ] Add web service integration to allow date-specific promotions and possible Leaderboard

---
## Credits

1. <span id="credit01">FlappyBird</a> was originally created by [Dong Nguyen](https://dotgears.com).  The instance included in this repository uses unique code, but does repurpose some of the original game's imagery.

2.  <span id="credit02">Magic 8</span> is inspired by [Mattel's Magic 8 Ball](https://shop.mattel.com/collections/family-party-games#filter.ss_filter_tags_subtype=Magic%208%20Ball). 