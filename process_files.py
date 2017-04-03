import csv
import os
import sys
import subprocess as sp


'''
file_in: specify your .wav file
out_file: specify your .prof output file
'''
def make_noise_profile(out_file, file_in):
    command = [
        'sox',
        file_in,
        '-n',
        'noiseprof',
        out_file
    ]
    sp.check_call(command)

'''
file_in: specify your .wav file
out_file: specify your .wav output file
noise_prof_file: specify your .prof input file
sensitivity: specify your sensitivity (recommended 0.2-0.3)
'''
def denoise_audio(out_file, file_in, noise_prof_file, sensitivity):
    command = [
        'sox',
        file_in,
        out_file,
        'noisered',
        noise_prof_file,
        str(sensitivity)
    ]
    sp.check_call(command)

'''
file_in: specify your .wav file
out_file: specify your .mp3 output file
start_time: format HH:MM:SS
end_time: format HH:MM:SS
'''
def extract_audio(out_file, file_in, start_time, end_time):
    command = [
        'ffmpeg',
        '-ss',
        start_time,
        '-i',
        file_in,
        '-t',
        end_time,
        out_file
    ]
    sp.check_call(command)



if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Format of call is 'python process_files.py <input_wav_file>'")
        sys.exit(2)
    first_arg = sys.argv[1]
    out_dir = first_arg.split('.')[0]+'_noise.prof'
    make_noise_profile(out_dir, first_arg)
    denoised_output = first_arg.split('.')[0]+'_denoised.wav'
    denoise_audio(denoised_output, first_arg, out_dir, 0.22)
    start_time = '00:00:00'
    end_time = '00:10:00'
    extracted_file_name = first_arg.split('.')[0]+'-'+'_'.join(start_time.split(":"))+'-'+'_'.join(end_time.split(":"))+'.mp3'
    extract_audio(extracted_file_name, denoised_output, start_time, end_time)
    print("DONE")
