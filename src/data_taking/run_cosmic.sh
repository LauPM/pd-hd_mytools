#!/usr/bin/env bash

echo -e "\e[36m[INFO] Welcome to the script for acquiring \033[1mCOSMICS RUNS!\033[0m"
echo -e "\e[36m To execute the script just run: \033[1msh run_cosmic.sh <username> <config_file> <runtime> <message> <expert_mode>\033[0m"
echo -e "\e[36m A log.txt file will be generated each time you run this script."
echo -e " If any of the arguments is missing, the script will ask for it."
echo -e " Enjoy! :) \n \e[0m"

# The confirmation message need to be run with $ bash setup.sh (this lines are to allow $ sh setup.sh too)
if [ ! "$BASH_VERSION" ] ; then
    exec /bin/bash "$0" "$@"
fi


if [ -n "$5" ] && [ "$5" = "True" ]; then
    echo "EXPERT_MODE ON: running without confirmation message"
else
    echo -e "\e[31mWARNING: You must MUST be (in np04daq@np04-srv-024) inside \033[1mnp04_pds tmux!\033[0m \e[31m[tmux a -t np04_pds]\e[0m"
    read -p "Are you sure you want to continue? (y/n) " -n 1 -r
    echo -e "\n"

    # If the user did not answer with y, exit the script
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
fi


if [ -n "$1" ];then
    username=$1
    else
        read -p "Enter your username: " username
fi
if [ -n "$2" ];then
    config_file=$2
    else
        read -p "Enter the configuration file [np04_DAPHNE_APAs34_SSP.json]: " config_file
fi
if [ -n "$3" ];then
    runtime=$3
    else
        read -p "Enter the runtime in seconds [RECOMMENDED 480]: " runtime
fi
if [ -n "$4" ];then
    message=$4
    else
        read -p "Please enter a message to be added in the ELisA describing the run: " message
fi

log="cosmic_log_$(date "+%F-%T").txt"

echo "***** Running $config_file *****" | tee -a $log
echo "Running for $runtime seconds" | tee -a $log
echo "dtsbutler mst MASTER_PC059_1 align apply-delay 0 0 0 --force -m 3" | tee -a $log
echo "dtsbutler mst MASTER_PC059_1 faketrig-clear 0" | tee -a $log
echo "nano04rc --partition-number 6 --timeout 120 global_configs/pds_calibration/${config_file} $username np04pds boot start_run --message "\"${message}\"" change_rate 100 wait ${runtime} stop_run" | tee -a $log

dtsbutler mst MASTER_PC059_1 align apply-delay 0 0 0 --force -m 3
dtsbutler mst MASTER_PC059_1 faketrig-clear 0
nano04rc --partition-number 6 --timeout 120 global_configs/pds_calibration/${config_file} $username np04pds boot start_run --message "\"${message}\"" change_rate 100 wait ${runtime} stop_run

if [ $? -ne 0 ]; then
    echo "nanorc exited with errors!" | tee -a $log
    exit 1
fi