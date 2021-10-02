# this file is loaded at ~/.profile
# with adding line . ~/sensorit/.profile

. ~/sensorit/.env

alias ll="ls -lah"

kappe () {
        kappe_ip=$(curl -u $VALLE_DYNDNS_USERNAME:$VALLE_DYNDNS_PASSWORD http://valle.fi/dyndns/)
        ssh $KAPPE_USERNAME@$kappe_ip -p $KAPPE_SSH_PORT
}

alias pistorasiat="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS"

alias aon="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py A on"
alias aoff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py A off"

alias bon="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py B on"
alias boff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py B off"

alias con="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py C on"
alias coff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py C off"

alias don="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py D on"
alias doff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py D off"

alias eon="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py E on"
alias eoff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py E off"

#alias fon="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS ''"
#alias foff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS ''"

alias gon="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py G on"
alias goff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py G off"

alias hon="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py H on"
alias hoff="ssh $PISTORASIAT_USERNAME@$PISTORASIAT_ADDRESS python3 $PISTORASIAT_ROOT_DIRECTORY/remote_control.py H off"

alias wsock="cd $ROOT_DIRECTORY/status_files; nohup websocat -tvvv ws://$(cat $ROOT_DIRECTORY/status_files/kappe_ip):$WEBSOCKET_PORT writefile:$ROOT_DIRECTORY/status_files/websocket_output --ping-interval 60 & >/dev/null"
alias wsockint="cd $ROOT_DIRECTORY/status_files; nohup bash $ROOT_DIRECTORY/websocket_interpreter.sh & >/dev/null"
