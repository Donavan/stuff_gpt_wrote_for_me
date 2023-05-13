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

    -o, --output: The output folder for the compressed files. If not specified, the script uses the input directory as the output directory.
    -l, --limit: The file size limit in GB. If a file is larger than this size, it will be compressed. Default is 8.0 GB.
    -t, --target: The target file size in GB. The script attempts to compress files to this size. Default is 8.0 GB.
    -p, --parallel: The number of parallel files to process. Default is 8.
    -c, --compressor: The compressor tool to use. Can be either 'handbrake' or 'ffmpeg'. Default is 'handbrake'.
    -b, --bitrate: The estimated bitrate for FFmpeg (e.g. 5000k). Default is '5000k'. This option is only used when FFmpeg is the chosen compressor.


## Examples

Here's an example command:

```bash
python vacuum.py /home/user/videos -o /home/user/compressed_videos -l 10.0 -t 2.0 -p 4 -c ffmpeg -b 4000k
```

This command will search for video files in /home/user/videos. If a file is larger than 10 GB, it will be compressed to around 2 GB and saved to /home/user/compressed_videos. The script will process up to 4 files in parallel. FFmpeg is used as the compressor with an estimated bitrate of 4000k.

## Requirements

    Python 3
    HandBrakeCLI or FFmpeg
    multiprocessing, subprocess, argparse, os, glob, functools, logging (These are standard Python libraries and should be included in most Python installations)