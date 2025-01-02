# AcousticID
Project that will run a web server that can accept a short (10 seconds) wav file and id the song, and return back metadata for that song

## Steps to install

> NOTE: I'm installing on a Debian 12 LXC in my Proxmox Homelab, so these instructions are for me and that environment
> 
### Prerequesitse (for my setup)

* Self Hosted Infisical instance
* New fresh Deb 12 LXC in Proxmox
* Python 3.11 installed

### Additional steps

* Create a new blank Deb 12 LXC
* Install [Infisical CLI](https://infisical.com/docs/cli/overview)
* cd to `/opt`
* `gh clone acousticid`
* `cd acousticid`
* `infisical login`
* 