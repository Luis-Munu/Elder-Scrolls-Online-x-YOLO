# Elder Scrolls Online x YOLO

![sc1](https://github.com/Valkam-Git/Elder-Scrolls-Online-x-YOLO/assets/82890199/d806e64e-2a73-47bb-a998-bc2443a865ec)

A YOLOv5 model for Elder Scrolls Online

Trained at 4k res, detects Bal-Foyen enemies, Harvest map indicators and various resources in real time.
The accuracy detecting resources leaves a lot to be desired due to the low size of the labeled dataset, labeling by hand is hard guys!

Benchmarks around 15-20 fps at populated areas on a 4k monitor, keep in mind that it will be much faster on lower resolutions. Still, I recommend porting it to TensorRT to earn much better speeds, beware that there's currently a bug that forces a low input resolution when porting a YOLO model to TensortRT, you may have to tinker with input sizes.

There's also a python script that works as a transparent overlay to draw detected objects in real time as you play.
What you do with this is up to you, botting is against the TOS of the game.

If for some reason you feel compelled to enhance the model hit me up on GitHub.
