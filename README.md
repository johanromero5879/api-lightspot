<div align="center">
    <div>
        <img 
            src="https://raw.github.com/johanromero5879/api-lightspot/main/assets/images/long_logo.png"
            width="50%"
            alt="Lightspot logo"
        />
        <h1 align="center">API v0.9.0</h1>
    </div>
</div>

An API to handle lightning activity data provided by [WWLLN](http://wwlln.net/) and uses geocode services.

### Requirements
- Python 3.11

### Install Nominatim Server
If you want to **use geolocation services**, you must **install an own server**. 
For now, this software uses [Nominatim](https://nominatim.org/) for reverse geocode. 

The easiest way to install a server is through [Docker](https://www.docker.com/).
Once you already have docker you can execute the following command and wait for 
the setup (it will take several minutes):
```
docker run -it `
  -e PBF_URL=https://download.geofabrik.de/south-america/colombia-latest.osm.pbf `
  -e REPLICATION_URL=https://download.geofabrik.de/south-america/colombia-updates/ `
  -e UPDATE_MODE=continuous `
  -e REVERSE_ONLY=true `
  -p 8000:8080 `
  --name nominatim `
  mediagis/nominatim:4.2
```
Take into account: 
- The ` character represents a break line, this might change in each OS.
- The above command will download Colombia data. You might check more info by [Geofabrik](https://download.geofabrik.de/).
- If you want to know all available versions on Docker, you can go to [nomitamin-docker](https://github.com/mediagis/nominatim-docker) on GitHub.
- Check the [installation guide](https://nominatim.org/release-docs/latest/admin/Installation/) by Nominatim for further info.

### Setup
1. Make a virtual machine in the root with the command: `python -m venv env`.
2. Start the virtual machine and execute `activate` command within the path `env/scripts`.
3. Install the dependencies on the root with the command: `pip install -r requirements.txt`.
4. Copy and paste `.env.example`, rename the copy as `.env`, then set all the environment variables.

### Notes
- Make sure to put an email that has enabled SMTP settings, otherwise features 
that envolved email sending will not work. 

### Execute
Type the command `python main.py`.

### Unit Tests
1. Copy and paste `.env.example`, rename the copy as `.env.test`, then set all the environment variables.
2. Type the command `python run_tests.py`

### Client
You can check the client project in this repository: [Karenyepes/lightspot](https://github.com/Karenyepes/lightspot)

---
_Developed by [Johan Romero](https://github.com/johanromero5879)_
