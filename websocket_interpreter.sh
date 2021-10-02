#!/bin/bash

. ~/sensorit/.env

saved_hash=""
output_file="$ROOT_DIRECTORY/status_files/websocket_output"
remote_control_program="remote_control.py"

while true;
do
incoming_hash=$(md5sum <<< cat $output_file)
if [[ $incoming_hash != $saved_hash ]]; then
	case $(tail -1 $output_file) in

		"bon")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program B on
			;;

		"boff")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program B off
			;;

		"con")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program C on
			;;

		"coff")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program C off
			;;

		"eon")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program E on
			;;

		"eoff")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program E off
			;;

		"gon")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program G on
			;;

		"goff")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program G off
			;;

		"hon")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program H on
			;;

		"hoff")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program H off
			;;

		"gaon")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program GROUP_A on
			;;

		"gaoff")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program GROUP_A off
			;;

		"gbon")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program GROUP_B on
			;;

		"gboff")
			ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/$remote_control_program GROUP_B off
			;;
	esac

	saved_hash=$incoming_hash
fi
sleep 0.2
done
