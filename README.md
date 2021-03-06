# YOLO Security

YOLO stands for you only look once and is a process for object detection. 
This app uses YOLO detection to monitor a video stream and send real-time alerts.
  - Advanced object detection
  - Realtime E-Mail alerts

### Getting Started
- If you don't already have one, make a burner E-Mail. I'd strongly recommend GMail for the purpose of uploading images to its Google photos account. 
- Go to [Google Security](https://myaccount.google.com/security) and do a find for "Less secure app access". Turn on less secure app access, this allows your dummy account to send E-Mails within the app.
- Run `cp skeleton_config.py config.py` and fill in the variables with the proper values
- Preferably within a dedicated virtual environment, run `pip install -r requirements.txt`


### Using the GPU
- Run `./tf_gpu_setup.sh`
- Add this to the bottom of your .bashrc
```bash
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"
export CUDA_HOME=/usr/local/cuda
export PATH="$PATH:/usr/local/cuda/bin"
```
- Instead of doing a pip install on requirements use tf_gpu_requirements.txt
> For more info on setting up TF GPU [TF GPU](https://github.com/williamFalcon/tensorflow-gpu-install-ubuntu-16.04)

### Running the app
```sh
# This is it. I know, anti-climactic
python main.py
```

### Todos

 - Store detected object sightings in Elasticsearch
 - Auto backup video into glacier
 - Upload backup of discovered object capture into google pictures (cause free)
 - Broadcast live stream
 - Sniff for mac address & tie to image
 - Set which objects to take note of
 - Expand list of possible detected objects
 - Allow for an offset of objects e.g. ignore 1 vehicle
 - Text alerts
 - Create profiles on frequently detected objects

 
License
----

It's a public repo, do whatever. 

