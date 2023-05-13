import os
import math
import shlex
import fnmatch
import logging
import argparse
import subprocess


class VideoVacuum:
    def __init__(self, args):
        self.input_folder = args.input
        self.output_folder = args.output
        self.limit = args.limit
        self.target_size = args.size
        self.file_mask = args.mask
        self.threads = args.threads
        self.codec = args.codec
        self.container = args.container

    def process_folder(self):
        for root, dirs, files in os.walk(self.input_folder):
            for basename in files:
                for extension in self.file_mask.split(','):
                    if fnmatch.fnmatch(basename, extension):
                        filename = os.path.join(root, basename)
                        try:
                            if os.path.getsize(filename) >= self.limit * (1024 ** 3):  # convert GB to bytes
                                if not os.path.exists(os.path.join(self.input_folder, basename.rsplit('.', 1)[0] + '_c.' + basename.rsplit('.', 1)[1])):
                                    self.process_file(filename)
                        except OSError as e:
                            logging.error(f"Error processing file {filename}: {e}")

    @staticmethod
    def convert_gb_per_hr_to_kbps(gb_per_hr):
        kilobits_per_gb = 8_589_934.592
        seconds_per_hour = 3600
        return math.ceil(gb_per_hr * kilobits_per_gb / seconds_per_hour)

    def probe_file(self, input_filename):
        # Determine the resolution and duration of the video file
        cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {shlex.quote(input_filename)}'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        width, height = output.strip().split('x')

        width = float(width)
        height = float(height)

        return width * height

    def process_file(self, input_filename):
        print(f"Processing {input_filename}")

        # Calculate the bitrate
        resolution = self.probe_file(input_filename)

        base_resolution = (1080 * 1920)
        res_scale = resolution / base_resolution
        target_bitrate = math.ceil(self.convert_gb_per_hr_to_kbps(self.target_size * res_scale))

        print(f"Res: {resolution},  Rate: {target_bitrate}")


        # Prepare the output file path
        basename = os.path.basename(input_filename)
        filename, ext = os.path.splitext(basename)

        if os.path.abspath(input_filename) == os.path.abspath(self.output_folder):
            filename = f"{filename}_c"

        if self.container is not None:
            ext = f".{self.container}"

        base_name = f"{filename}{ext}"

        output_file = shlex.quote(os.path.join(self.output_folder, base_name))

        # Use ffmpeg to transcode the input file into the output folder using the target bitrate
        cmd = f'ffmpeg -i {shlex.quote(input_filename)} -c:v {self.codec} -threads {self.threads} -b:v {target_bitrate}k {output_file} -loglevel info -progress - 2>&1 >/dev/null'
        print(cmd)
        subprocess.call(cmd, shell=True)
        print()


def parse_args():
    parser = argparse.ArgumentParser(description='Video Vacuum')
    parser.add_argument('--input', type=str, required=True, help='The location where the video files to process can be found.')
    parser.add_argument('--output', type=str, default=None, help='The location to put the new video files. This should default to the input folder.')
    parser.add_argument('--limit', type=int, required=True, help='The minimum size file to process from the input folder measured in gigabytes.')
    parser.add_argument('--threads', type=int, default=1, help='The number of threads FFMPEG will use')
    parser.add_argument('--size', type=int, default=4, help='How many gigabytes per hour of video at 1080p should the resulting file have. Defaults to 4.')
    parser.add_argument('--mask', type=str, default='*.mp4,*.mpg,*.avi,*.mkv', help='A file mask for finding the filenames to process. should default to handling any mp4, mpg, avi or mkv file')
    parser.add_argument('--codec', type=str, default="libx264", help='The codec to use.  Defaults to libx264')
    parser.add_argument('--container', type=str, default=None, help='Force output to use this extension')


    return parser.parse_args()

def main():
    args = parse_args()
    video_vacuum = VideoVacuum(args)
    video_vacuum.process_folder()

if __name__ == "__main__":
    main()
