#!/bin/bash

date >> timestamp.out
python auto_download_compressed_images.py -f images-names/xdj -d /gpfs/docker_images_largefs/xdj/
date >> timestamp.out
python auto_download_compressed_images.py -f images-names/xdh -d /gpfs/docker_images_largefs/xdh/
date >> timestamp.out
python auto_download_compressed_images.py -f images-names/xdg -d /gpfs/docker_images_largefs/xdg/
date >> timestamp.out
python auto_download_compressed_images.py -f images-names/xdf -d /gpfs/docker_images_largefs/xdf/
date >> timestamp.out
