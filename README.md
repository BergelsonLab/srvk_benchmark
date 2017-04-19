# srvk_benchmark

srvk_benchmark is a tool for comparing Speech Recognition Virtual Kitchen's eesen-transcriber output to the 
BLAB created annotation files.

## Installation

To start, clone the eesen transcriber:

```
git clone https://github.com/srvk/eesen-transcriber
cd eesen-transcriber
```
(N.B. to run the VM, please download the corresponding virtualizer [here](https://www.virtualbox.org/wiki/VirtualBox))

Now that we have cloned the transcriber, we need to install and download the virtual machine.  From the eesen-transciber
directory, run the following command.

```
vagrant up
```
(N.B. this might take a couple of minutes to complete)

Once the virtual machine has been created, we are now ready to provide our files.  Place any 
wav files (and corresponding BLAB created annotation CSVs) into the eesen-transcriber directory.

Now that the files that we want to compare against are available, we will enter the VM and continue from there.

Run the following command to enter the VM

```
vagrant ssh
```

Once you have entered the virtual machine, follow the next steps to configure the VM for the correct segmentation values.

```
nano /vagrant/Makefile.options
```

change the third line of this file to read

```
SEGMENTS=show.seg
```

*** This change is a workaround to make sure that segmentation of files is not too small

Within the virtual machine, run the following commands to install the necessary dependencies:

```
cd
sudo apt-get install git
sudo add-apt-repository ppa:jonathonf/ffmpeg-3
sudo apt-get update
sudo apt-get install ffmpeg
git clone https://github.com/BergelsonLab/srvk_benchmark
```

## Running the Comparisons
Now that our repo has been cloned, we are ready to run the comparison process.

```
cd srvk_benchmark
python process_files.py /vagrant/<input wav file> /vagrant/<input csv file>
```

If you need to add more files, exit the VM and add more files to the eesen-transcriber directory.

The output will be shown in the VM terminal.
