#!/usr/bin/env python3
import os
import subprocess
import argparse
import glob
import multiprocessing
import functools
import logging


def compress_file_handbrake(file_path, output_folder, target_file_size):
    base_name = os.path.basename(file_path)
    if output_folder != os.path.dirname(file_path):
        base_name = os.path.splitext(base_name)[0]
    output_file = os.path.join(output_folder, base_name + "_compressed.mkv")

    command = [
        "HandBrakeCLI",
        "--input", file_path,
        "--output", output_file,
        "--encoder", "x265",
        "--vb", "8000",
        "--limit-rate", "8000",
        "--quality", "22",
        "--optimize",
        "--encoder-preset", "medium",
        "--encoder-tune", "film",
        "--rate", str(target_file_size) + "k"
    ]
    try:
        subprocess.check_call(command)
        logging.info(f'Successfully compressed: {file_path}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Compression failed for: {file_path}, error: {e}')


def compress_file_ffmpeg(file_path, output_folder, target_file_size, estimated_bitrate):
    base_name = os.path.basename(file_path)
    if output_folder != os.path.dirname(file_path):
        base_name = os.path.splitext(base_name)[0]
    output_file = os.path.join(output_folder, base_name + "_compressed.mkv")

    command_pass1 = [
        "ffmpeg",
        "-y",
        "-i", file_path,
        "-c:v", "libx265",
        "-preset", "medium",
        "-b:v", estimated_bitrate,
        "-pass", "1",
        "-f", "null", "/dev/null"  # Discard output of first pass
    ]
    command_pass2 = [
        "ffmpeg",
        "-i", file_path,
        "-c:v", "libx265",
        "-preset", "medium",
        "-b:v", estimated_bitrate,
        "-pass", "2",
        output_file
    ]
    try:
        subprocess.check_call(command_pass1)
        subprocess.check_call(command_pass2)
        logging.info(f'Successfully compressed: {file_path}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Compression failed for: {file_path}, error: {e}')


def compress_file(file_path, output_folder, target_file_size, tool, estimated_bitrate):
    if tool.lower() == 'handbrake':
        compress_file_handbrake(file_path, output_folder, target_file_size)
    elif tool.lower() == 'ffmpeg':
        compress_file_ffmpeg(file_path, output_folder, target_file_size, estimated_bitrate)


def process_directory(directory, output_folder, file_size_limit, target_file_size, parallel_files, tool, estimated_bitrate, masks):
    files = []
    for mask in masks:
        files.extend(glob.glob(os.path.join(directory, mask)))
    large_files = []
    for file in files:
        size = os.path.getsize(file) / (1024 * 1024 * 1024)  # Size in GB
        if size > file_size_limit:
            large_files.append(file)

    pool = multiprocessing.Pool(processes=parallel_files)
    partial_compress_file = functools.partial(compress_file, output_folder=output_folder, target_file_size=target_file_size, tool=tool, estimated_bitrate=estimated_bitrate)
    pool.map(partial_compress_file, large_files)
    pool.close()
    pool.join()


def main():
    parser = argparse.ArgumentParser(description="Recompress large video files using HandBrake CLI or FFmpeg")
    parser.add_argument("directory", help="Directory to search for video files")
    parser.add_argument("-o", "--output", help="Output folder for compressed files")
    parser.add_argument("-l", "--limit", type=float, help="File size limit in GB", default=8.0)
    parser.add_argument("-t", "--target", type=float, help="Target file size in GB", default=8.0)
    parser.add_argument("-p", "--parallel", type=int, help="Number of parallel files to process", default=8)
    parser.add_argument("-c", "--compressor", help="Compressor tool to use: 'handbrake' or 'ffmpeg'", default='handbrake')
    parser.add_argument("-b", "--bitrate", help="Estimated bitrate for FFmpeg (e.g. 5000k)", default='5000k')
    parser.add_argument("-m", "--mask", nargs='+', help="File masks to match, e.g. *.mkv *.mp4", default=["*.[Mm][Kk][Vv]", "*.[Mm][Pp]4", "*.[Aa][Vv][Ii]", "*.[Mm][Pp][Gg]", "*.[Mm][Pp][Ee][Gg]"])
    args = parser.parse_args()

    if args.output is None:
        output_folder = args.directory
    else:
        output_folder = args.output

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_directory(args.directory, output_folder, args.limit, args.target, args.parallel, args.compressor, args.bitrate, args.mask)

if __name__ == "__main__":
    main()
