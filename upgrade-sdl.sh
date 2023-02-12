cd ~

echo -e ''
echo -e '\033[93mRemove prior user-initiated install attempts... \033[0m'
sudo rm -Rf ~/SDL2-*
sudo rm -Rf /usr/local/lib/libSDL2*


echo -e '\033[93mSet linker location... \033[0m'
export LD_LIBRARY_PATH="/usr/local/lib"
echo $LD_LIBRARY_PATH


echo -e ''
echo -e '\033[93mUninstalling system-provided libraries... \033[0m'
sudo apt remove -y libsdl2*
sudo apt autoremove -y
sudo apt autoclean


echo -e ''
echo -e '\033[93mInstalling build tools... \033[0m'
sudo apt -y install --no-install-recommends build-essential autoconf automake libtool


echo -e ''
echo -e '\033[93mInstalling build dependencies... \033[0m'
sudo apt -y install libasound2-dev libudev-dev libdbus-1-dev libts-dev libpng-dev libjpeg-dev libfreetype6-dev libflac-dev libogg-dev libmpg123-dev libmodplug-dev


echo -e ''
echo -e '\033[93mInstalling SDL 2... \033[0m'
wget https://www.libsdl.org/release/SDL2-2.0.18.tar.gz
tar zxf SDL2-2.0.18.tar.gz
rm SDL2-2.0.18.tar.gz
cd SDL2-2.0.18
./autogen.sh
./configure --disable-pulseaudio --disable-esd --disable-video-wayland --disable-video-opengl --disable-video-x11  #--enable-arm-neon
make -j $(grep -c '^processor' /proc/cpuinfo 2>/dev/null)
sudo make install
cd ~


echo -e ''
echo -e '\033[93mInstalling SDL Image... \033[0m'
wget https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.5.tar.gz
tar zxf SDL2_image-2.0.5.tar.gz
rm SDL2_image-2.0.5.tar.gz
cd SDL2_image-2.0.5
./autogen.sh
./configure --disable-bmp --disable-gif --disable-lbm --disable-pcx --disable-pnm --disable-svg --disable-tga --disable-tif --disable-xcf --disable-xpm --disable-xv --disable-webp
make -j $(grep -c '^processor' /proc/cpuinfo 2>/dev/null)
sudo make install
cd ~


echo -e ''
echo -e '\033[93mInstalling SDL TTF... \033[0m'
wget https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.15.tar.gz
tar zxf SDL2_ttf-2.0.15.tar.gz
rm SDL2_ttf-2.0.15.tar.gz
cd SDL2_ttf-2.0.15
./autogen.sh
./configure --without-x
make -j $(grep -c '^processor' /proc/cpuinfo 2>/dev/null)
sudo make install
cd ~


echo -e ''
echo -e '\033[93mInstalling SDL Mixer... \033[0m'
wget https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.4.tar.gz
tar zxf SDL2_mixer-2.0.4.tar.gz
rm SDL2_mixer-2.0.4.tar.gz
cd SDL2_mixer-2.0.4
./autogen.sh
./configure --disable-music-midi --disable-music-opus
make -j $(grep -c '^processor' /proc/cpuinfo 2>/dev/null)
sudo make install
cd ~


#echo -e ''
#echo -e '\033[93mRemoving build dependencies... \033[0m'
#sudo apt -y remove libasound2-dev libudev-dev libdbus-1-dev libts-dev libpng-dev libjpeg-dev libfreetype6-dev libflac-dev libogg-dev libmpg123-dev libmodplug-dev
