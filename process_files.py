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
duration: format HH:MM:SS
'''
def extract_audio(out_file, file_in, start_time, duration):
    command = [
        'ffmpeg',
        '-ss',
        start_time,
        '-i',
        file_in,
        '-t',
        duration,
        out_file
    ]
    sp.check_call(command)

'''
extracted_file: input .wav file
'''
def diarize(extracted_file):
    ## currently set up to be run from host machine
    ## need to test running inside of VM
    command = [
        '/home/vagrant/bin/speech2text.sh',
        ' /vagrant/'+extracted_file
    ]
    sp.check_call(command)

'''
input_file: human created csv file
'''
def make_tuples_BLAB(input_file):
    human_tuple_list=[]
    with open('/vagrant/'+input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader,None)
        for row in reader:
            word = row[1]
            onset_offset = row[5]
            onset = int(onset_offset.split('_')[0])
            offset = int(onset_offset.split('_')[1])
            human_tuple_list.append((word, onset, offset))
    return human_tuple_list
'''
input_file: input csv file converted from ctm
'''
def make_tuples_ctm(input_file):
    tuple_list = []
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            word = row[1]
            onset_offset = row[0].split('_')
            onset = int(onset_offset[0])
            offset = int(onset_offset[1])
            tuple_list.append((word, onset, offset))
    return tuple_list

'''
input_file: input ctm file
'''
def convert_ctm_to_csv(input_file):
    f = open('/vagrant/build/output/'+input_file)
    lines = f.readlines()
    f.close()
    csv_file = input_file.strip('.ctm')+'.csv'
    with open('/vagrant/'+csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time_interval', "Utterance", "Confidence?"])
        for line in lines:
            split_line = line.split()
            onset_time = int(1000*(float(split_line[2]))) # multiply by 1000 to convert to milliseconds
            offset_time = int(1000*(float(split_line[2])+float(split_line[3]))) # multiply by 1000 to convert to milliseconds
            utterance = split_line[4]
            confidence = float(split_line[5])
            time_interval = str(onset_time)+'_'+str(offset_time)
            writer.writerow([time_interval, utterance, confidence])
    return '/vagrant/'+csv_file

'''
Compare processed file to VSK outputted files (within time range specified)
'''
def compare_files(ctm_list, blab_list, time):
    len_vsk = len(ctm_list)
    len_blab = len(blab_list)
    num_matches = 0
    for blab_line in blab_list:
        blab_word = blab_line[0]
        blab_onset = blab_line[1]
        blab_offset = blab_line[2]
        for ctm_line in ctm_list:
            ctm_word = ctm_line[0]
            ctm_onset = ctm_line[1]
            ctm_offset = ctm_line[2]
            if ctm_word == ctm_word:
                if (abs(blab_onset-ctm_onset) <= time) and (abs(blab_offset-ctm_offset) <= time):
                    print(blab_word, blab_onset, blab_offset)
                    print(ctm_word, ctm_onset, ctm_offset)
                    num_matches+=1
    print("% matched: ", int(num_matches),int(len_blab))
    print()

if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Format of call is 'python process_files.py <input_wav_file> <input_csv_file>'")
        sys.exit(2)
    first_arg = os.path.realpath(sys.argv[1])
    BLAB_csv = os.path.realpath(sys.argv[2]).split('/')[-1]
    out_dir = first_arg.strip('.wav')+'_noise.prof'
    make_noise_profile(out_dir, first_arg)
    print("NOISE PROFILE CREATED")
    denoised_output = first_arg.strip('.wav')+'_denoised.wav'
    denoise_audio(denoised_output, first_arg, out_dir, 0.22)
    print("DENOISED")
    start_time = '01:00:00'
    duration = '00:10:00'
    extracted_file_name_full = first_arg.strip('.wav')+'-'+'_'.join(start_time.split(":"))+'-'+'_'.join(duration.split(":"))+'.mp3'
    extracted_file_name = extracted_file_name_full.split('/')[-1]
    extract_audio(extracted_file_name_full, denoised_output, start_time, duration)
    print("EXTRACTED")
    diarize(extracted_file_name)
    print("DIARIZED")
    ctm_file = convert_ctm_to_csv(extracted_file_name.strip('.mp3')+'.ctm')
    blab_tuples = make_tuples_BLAB(BLAB_csv)
    ctm_tuples = make_tuples_ctm(ctm_file)
