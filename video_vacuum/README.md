# Video Vacuum

Video Vacuum is a Python script that helps you to recompress large video files to save space. It allows you to use either HandBrake or FFmpeg as the compression tool.

It allows you to say "here's a folder, any video files in here that are over X gb run them through handbrake (or ffmpeg) and get them down to size and save them in this output folder,and do P files in parallel"




## Usage

To use Video Vacuum, you need to have either HandBrakeCLI or FFmpeg installed on your system.

Here's how to run Video Vacuum:

```bash
python vv.py <directory> [OPTIONS]
```

The <directory> argument specifies the directory to search for video files.


## Options

Here's a list of all available options:
    --input: The location where the video files to process can be found.
    --output: The location to put the new video files. This defaults to the input folder
    --limit: The minimum size file to process from the input folder measured in gigabytes.
    --threads: The number of threads FFMPEG will use
    --size: How many gigabytes per hour of video at 1080p should the resulting file have. Defaults to 4.
    --mask: A file mask for finding the filenames to process. should default to handling any mp4, mpg, avi or mkv file
    --codec: The codec to use.  Defaults to libx264
    --container: Force output to use this extension


## Examples

Here's an example command:

```bash
python vv.py --input /home/user/videos --output /home/user/compressed_videos --limit 10 --size 2 --threads 4 
```

This command will search for video files in /home/user/videos. If a file is larger than 10 GB, it will be compressed to around 2 GB / hr  and saved to /home/user/compressed_videos.

## Requirements

    Python 3
    FFmpeg
    multiprocessing, subprocess, argparse, os, glob, functools, logging (These are standard Python libraries and should be included in most Python installations)