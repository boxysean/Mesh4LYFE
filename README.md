# Mesh4LYFE

![Mesh4LYFE](https://github.com/boxysean/Mesh4LYFE/raw/master/images/mesh4lyfe.png)

## About

Eight routers connected over a wireless mesh network, cooperating to blink Conway's Game of Life in realtime.

[Mesh4LYFE on Vimeo](http://vimeo.com/35936030)

The routers used in the video are Netgear WNDR3700v2s running [OpenWrt](https://openwrt.org/). They are communicating using [B.A.T.M.A.N. advanced](http://www.open-mesh.org/wiki/batman-adv) on their 5.1 GHz radios.

This project was conceived and made during [Art Hack Day](http://arthackday.net/319scholes/).

## Installation Instructions

1. Install OpenWrt on routers with `kmod-batman-adv` and `python` packages
2. Move this code into `/root` on router
3. Configure variables in `/root/init.sh`
4. Add line `. /root/init.sh` to `/etc/rc.local` (before `exit` command!)
5. Repeat steps 2-4 for each router (note: `scripts/sync.sh` may help you)
6. Pick your favourite router and change `MASTER=1` in `/root/init.sh`
7. Reboot all routers, watch them blink!

## Credits

Thanks to Jonathan Kiritharan who made the project with me.
