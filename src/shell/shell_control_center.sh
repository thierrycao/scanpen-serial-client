##########################################################################
# File Name: PLAYBACK_CONTROL.sh
# Author: ThierryCao
# mail: iamthinker@163.com
# Created Time: mar 03 mar 2020 18:04:46 CST
#########################################################################
#!/bin/zsh

function get_platform()
{
	echo $(uname | tr '[:upper:]' '[:lower:]')
}

function playback_menu()
{
    #echo "playback_menu: $@"
    
    local option
    local OPTIND

    if command -v ffplay > /dev/null;then
			#echo "found ffplay"
			ffplay_path="ffplay"
		else 
			ffplay_path="$iutils/ffplay-darwin"
		fi
	#echo "ffplay_path: $ffplay_path"
	if [[ $(get_platform) == 'darwin' ]];then
		result=$(ps aux | grep ffplay | grep -v grep | grep -v grep | awk -F ' '  '{ print $2}')
	else
		result=$(ps -lfe | grep ffplay | grep -v grep | awk -F ' '  '{ print $4}')
	fi

    while getopts :b:lprsh option
    do
        printChar="$OPTARG"
        case $option in
            b)
                isURL=$(echo $printChar | grep -E 'http(s)?')
                if [ "$isURL" ];then
                    {
                        $ffplay_path -nodisp -autoexit -loglevel quiet $printChar
                        #curl -L $1 | ffplay -nodisp -autoexit -
                    } &
                fi
                ;;
            p)
                [[ "v$result" != "v" ]] && kill -STOP $result
                ;;
            r)
                [[ "v$result" != "v" ]] && kill -CONT $result
                ;;
            s)
                [[ "v$result" != "v" ]] && kill -KILL $result
                ;;
            l)
                [[ "v$result" != "v" ]] && echo "ffplay process: $result"
                ;;
            ?)
                echo "playback_menu: [invalid charactor]!"
                ;;
        esac

    done
    shift $(($OPTIND - 1))
}

function record_menu()
{
    echo "record_menu: $@"
    
    local option
    local OPTIND


    while getopts :b:sh option
    do
        printChar="$OPTARG"
        case $option in
            b)
                {
                    exec 6<> "$printChar"
                    arecord -r 16000 -f S16_LE -c 1 >&6
                    exec 6>&-
		        } &
                ;;
            s)
                result=$(ps -lfe | grep arecord | grep -v grep | awk -F '  '  '{ print $4}')
                if [ "$result" != '' ];then
                    exec 6>&-
                    kill -KILL $result
                fi
                ;;
            ?)
                echo "record_menu: [invalid charactor]!"
                ;;
        esac

    done
    shift $(($OPTIND - 1))
}

function volume_control()
{
    if [[ $(get_platform) == 'darwin' ]];then   
        # osascript -e 'display notification "通知内容" with title "标题" subtitle "子标题"'
        #
        sysValue=$( osascript -e 'output volume of (get volume settings)' )
        muted=$( osascript -e 'output muted of (get volume settings)' )


        while getopts :s:mudgh option
        do
            printChar="$OPTARG"
            case $option in
                s)
                    # echo $@
                    if [ $OPTARG -gt -1 ] && [ $OPTARG -lt 101 ];then
                        # pactl set-sink-volume 0 $OPTARG% && notify-send 'Volume:'$OPTARG -t 1000 && echo "set volume:"$OPTARG"%"
                        osascript -e 'set volume output volume '$OPTARG'' && osascript -e 'display notification "音量'$OPTARG'" with title "呆呆🤖️提醒你⏰" ' && echo "set volume:"$OPTARG"%"
                    fi
                    ;;
                m)
                    pactl set-sink-mute 0 toggle
                    if [ $muted == 'yes' ];then
                            osascript -e 'display notification "静音了😯" with title "呆呆🤖️提醒你⏰" '
                            # notify-send 'Volume - '$sysValue -t 1000
                    else
                            osascript -e 'display notification "静音了😯" with title "呆呆🤖️提醒你⏰" '

                            # notify-send 'Muted' -u critical -t 1500
                    fi
                    ;;
                u)
                    up=$((10#${sysValue}+5))
                    if [ $up -le 100 ];then
                            # pactl set-sink-volume 0 ${up}%
                            # notify-send 'Volume - '$up -t 1000
                            osascript -e 'set volume output volume '$up'' && osascript -e 'display notification "音量'$up'" with title "呆呆🤖️提醒你⏰" ' && echo "set volume:"$up"%"

                            if [ $muted == 'yes' ];then
                                    pactl set-sink-mute 0 0
                            fi
                    fi
                    ;;
                d)
                    current=$((10#${sysValue}-5))
                    if [ $current -lt 0 ];then
                        current=0
                    fi

                    if [ $current -gt 0 ];then
                            osascript -e 'set volume output volume '$current'' && osascript -e 'display notification "音量'$current'" with title "呆呆🤖️提醒你⏰" ' && echo "set volume:"$current"%"

                            # pactl set-sink-volume 0 ${current}%
                            # notify-send 'Volume - '$current -t 1000
                            # if [ $muted == 'yes' ];then
                            #         pactl set-sink-mute 0 0
                            # fi
                    elif [ $current -eq 0 ];then
                            osascript -e 'display notification "音量'$current'" with title "呆呆🤖️提醒你⏰" '
                            # pactl set-sink-volume 0 ${current}%
                            # pactl set-sink-mute 0 1
                    fi
                    ;;
                g)
                    osascript -e 'display notification "音量'$sysValue'" with title "呆呆🤖️提醒你⏰" ' && echo "当前音量: $sysValue"
                    ;;
                ?)
                    echo "record_menu: [invalid charactor]!"
                    ;;
            esac

        done
        shift $(($OPTIND - 1))

    else
        sysValue=$( pacmd info|grep 'volume: front-left: [0-9]\+'|head -n 1|sed 's/.*: [0-9]\+ \/  \? \?//g'|sed 's/%.*//g' )
        muted=$( pacmd info|grep -iE "muted: no$|muted: yes$"|head -n 1|sed 's/.*muted: //g' )

        while getopts :s:mudgh option
        do
            printChar="$OPTARG"
            case $option in
                s)
                    # echo $@
                    if [ $OPTARG -gt -1 ] && [ $OPTARG -lt 101 ];then
                        pactl set-sink-volume 0 $OPTARG% && notify-send 'Volume:'$OPTARG -t 1000 && echo "set volume:"$OPTARG"%"
                    fi
                    ;;
                m)
                    pactl set-sink-mute 0 toggle
                    if [ $muted == 'yes' ];then
                            notify-send 'Volume - '$sysValue -t 1000
                    else
                            notify-send 'Muted' -u critical -t 1500
                    fi
                    ;;
                u)
                    up=$((10#${sysValue}+5))
                    if [ $up -le 100 ];then
                            pactl set-sink-volume 0 ${up}%
                            notify-send 'Volume - '$up -t 1000
                            if [ $muted == 'yes' ];then
                                    pactl set-sink-mute 0 0
                            fi
                    fi
                    ;;
                d)
                    current=$((10#${sysValue}-5))
                    if [ $current -gt 0 ];then
                            pactl set-sink-volume 0 ${current}%
                            notify-send 'Volume - '$current -t 1000
                            if [ $muted == 'yes' ];then
                                    pactl set-sink-mute 0 0
                            fi
                    elif [ $current -eq 0 ];then
                            pactl set-sink-volume 0 ${current}%
                            pactl set-sink-mute 0 1
                    fi
                    ;;
                g)
                    echo -n $sysValue
                    ;;
                ?)
                    echo "record_menu: [invalid charactor]!"
                    ;;
            esac

        done
        shift $(($OPTIND - 1))
    fi
}

function shell_control_center_main()
{
    local option
    local OPTIND

    while getopts :pvrh option
    do
        printChar="$OPTARG"
        case $option in
            p)
                # echo "play"
                shift $(($OPTIND - 1))
                # echo $@
                playback_menu $@
                ;;
            r)
                echo "record"
                ;;
            v)
                volume_control $@
                ;;
            ?)
                # echo "shell_control_center_main: [invalid charactor]!"
                ;;
        esac

    done
    shift $(($OPTIND - 1))
    # secondary_menu $@

}

shell_control_center_main "$@"

function test()
{
if [ $# -eq 1 ];then
	if command -v ffplay > /dev/null;then
		echo "hh"
	else 
		ffplay_path="$iutils/ffplay-darwin"
	fi
	if [[ $(get_platform) == 'darwin' ]];then
		result=$(ps aux | grep ffplay | grep -v grep | grep -v grep | awk -F ' '  '{ print $2}')
	else
		result=$(ps -lfe | grep ffplay | grep -v grep | awk -F ' '  '{ print $4}')
	fi

	isURL=$(echo $1 | grep -E 'http(s)?')
	echo "result:$result"
	if [[ "$result" != '' ]];then
			case "$1" in
				'PAUSE' )
				kill -STOP $result
				;;
				'RESUME')
				kill -CONT $result
				;;
				'STOP')
				kill -KILL $result
				;;
				'STATUS')
				echo $result
				;;
				'BGPLAY')
				;;
				*)
				;;
			esac
	fi
		if [[ "$isURL" ]];then
			{
				$ffplay_path -nodisp -autoexit -loglevel quiet $1
				#curl -L $1 | ffplay -nodisp -autoexit -
			} &
	  fi
fi
}
