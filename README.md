# Tiny Bandit

Inspired by my prior [Tiny TV](https://github.com/eat-sleep-code/tiny-tv) project, we are back with Tiny Bandit.  Tiny Bandit is a miniaturized version of a casino gaming machine.   

The initial game under development is Slots.  However, Tiny Bandit is designed to host multiple games in the future.   

---

## Installation

Installation of the program, any software prerequisites, as well as the display driver can be completed with the following two-line install script.

```
wget -q https://raw.githubusercontent.com/eat-sleep-code/tiny-bandit/main/install-tiny-bandit.sh -O ~/install-tiny-bandit.sh
sudo chmod +x ~/install-tiny-bandit.sh && ~/install-tiny-bandit.sh
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
- [ ] Add jackpot animation 
- [ ] Add wild animation 
- [ ] Add actual mask
- [ ] Add splash screen / menu
- [X] Write install script
- [ ] Build physical Tiny Bandit machine and document the process
- [ ] Add web service integration to allow date-specific promotions and possible Leaderboard
